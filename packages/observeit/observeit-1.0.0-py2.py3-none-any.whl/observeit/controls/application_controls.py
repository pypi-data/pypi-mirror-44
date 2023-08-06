"""ObserveIT Create New Application"""

import json
import logging
import traceback

LOG = logging.getLogger(__name__)

def create_application(client, app_name):
    """Create a new application in ObserveIT"""
    LOG.info("Creating %s application in ObserveIT", app_name)
    url = "auth/clients"
    data = {
        "name": app_name,
        "redirect_uris": [],
        "allowedGrantTypes": ["client_credentials"]
        }
    try:
        response = client.make_request(url, method="post", data=json.dumps(data),
                                   headers = {"accept": "application/json"})
    except Exception as e:
        LOG.error("Failed to get report from ObserveIT!")
        LOG.debug(traceback.format_exc())
        raise
    LOG.debug("Request Headers:")
    LOG.debug(str(response.request.headers))
    LOG.debug("Response Headers:")
    LOG.debug(str(response.headers))
    LOG.debug(response.text)
    response.raise_for_status()
    LOG.info("Application created successfully")
    return response
# end create_application
