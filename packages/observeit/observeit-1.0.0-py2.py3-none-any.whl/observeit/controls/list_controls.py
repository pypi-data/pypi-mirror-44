"""ObserveIT Control API"""

import json
import logging
import traceback
from requests import HTTPError
from observeit.decorators import login_auth_only

LOG = logging.getLogger(__name__)

# Map list names to IDs
LIST_MAP = {}


@login_auth_only
def create_list(client, list_name, list_type="general", items=None, description=None):
    if list_type not in ("general", "user"):
        raise ValueError("list_type should be one of: general, user")
    list_type = "it:control:list-kinds:general" if list_type == "general" else "it:control:list-kinds:user"
    description = description or "created with observeit cli tool"
    list_data = {
        "kind": list_type,
        "permission": "public",
        "details": {
            "name": list_name,
            "description": description
            },
        "items": []
        }
    if items:
        for item in items:
            list_data["items"].append(
                {"details": {
                    "value": item,
                    "name": item
                    }
                })

    url = "control/lists"
    try:
        response = client.make_request(url, method="post", data=json.dumps(list_data),
                                       headers={"Accept": "application/json",
                                                "Content-Type": "application/json"},
                                       extend_base_url="/ObserveIT")
    except HTTPError as e:
        LOG.error("List creation failed")
        return False
    return True
# end create_list


def _get_list_id(client, list_name):
    """Get a list ID from the name"""
    if list_name in LIST_MAP:
        return LIST_MAP[list_name]
    try:
        url = "control/lists/"
        response = client.make_request(url,
                                       params={"limit": 1000},
                                       headers={"Accept": "application/json"},
                                       extend_base_url="/ObserveIT")
        for item in response.json()["data"]:
            if item["details"]["name"] == list_name:
                list_id = item["id"]
                LOG.debug("List ID found: %s", list_id)
                # Save it so we won't need to look it up again
                LIST_MAP[list_name] = list_id
                return list_id
        raise LookupError("List %s not found" % list_name)
    except HTTPError as e:
        LOG.error("Get ID for list %s failed", list_name)
        raise
# end _get_list_id


@login_auth_only
def add_list_items(client, list_name, items):
    """Append additional values to the list"""
    num_added = 0
    # First we need to translate the list_name to an id
    list_id = _get_list_id(client, list_name)

    url = "/control/lists/%s/items" % list_id
    for item in items:
        data = {
            "details": {
                "value": item,
                "name": item
            }
            }

        try:
            response = client.make_request(url, method="post", data=json.dumps(data),
                                           headers={"Accept": "application/json",
                                                    "Content-Type": "application/json"},
                                           extend_base_url="/ObserveIT")
            num_added = num_added + 1
        except HTTPError as e:
            LOG.error("Failed to add '%s' to %s", item, list_name)
    return num_added
# end add_list_items

@login_auth_only
def set_list_items(client, list_name, items):
    """Replace all list items with a new set"""
    # First we need to get the existing list
    try:
        url = "control/lists/"
        list_to_update = None
        response = client.make_request(url,
                                       params={"limit": 1000},
                                       headers={"Accept": "application/json"},
                                       extend_base_url="/ObserveIT")
        for item in response.json()["data"]:
            if item["details"]["name"] == list_name:
                list_id = item["id"]
                list_to_update = item
                LOG.debug("List ID found: %s", list_id)
                break
        else:
            raise LookupError("List %s not found" % list_name)
    except HTTPError as e:
        LOG.error("Get ID for list %s failed", list_name)
        raise

    # Put the item list into the returned structure
    list_to_update["items"] = []
    for item in items:
        data = {
            "details": {
                "value": item,
                "name": item
                }
            }
        list_to_update["items"].append(data)

    # Put the updates back to ObserveIT
    try:
        url = "control/lists/" + list_id
        response = client.make_request(url, method="put", data=json.dumps(list_to_update),
                                       headers={"Accept": "application/json",
                                                "Content-Type": "application/json"},
                                       extend_base_url="/ObserveIT")
        return len(items)
    except HTTPError as e:
        LOG.error("Failed to replace items in list %s", list_name)
        raise

# end set_list_items


@login_auth_only
def get_list_items(client, list_name):
    """Return list of values of items in the list"""
    # First we need to translate the list_name to an id
    list_id = _get_list_id(client, list_name)

    # Now get the items
    url = "control/lists/%s/items" % list_id
    response = client.make_request(url,
                                   headers={"accept": "application/json"},
                                   extend_base_url="/ObserveIT")
    return [item["details"]["value"] for item in response.json()["data"]]
# end get_list_items


@login_auth_only
def remove_list_items(client, list_name, items):
    """Remove the values from the list"""
    # First we need to get the existing list
    try:
        url = "control/lists/"
        list_to_update = None
        response = client.make_request(url,
                                       params={"limit": 1000},
                                       headers={"Accept": "application/json"},
                                       extend_base_url="/ObserveIT")
        for item in response.json()["data"]:
            if item["details"]["name"] == list_name:
                list_id = item["id"]
                list_to_update = item
                LOG.debug("List ID found: %s", list_id)
                break
        else:
            raise LookupError("List %s not found" % list_name)
    except HTTPError as e:
        LOG.error("Get ID for list %s failed", list_name)
        raise

    # Now get the existing list items
    url = "control/lists/%s/items" % list_id
    response = client.make_request(url,
                                   headers={"accept": "application/json"},
                                   extend_base_url="/ObserveIT")
    item_list = response.json()["data"]
    updated_list = [val for val in item_list if val["details"]["value"] not in items]

    # Put the updated list back to ObserveIT
    list_to_update["items"] = updated_list
    try:
        url = "control/lists/" + list_id
        response = client.make_request(url, method="put", data=json.dumps(list_to_update),
                                       headers={"Accept": "application/json",
                                                "Content-Type": "application/json"},
                                       extend_base_url="/ObserveIT")
        return len(item_list) - len(updated_list)
    except HTTPError as e:
        LOG.error("Failed to remove items in list %s", list_name)
        raise
# end remove_list_items
