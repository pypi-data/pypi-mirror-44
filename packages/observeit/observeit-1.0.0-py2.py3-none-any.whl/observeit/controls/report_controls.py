"""ObserveIT Report APIs"""

from datetime import datetime
import logging
try:
    # Python 3
    import urllib.parse as urllib_parse
except:
    # Python 2
    import urllib as urllib_parse
from string import Template
import traceback

LOG = logging.getLogger(__name__)

def create_rql(rql_template, **kwargs):
    """urlencode params before rendering them into template"""
    query_values = {}
    for key, value in kwargs.items():
        query_values[key] = urllib_parse.quote(str(value))

    template = Template(rql_template)
    return template.safe_substitute(query_values)
#end create_rql

def get_streaming_report(client, report_id, limit=None, since=None, fields=None,
                         realm="observeit", response_type="json"):
    url = "report;realm=%s/reports/%s/stream" % (realm, report_id)
    query_params = {}
    if response_type not in client.RESPONSE_TYPES:
        raise ValueError("response_type '%s' should be one of: %s" % (response_type, str(client.RESPONSE_TYPES)))
    if limit:
        query_params['limit'] = limit
    if fields:
        query_params['fields'] = ','.join(fields)
    if since:
        if isinstance(since, datetime):
            # format like 2018-05-05T14:49:08.522Z
            formatted_since = since.strftime("%Y-%m-%dT:%H:%M:%S.000Z")
        else:
            formatted_since = since
        query_params['since'] = formatted_since

    try:
        return client.make_request(url, params=query_params,
                                    headers = {"accept": client.RESPONSE_TYPES[response_type]})
    except Exception as e:
        LOG.error("Failed to get report from ObserveIT!")
        LOG.debug(traceback.format_exc())
        raise
# end get_streaming_report

def get_report(client, report_id, rql=None, realm="observeit", response_type="json"):
    url = "report;realm=%s/reports/%s/data" % (realm, report_id)
    query_params = {}
    if response_type not in client.RESPONSE_TYPES:
        raise ValueError("response_type '%s' should be one of: %s" % (response_type, str(client.RESPONSE_TYPES)))
    if rql:
        query_params['rql'] = rql
    try:
        return client.make_request(url, params=query_params,
                                 headers={"accept": client.RESPONSE_TYPES[response_type]})
    except Exception as e:
        LOG.error("Failed to get report from ObserveIT!")
        LOG.debug(traceback.format_exc())
        raise
# end get_report

def get_streaming_analytics_report(client, report_id, limit=None, since=None, fields=None, realm="observeit", response_type="json"):
    # TBD
    raise NotImplementedError()

def get_analytics_report(client, report_id, rql=None, realm="observeit", response_type="json"):
    # TBD
    raise NotImplementedError()
