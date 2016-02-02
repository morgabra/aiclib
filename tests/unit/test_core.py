# Copyright 2015 Rackspace
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import aiclib
import tests.base as test_base

from tests.unit import fixtures

class ConnectionTestCase(test_base.UnitTestBase):
    def setUp(self):
        super(ConnectionTestCase, self).setUp()

        self.connection = aiclib.nvp.Connection("https://localhost",
          username='fakeuser', password='fakepass', retries=2)

    def test_connection_retries_unauthorized(self):

        # we expect to query lswitches (and auth once), return 401 on the
        # second lswitch query (triggering a re-auth), and finally succeed
        # the third call.
        self._add_response(
            '/ws.v1/login', status=200, headers={'set-cookie': 'fakecookie'})
        self._add_response(
            '/ws.v1/login', status=200, headers={'set-cookie': 'fakecookie'})

        self._add_response(
            '/ws.v1/lswitch', status=200, body=fixtures.LSWITCH_Q,
            headers={"content-type": "application/json",
                     "content-length": str(len(fixtures.LSWITCH_Q))})
        self._add_response(
            '/ws.v1/lswitch', status=401, reason='Unauthorized')
        self._add_response(
            '/ws.v1/lswitch', status=200, body=fixtures.LSWITCH_Q,
            headers={"content-type": "application/json",
                     "content-length": str(len(fixtures.LSWITCH_Q))})

        # First call, should succeed
        self.connection.lswitch().query().results()

        # Second call, should be unauthorized, reauth, and then succeed.
        self.connection.lswitch().query().results()

