#
# Copyright 2018 PyWren Team
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
#

import time
import logging
import random
from pywren_ibm_cloud.cf_connector import CloudFunctions

logger = logging.getLogger(__name__)


class IBMCloudFunctionsInvoker:

    def __init__(self, cf_config, retry_config):
        self.namespace = cf_config['namespace']
        self.endpoint = cf_config['endpoint']
        self.cf_action_name = cf_config['action_name']  # Runtime
        self.invocation_retry = retry_config['invocation_retry']
        self.retry_sleeps = retry_config['retry_sleeps']
        self.retries = retry_config['retries']
        self.client = CloudFunctions(cf_config)

        log_msg = 'IBM Cloud Functions init for Runtime: {}'.format(self.cf_action_name)
        logger.info(log_msg)
        if(logger.getEffectiveLevel() == logging.WARNING):
            print(log_msg)

    def invoke(self, payload):
        """
        Invoke -- return information about this invocation
        """
        act_id = self.client.invoke(self.cf_action_name, payload)
        attempts = 1

        while not act_id and self.invocation_retry and attempts < self.retries:
            attempts += 1
            selected_sleep = random.choice(self.retry_sleeps)
            exec_id = payload['executor_id']
            call_id = payload['call_id']

            log_msg = ('Executor ID {} Function {} - Invocation failed - retry {} in {} seconds'.format(exec_id, call_id, attempts, selected_sleep))
            logger.debug(log_msg)

            time.sleep(selected_sleep)
            act_id = self.client.invoke(self.cf_action_name, payload)

        return act_id

    def config(self):
        """
        Return config dict
        """
        return {'cf_action_name': self.cf_action_name,
                'cf_namespace': self.namespace,
                'cf_endpoint': self.endpoint}
