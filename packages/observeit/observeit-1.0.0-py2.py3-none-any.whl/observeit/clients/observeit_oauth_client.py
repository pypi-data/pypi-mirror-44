"""ObserveIT REST API Client authenticated with OAUTH"""

import logging
import os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from observeit.clients.observeit_base_client import ObserveITBase
LOG = logging.getLogger(__name__)


class ObserveITOAUTHClient(ObserveITBase):
    def __init__(self, host, client_id, client_secret, api_version="v2", verify=True,
                 cafile=None, connect_timeout=None):
        self.client_id = client_id
        self.client_secret = client_secret
        super(ObserveITOAUTHClient, self).__init__(host, api_version=api_version,
                                                   verify=verify, cafile=cafile,
                                                   connect_timeout=connect_timeout)
    # end __init__

    def connect(self):
        """Establish authenticated session to ObserveIT REST API"""
        LOG.debug("Connecting to %s", self.host)
        if not self.host.startswith("https://"):
            LOG.warn("Connecting with Insecure Transport Protocol! HTTPS Strongly Encouraged!")
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        client = BackendApplicationClient(client_id=self.client_id)
        observeit = OAuth2Session(client=client)

        if self.cafile and self.verify:
            # Verify SSL connection using this Certificate File. (for self-signed certs)
            observeit.verify = self.cafile

        token_url = "%s/%s/apis/auth/oauth/token" % (self.host, self.api_version)
        token = observeit.fetch_token(token_url=token_url, client_id=self.client_id,
                                      client_secret=self.client_secret, scope=["*"],
                                      include_client_id=True,
                                      verify=self.verify, timeout=self.connect_timeout)
        if not token:
            raise RuntimeError("Failed to fetch token from ObserveIT")

        LOG.debug("Successfully connected to ObserveIT API.")
        return self.retryable_session(observeit)
    # end connect
