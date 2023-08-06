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

import os.path

from kamonohashi.op import object_storage
from kamonohashi.op import rest


def get(api_client, id):
    api = rest.DataSetApi(api_client)
    result = api.get_dataset(id)
    return result


def create(api_client, model):
    api = rest.DataSetApi(api_client)
    result = api.create_dataset(model=model)
    return result


def update(api_client, id, model):
    api = rest.DataSetApi(api_client)
    result = api.update_dataset(id, model=model)
    return result


def update_meta_info(api_client, id, name=None, memo=None):
    api = rest.DataSetApi(api_client)
    model = rest.DataSetApiModelsEditInputModel(name=name, memo=memo)
    result = api.patch_dataset(id, model=model)
    return result


def delete(api_client, id):
    api = rest.DataSetApi(api_client)
    api.delete_dataset(id)


def download_files(api_client, id, dir_path):
    api = rest.DataSetApi(api_client)
    result = api.list_dataset_files(id, with_url=True)
    pool_manager = api_client.rest_client.pool_manager
    for entry in result.entries:
        for file in entry.files:
            destination_dir_path = os.path.join(dir_path, entry.type, str(file.id))
            object_storage.download_file(pool_manager, file.url, destination_dir_path, file.file_name)
