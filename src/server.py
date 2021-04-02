import sys
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError, AccessError
from src import config
from src.auth import auth_login_v2, auth_register_v2
from src.channel import channel_addowner_v1
from src.user import user_profile_setname_v2
from src.other import clear_v1
from src.helper import is_valid_token


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


@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    return jsonify({})


@ APP.route("/auth/login/v2", methods=['POST'])
def login_v2():
    data = request.get_json()
    return jsonify(auth_login_v2(data['email'], data['password']))


@ APP.route("/auth/register/v2", methods=['POST'])
def register_v2():
    data = request.get_json()
    return jsonify(auth_register_v2(data['email'], data['password'], data['name_first'], data['name_last']))


@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    decoded_token = is_valid_token(data['token'])
    if decoded_token is False:
        raise AccessError("Invalid Token.")
    return jsonify(channel_addowner_v1(decoded_token['user_id'], data['channel_id'], data['u_id']))


@APP.route("/user/profile/setname/v2", methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    decoded_token = is_valid_token(data['token'])
    if decoded_token is False:
        raise AccessError("Invalid Token.")
    user_profile_setname_v2(
        decoded_token['user_id'], data['name_first'], data['name_last'])
    return jsonify({})


if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
