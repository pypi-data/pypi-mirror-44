#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Command line tool to use ObserveIT REST API"""
from __future__ import print_function
import calendar
import datetime
import json
import logging
import time
import traceback
import click
import requests
from observeit.clients.observeit_login_client import ObserveITLoginClient
from observeit.clients.observeit_oauth_client import ObserveITOAUTHClient
from observeit.controls import report_controls, list_controls, application_controls, session_controls
try:
    from builtins import input
except ImportError:
    # Python 2
    from __builtin__ import raw_input as input

LOG = logging.getLogger("observeit")
LOG.addHandler(logging.StreamHandler())
LOG.setLevel(logging.INFO)


def wrap_cli():
    # Wrapper so we can pass arguments
    cli(auto_envvar_prefix='OBSERVEIT')


def validate_url(ctx, param, value):
    if not (value.lower().startswith("https://") or value.lower().startswith("http://")):
        raise click.BadParameter('ObserveIT URL should start with HTTPS:// or HTTP://')
    return value


@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Show debug output')
@click.option('--noverify', is_flag=True, help="Don't check SSL certificate validity")
@click.pass_context
def cli(ctx, verbose, noverify):
    ctx.obj = {}
    ctx.obj['noverify'] = noverify
    if noverify:
        LOG.warning("Insecure Warning! Certificates will not be verified. Further warnings supressed.")
        requests.packages.urllib3.disable_warnings()
    if verbose:
        LOG.setLevel(logging.DEBUG)
        LOG.debug("Verbose Logging Enabled")


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.option('-i', '--clientid', default=None, prompt="Client ID: ",
              help="Client ID for ObserveIT OAUTH Authentication")
@click.option('-s', '--clientsecret', default=None, prompt="Client Secret: ",
              help="Client Secret for ObserveIT OAUTH Authentication")
@click.option('--since', default=None, help="Optional start time. Otherwise current time used. Ex. 2019-03-04T21:29:20.681Z")
@click.argument('name', nargs=1,
                type=click.Choice(['alert_v0', 'user_command_activity_v0',
                                   'user_interface_activity_v0',
                                   'user_activity_profile_tz_daily_pull_v0']))
@click.pass_obj
def stream_report(obj, observeit, clientid, clientsecret, name, since):
    """Print out new events from a report as they come in"""
    client = ObserveITOAUTHClient(observeit, client_id=clientid,
                                  client_secret=clientsecret, verify=not obj['noverify'])
    since = since or datetime.datetime.utcnow().isoformat()[:23] + 'Z'
    LOG.info("Begin Streaming %s Events...", name)
    while(True):
        data = []
        try:
            response = report_controls.get_streaming_report(client, name, response_type="jsonl", limit=100, since=since)
            data = response.text.rstrip("\n").split("\n") if response.text else []

        except Exception as e:
            LOG.error("Failed to retrieve %s from ObserveIT!: %s", name, e)

        if not data:
            LOG.debug("No data returned")
        else:
            for row in data:
                print(row)
            since = json.loads(data[-1])["risingValue"]
        time.sleep(3)
# end stream_report


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.option('-i', '--clientid', default=None, prompt="Client ID: ",
              help="Client ID for ObserveIT OAUTH Authentication")
@click.option('-s', '--clientsecret', default=None, prompt="Client Secret: ",
              help="Client Secret for ObserveIT OAUTH Authentication")
@click.option('-h', '--hours', default=2, type=click.INT,
              help="How many hours of activities to pull?")
@click.option('-l', '--login', type=click.STRING, prompt="User's Login: ",
              help="Which user to summarize activities for")
@click.pass_obj
def user_activity_summary(obj, observeit, clientid, clientsecret, hours, login):
    """Summary of a user's recent application usage"""
    client = ObserveITOAUTHClient(observeit, client_id=clientid,
                                  client_secret=clientsecret, verify=not obj['noverify'])
    since =  int(calendar.timegm(time.gmtime()) * 1000) - (hours * 60 * 60 * 1000)
    data = []
    try:
        rql = report_controls.create_rql("and(eq(loginName,$loginname),limit($limit),gt(risingValue,epoch:$time),aggregate(applicationName,windowTitle,as(min(observedAt),firstObserved),as(max(observedAt),lastObserved),as(count(),count)))", loginname=login, time=since, limit=500)
        response = report_controls.get_report(client, "user_interface_activity_v0", rql)
        data = response.json()
    except Exception as e:
        LOG.error("Failed to retrieve events from ObserveIT! %s", e)
        LOG.debug(traceback.format_exc())

    if not data:
        LOG.debug("No data returned")
    else:
        print("Activity Summary for %s for last %d hours:" % (login, hours))
        print(json.dumps(data["data"], indent=2))
# end user_activity_summary


@cli.command()
@click.argument('application_name', nargs=1)
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.pass_obj
def create_app(obj, observeit, application_name, username, password):
    """Create a new application for OAuth2 Authentication"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    response = application_controls.create_application(client, application_name)
    data = response.json()
    print("Client ID: %s" % data["id"])
    print ("Client Secret: %s" % data["clientSecret"])
# end create_app


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('list_name', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.pass_obj
def print_list(obj, observeit, list_name, username, password):
    """Print out all values in an existing list"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    items = list_controls.get_list_items(client, list_name)
    print("Contents of %s:"% list_name)
    for value in items:
        print(value)
    if not items:
        print("<Empty List>")
# end print_list


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('list_name', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--item', type=click.STRING, help="value to add to list", multiple=True)
@click.pass_obj
def create_list(obj, observeit, list_name, item, username, password):
    """Create a new list and set its items"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    list_controls.create_list(client, list_name, items=item)
    print("Created list %s" % list_name)
# end create_list


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('list_name', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--item', type=click.STRING, help="value to add to list", multiple=True)
@click.pass_obj
def add_list_items(obj, observeit, list_name, item, username, password):
    """Append additional items to existing list"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    num_added = list_controls.add_list_items(client, list_name, items=item)
    print("Successfully added %d items to list" % num_added)
# end add_list_items


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('list_name', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--item', type=click.STRING, help="value to add to list", multiple=True)
@click.pass_obj
def set_list_items(obj, observeit, list_name, item, username, password):
    """Replace all items in list with new values"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    num_added = list_controls.set_list_items(client, list_name, items=item)
    print("Successfully updated list with %d items" % num_added)

# end set_list_items


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('list_name', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--item', type=click.STRING, help="value to add to list", multiple=True)
@click.pass_obj
def remove_list_items(obj, observeit, list_name, item, username, password):
    """Remove specified items from existing list"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    num_removed = list_controls.remove_list_items(client, list_name, items=item)
    print("Successfully removed %d items." % num_removed)

# end remove_list_items


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('session_id', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--dest', type=click.Path(exists=True), help="Destination Directory")
@click.pass_obj
def download_session(obj, observeit, session_id, username, password, dest):
    """Save session screenshots to a directory"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    location = session_controls.export_session(client, session_id, dest_dir=dest)
    print("Successfully saved session to %s" % location)
# end download_session


@cli.command()
@click.option('-o', '--observeit', type=click.STRING, required=True, prompt="Observeit Base URL",
              help="Base URL for observeit. Like http://myobserveit:443",
              callback=validate_url)
@click.argument('session_id', nargs=1)
@click.option('-u', '--username', prompt="ObserveIT Account Username",
              help="Username for ObserveIT Authentication")
@click.option('-p', '--password', hide_input=True,
              prompt="ObserveIT Account Password: ",
              help="Password for ObserveIT Authentication")
@click.option('--dest', type=click.Path(exists=True), help="Destination Directory")
@click.pass_obj
def make_video(obj, observeit, session_id, username, password, dest):
    """Create video from session screenshots and metadata"""
    client = ObserveITLoginClient(observeit, username=username,
                                  password=password, verify=not(obj['noverify']))
    location = session_controls.make_video(client, session_id, dest_dir=dest)
    print("Successfully saved session video to %s" % location)
# end make_video
