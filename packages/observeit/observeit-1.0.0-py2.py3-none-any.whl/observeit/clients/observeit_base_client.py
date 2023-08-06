"""ObserveIT REST API Client"""

from abc import abstractmethod
try:
    from abc import ABC
except:
    # python2
    from abc import ABCMeta
    ABC = ABCMeta('ABC', (object,), {})
import calendar
from datetime import datetime
import logging
import traceback
from oauthlib.oauth2 import TokenExpiredError
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

LOG = logging.getLogger(__name__)


class ObserveITBase(ABC):
    RESPONSE_TYPES = {"json": "application/json",
                      "jsonl": "application/jsonl",
                      "csv": "text/csv"}

    def __init__(self, host, api_version="v2", verify=True, cafile=None,
                 connect_timeout=None):
        self.host = host
        self.api_version = api_version
        self.verify = verify
        self.cafile = cafile
        self.connect_timeout = connect_timeout or 10
        self.session = self.connect()
    # end __init__

    @staticmethod
    def convert_observeit_datetime(timestamp):
        # YYYY-MM-DDTHH:MM:SS.mmm+00:00
        """Convert timestamp like 2017-11-15T20:06:16.150Z to epoch in ms"""
        ts = timestamp.replace("Z", "GMT")
        ms = int(ts[-6:-3])
        ts_format = "%Y-%m-%dT%H:%M:%S.%f%Z"
        dt = datetime.strptime(ts, ts_format)
        return int(calendar.timegm(dt.timetuple()) * 1000) + ms
    # end convert_observeit_datetime

    @abstractmethod
    def connect(self):
        """Establish authenticated session to ObserveIT REST API"""
        pass

    def retryable_session(self, session, retries=3, backoff_factor=0.3):
        """ Automatically retry session requests for certain failures """
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            method_whitelist=False, # this will force retry on POST/PATCH/DELETE as well as GET/PUT
            backoff_factor=backoff_factor)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def make_request(self, endpoint, method="get", data=None, headers=None, params=None,
                     extend_base_url="", timeout=20):
        """Make ObserveIT REST Request and Return JSON Response"""
        response = None
        params = params or {}
        method = method.lower()
        if "http://" in endpoint or "https://" in endpoint:
            # Endpoint is a full URL already
            url = endpoint
        else:
            url = "%s%s/%s/apis/%s" % (self.host, extend_base_url, self.api_version, endpoint)
        LOG.debug("%s REQUEST TO %s?%s", method.upper(), endpoint,
                  "&".join([tag+"="+str(value) for tag, value in params.items()]))
        try:
            if method == "get":
                response = self.session.get(url, headers=headers, params=params,
                                            verify=self.verify, timeout=timeout)
            elif method == "post":
                response = self.session.post(url, data=data, headers=headers, params=params,
                                             verify=self.verify, timeout=timeout)
            elif method == "put":
                response = self.session.put(url, data=data, headers=headers, params=params,
                                            verify=self.verify, timeout=tieout)
            elif method == "patch":
                response = self.session.patch(url, data=data, headers=headers, params=params,
                                              verify=self.verify, timeout=timeout)
            elif method == "delete":
                response = self.session.delete(url, headers=headers, params=params,
                                               verify=self.verify, timeout=timeout)
            else:
                raise ValueError("Method '%s' not currently supported" % method)

            LOG.debug("Request Headers:")
            LOG.debug(str(response.request.headers))
            LOG.debug("Response Headers:")
            LOG.debug(str(response.headers))
            if response.status_code not in (requests.codes.ok, requests.codes.created, requests.codes.accepted):
                LOG.error("Bad Status %s: %s" % (response.status_code, response.text))
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "html" in content_type:
                # Not a response we were expecting, probably an IIS error.
                msg = "Unexpected Response content-type: %s" % content_type
                LOG.error(msg)
                LOG.error("ObserveIT Response %s: %s" % (response.status_code, response.text))
                raise RuntimeError(msg)

            return response
        except TokenExpiredError as e:
            # Token expired, refresh token and retry
            LOG.info("Token Expired. Refreshing..")
            self.session = self.connect()
            return self.make_request(endpoint, method=method, data=data,
                                     headers=headers, params=params)
        except Exception as e:
            LOG.error("Unexpected Error: %s", e)
            LOG.debug(traceback.format_exc())
            raise
    # end make_request
