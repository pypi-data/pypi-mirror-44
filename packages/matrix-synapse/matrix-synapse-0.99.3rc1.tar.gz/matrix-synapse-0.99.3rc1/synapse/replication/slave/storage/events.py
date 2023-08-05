# -*- coding: utf-8 -*-
# Copyright 2016 OpenMarket Ltd
# Copyright 2018 New Vector Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from synapse.api.constants import EventTypes
from synapse.storage.event_federation import EventFederationWorkerStore
from synapse.storage.event_push_actions import EventPushActionsWorkerStore
from synapse.storage.events_worker import EventsWorkerStore
from synapse.storage.roommember import RoomMemberWorkerStore
from synapse.storage.signatures import SignatureWorkerStore
from synapse.storage.state import StateGroupWorkerStore
from synapse.storage.stream import StreamWorkerStore
from synapse.storage.user_erasure_store import UserErasureWorkerStore

from ._base import BaseSlavedStore
from ._slaved_id_tracker import SlavedIdTracker

logger = logging.getLogger(__name__)


# So, um, we want to borrow a load of functions intended for reading from
# a DataStore, but we don't want to take functions that either write to the
# DataStore or are cached and don't have cache invalidation logic.
#
# Rather than write duplicate versions of those functions, or lift them to
# a common base class, we going to grab the underlying __func__ object from
# the method descriptor on the DataStore and chuck them into our class.


class SlavedEventStore(EventFederationWorkerStore,
                       RoomMemberWorkerStore,
                       EventPushActionsWorkerStore,
                       StreamWorkerStore,
                       StateGroupWorkerStore,
                       EventsWorkerStore,
                       SignatureWorkerStore,
                       UserErasureWorkerStore,
                       BaseSlavedStore):

    def __init__(self, db_conn, hs):
        self._stream_id_gen = SlavedIdTracker(
            db_conn, "events", "stream_ordering",
        )
        self._backfill_id_gen = SlavedIdTracker(
            db_conn, "events", "stream_ordering", step=-1
        )

        super(SlavedEventStore, self).__init__(db_conn, hs)

    # Cached functions can't be accessed through a class instance so we need
    # to reach inside the __dict__ to extract them.

    def get_room_max_stream_ordering(self):
        return self._stream_id_gen.get_current_token()

    def get_room_min_stream_ordering(self):
        return self._backfill_id_gen.get_current_token()

    def stream_positions(self):
        result = super(SlavedEventStore, self).stream_positions()
        result["events"] = self._stream_id_gen.get_current_token()
        result["backfill"] = -self._backfill_id_gen.get_current_token()
        return result

    def process_replication_rows(self, stream_name, token, rows):
        if stream_name == "events":
            self._stream_id_gen.advance(token)
            for row in rows:
                self.invalidate_caches_for_event(
                    token, row.event_id, row.room_id, row.type, row.state_key,
                    row.redacts,
                    backfilled=False,
                )
        elif stream_name == "backfill":
            self._backfill_id_gen.advance(-token)
            for row in rows:
                self.invalidate_caches_for_event(
                    -token, row.event_id, row.room_id, row.type, row.state_key,
                    row.redacts,
                    backfilled=True,
                )
        return super(SlavedEventStore, self).process_replication_rows(
            stream_name, token, rows
        )

    def invalidate_caches_for_event(self, stream_ordering, event_id, room_id,
                                    etype, state_key, redacts, backfilled):
        self._invalidate_get_event_cache(event_id)

        self.get_latest_event_ids_in_room.invalidate((room_id,))

        self.get_unread_event_push_actions_by_room_for_user.invalidate_many(
            (room_id,)
        )

        if not backfilled:
            self._events_stream_cache.entity_has_changed(
                room_id, stream_ordering
            )

        if redacts:
            self._invalidate_get_event_cache(redacts)

        if etype == EventTypes.Member:
            self._membership_stream_cache.entity_has_changed(
                state_key, stream_ordering
            )
            self.get_invited_rooms_for_user.invalidate((state_key,))
