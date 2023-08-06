"""ObserveIT REST API Client authenticated with username and password"""

import json
import logging
import os
import requests
from observeit.clients.observeit_base_client import ObserveITBase
LOG = logging.getLogger(__name__)


class ObserveITLoginClient(ObserveITBase):
    def __init__(self, host, username, password, api_version="v2", verify=True, cafile=None, connect_timeout=None, application_server=None):
        self.username = username
        self.password = password
        self.application_server = application_server
        super(ObserveITLoginClient, self).__init__(host, api_version=api_version, verify=verify, cafile=cafile, connect_timeout=connect_timeout)
    # end __init__

    def connect(self):
        """Establish authenticated session to ObserveIT REST API"""
        LOG.debug("Connecting to %s", self.host)
        if not self.host.startswith("https://"):
            LOG.warn("Connecting with Insecure Transport Protocol! HTTPS Strongly Encouraged!")
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        auth_url = "%s/%s/apis/auth/logins" % (self.host, self.api_version)
        session = requests.session()
        LOG.debug("POST login info to %s", auth_url)
        credentials = {
            "username": self.username,
            "password": self.password
            }
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json"
            }
        session.headers = headers
        session.verify = self.verify
        response = None
        if self.cafile:
            # Verify SSL connection using this Certificate File. (for self-signed certs)
            session.verify = self.cafile
        elif not self.verify:
            session.verify = False
        try:
            response = session.post(auth_url, data=json.dumps(credentials),
                                    timeout=self.connect_timeout)
            response.raise_for_status()
        except Exception as e:
            LOG.error("Attempt to connect to ObserveIT Failed")
            if response:
                LOG.debug(response.text)
            raise
        LOG.debug(json.dumps(response.json(), indent=2))
        token = "Bearer " + response.json().get("access_token")
        session.headers["Authorization"] = token
        LOG.debug("Successfully connected to ObserveIT API.")
        return self.retryable_session(session)
    # end connect
