import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
from src.helper import valid_token, get_user_from_token
from src.error import AccessError

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

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications():
    token = request.args.get('token')
    if not valid_token(token):
        raise AccessError("Invalid User")
    user = get_user_from_token(token)
    return {'notifications' : user['notifications']}

if __name__ == "__main__":
    APP.run(port=config.port) # Do not edit this port
