import sys
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError
from src import config
from src.helper import is_valid_token
from src.error import AccessError
from src.data import data
from src.auth import auth_login_v2, auth_register_v2
from src.other import clear_v1


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

@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    token = request.args.get('token')
    if not is_valid_token(token):
        raise AccessError("Invalid User")
    token = is_valid_token(token)
    user = next(user for user in data['users'] if user['user_id'] == token['user_id'])
    return jsonify({'user' : {  'u_id' : token['user_id'],
                        'email' : user['email'],
                        'name_first' : user['first_name'],
                        'name_last' : user['lase_name'],
                        'handle_str' : user['handle'],                            
                     }
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


if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
