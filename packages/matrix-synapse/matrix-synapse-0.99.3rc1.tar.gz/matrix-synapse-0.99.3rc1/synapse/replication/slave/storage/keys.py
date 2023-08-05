# -*- coding: utf-8 -*-
# Copyright 2015, 2016 OpenMarket Ltd
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

from synapse.storage import DataStore
from synapse.storage.keys import KeyStore

from ._base import BaseSlavedStore, __func__


class SlavedKeyStore(BaseSlavedStore):
    _get_server_verify_key = KeyStore.__dict__[
        "_get_server_verify_key"
    ]

    get_server_verify_keys = __func__(DataStore.get_server_verify_keys)
    store_server_verify_key = __func__(DataStore.store_server_verify_key)

    get_server_certificate = __func__(DataStore.get_server_certificate)
    store_server_certificate = __func__(DataStore.store_server_certificate)

    get_server_keys_json = __func__(DataStore.get_server_keys_json)
    store_server_keys_json = __func__(DataStore.store_server_keys_json)
