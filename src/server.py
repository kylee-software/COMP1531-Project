import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src.dm import dm_create_v1, dm_messages_v1
from src import config

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("dm/create/v1", methods=['POST'])
def dm_create_v1():
    token = request.args.get('token')
    u_ids = request.args.get('u_ids')
    dm_dict = dm_create_v1(token, u_ids)

    return dumps(dm_dict)

@APP.route("dm/messages/v1", methods=['GET'])
def dm_messages_v1():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')

    messages_dict = dm_messages_v1(token, dm_id, start)
    return dumps(messages_dict)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
