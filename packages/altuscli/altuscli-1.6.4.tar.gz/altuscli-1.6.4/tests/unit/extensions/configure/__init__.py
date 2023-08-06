# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Modifications made by Cloudera are:
#     Copyright (c) 2016 Cloudera, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from altuscli.exceptions import ProfileNotFound


class FakeContext(object):

    def __init__(self, all_variables, profile_does_not_exist=False,
                 config_file_vars={}, environment_vars={},
                 credentials=None):
        self.variables = all_variables
        self.profile_does_not_exist = profile_does_not_exist
        self.config = {}
        self.config_file_vars = config_file_vars
        self.environment_vars = environment_vars
        self._credentials = credentials
        self.profile = None
        self.effective_profile = None
        # This lets us use the FakeContext as both context and "client_creator"
        self.context = self

    def get_credentials(self):
        return self._credentials

    def get_scoped_config(self):
        if self.profile_does_not_exist:
            raise ProfileNotFound(profile='foo')
        return self.config

    def get_config_variable(self, name, methods=None):
        if name == 'credentials_file':
            # The credentials_file var doesn't require a
            # profile to exist.
            return '~/fake_credentials_filename'
        if self.profile_does_not_exist and not name == 'config_file':
            raise ProfileNotFound(profile='foo')
        if methods is not None:
            if 'env' in methods:
                return self.environment_vars.get(name)
            elif 'config' in methods:
                return self.config_file_vars.get(name)
        else:
            return self.variables.get(name)

    def _build_profile_map(self):
        if self.full_config is None:
            return None
        return self.full_config['profiles']
