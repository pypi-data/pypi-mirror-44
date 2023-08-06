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

from __future__ import print_function, absolute_import, with_statement

import contextlib

import six


def to_dict_value(value):
    if hasattr(value, 'to_dict'):
        return to_dict(value)
    if isinstance(value, list):
        return [to_dict_value(x) for x in value]
    if isinstance(value, dict):
        return {k: to_dict_value(v) for k, v in value.items()}
    return value


def to_dict(model):
    """Returns a model properties as a dict.
    This works even when 'value of dict' is 'list of models'.
    """
    result = {}
    for attr, _ in six.iteritems(model.swagger_types):
        value = getattr(model, attr)
        result[attr] = to_dict_value(value)
    return result


@contextlib.contextmanager
def release_conn(response):
    """Call urllib3.response.HTTPResponse.release_conn().
    :param urllib3.response.HTTPResponse response:
    """
    try:
        yield response
    finally:
        response.release_conn()
