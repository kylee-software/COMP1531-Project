import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config, channel

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

@APP.route("channel/messages/v2", methods=['GET'])
def channel_messages_v2():
    token = request.get_json()['token']
    channel_id = request.get_json()['channel_id']
    start = request.get_json()['start']

    messages_dict = channel.channel_messages_v2(token, channel_id, start)
    return dumps(messages_dict)

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
