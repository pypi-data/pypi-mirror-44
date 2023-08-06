# -*- coding: utf-8 -*-
# Copyright 2018 NS Solutions Corporation.
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

from kamonohashi.op import object_storage
from kamonohashi.op import rest


def get(api_client, id):
    api = rest.DataApi(api_client)
    result = api.get_data(id)
    return result


def create(api_client, name, memo=None, tags=()):
    api = rest.DataApi(api_client)
    model = rest.DataApiModelsCreateInputModel(memo=memo, name=name, tags=list(tags))
    result = api.create_data(model=model)
    return result


def update(api_client, id, name=None, memo=None, tags=()):
    api = rest.DataApi(api_client)
    model = rest.DataApiModelsEditInputModel(name=name, memo=memo, tags=list(tags))
    result = api.update_data(id, model=model)
    return result


def delete(api_client, id):
    api = rest.DataApi(api_client)
    api.delete_data(id)


def list_files(api_client, id):
    api = rest.DataApi(api_client)
    result = api.list_data_files(id, with_url=True)
    return result


def upload_file(api_client, id, file_path):
    api = rest.DataApi(api_client)
    upload_info = object_storage.upload_file(api_client, file_path, 'Data')
    model = rest.ComponentsAddFileInputModel(file_name=upload_info.file_name, stored_path=upload_info.stored_path)
    result = api.add_data_file(id, model=model)
    return result


def download_files(api_client, id, dir_path):
    api = rest.DataApi(api_client)
    result = api.list_data_files(id, with_url=True)
    pool_manager = api_client.rest_client.pool_manager
    for x in result:
        object_storage.download_file(pool_manager, x.url, dir_path, x.file_name)
