"""Home - Controller

"""
from fabric.connection import Connection
import json
from invoke.exceptions import UnexpectedExit

from flask import Blueprint, Response, request

import app
from app.utilities import parse

home = Blueprint('Home', __name__, url_prefix='/')


@home.route('')
def index():
    """
    Main index page.

    """
    app.app.logger.info('Request from %s for %s' % ('ip', '/'))  # @ todo: handle this
    data = {
        "host": 'host'
    }
    _run_fabric(data)
    return _render(data)


@home.route('/run', methods=["POST"])
def run():
    """
    Will run commands on a remote host.
    Expects JSON data to come in with the following structure.
    {
        'host': 'host_name',
        'cmds': ['du -hs /root/data/backup']
    }

    """
    req_data = _get_request_data()
    app.app.logger.info('Request from %s for %s data: %s' % ('ip', '/', str(req_data)))  # @ todo: handle this
    data = {}
    if not req_data:
        data['status'] = 'failed'
        data['errors'] = 'Could not decode a json request'
        return _render(data)
    data['host'] = req_data.get('host')
    data['cmds'] = req_data.get('cmds')
    _run_fabric(data)
    return _render(data)


def _get_request_data():
    """
    """
    try:
        return request.get_json()
    except AttributeError:
        return None


def _run_fabric(data):
    """
    Runs fabric commands on a 'remote' host.

    """
    host = data.get('host')
    if not host:
        app.app.logger.warning("No 'host' specified in request")
        data['status'] = 'failed'
        data['warnings'] = "No 'host' specified in request"
        return False

    data['responses'] = []
    if data.get('cmds'):
        with Connection(host) as c:
            app.app.logger.debug(data.get('cmds'))
            for cmd in data.get('cmds'):
                app.app.logger.debug(cmd)
                rsp = {
                    'cmd': cmd,
                    'output': None
                }
                try:
                    cmd_response = c.run(cmd)
                    rsp['output'] = str(cmd_response)
                except UnexpectedExit:
                    app.app.logger.warning('%s CMD non exit 0' % cmd)
                    rsp['output'] = str(UnexpectedExit.__doc__)
                    data['status'] = 'failed'
                    data['responses'].append(rsp)
                    break
            data['responses'].append(rsp)


def _render(data):
    """
    Draws the JSON response and adds the needed default responses if they dont exist already.

    """
    if not data.get('status'):
        data['status'] = 'success'
    return Response(json.dumps(data), mimetype='text/json')
