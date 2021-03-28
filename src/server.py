import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config, channels

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

@APP.route("channels/create/v2", methods=['POST'])
def channels_create_v2():
    token = request.get_json()['token']
    name = request.get_json()['name']
    is_public = token = request.get_json()['is_public']

    # Get the return value
    dict = channels.channels_create_v2(token, name, is_public)

    return dumps(dict)


if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
