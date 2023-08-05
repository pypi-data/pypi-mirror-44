# Copyright 2018 Huawei Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_policy import policy

from manila.policies import base


BASE_POLICY_NAME = 'share_access_rule:%s'


share_access_rule_policies = [
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'get',
        check_str=base.RULE_DEFAULT,
        description="Get details of a share access rule.",
        operations=[
            {
                'method': 'GET',
                'path': '/share-access-rules/{share_access_id}'
            }
        ]),
    policy.DocumentedRuleDefault(
        name=BASE_POLICY_NAME % 'index',
        check_str=base.RULE_DEFAULT,
        description="List access rules of a given share.",
        operations=[
            {
                'method': 'GET',
                'path': ('/share-access-rules?share_id={share_id}'
                         '&key1=value1&key2=value2')
            }
        ]),
]


def list_rules():
    return share_access_rule_policies
