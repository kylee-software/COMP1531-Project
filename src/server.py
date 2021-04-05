import sys
from json import dumps
from types import prepare_class
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError
from src.dm import dm_create_v1, dm_details_v1
from src import config
from src.channel import channel_details_v1, channel_join_v1, channel_invite_v1, channel_leave_v1
from src.other import clear_v1
<<<<<<< HEAD
from src.channels import channels_create_v2, channels_list_v2
=======
from src.user import user_profile_v2
from src.channels import channels_create_v2
>>>>>>> master
from src.auth import auth_login_v2, auth_register_v2
from src.message import message_send_v2


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

@APP.route("/channel/details/v2", methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    try:
        channel_id = int(channel_id)
    except:
        pass
    return dumps(channel_details_v1(token, channel_id))

@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    return dumps(channel_join_v1(data['token'], data['channel_id']))

@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite():
    data = request.get_json()
    u_id = data['u_id']
    channel_id = data['channel_id']
    return jsonify(channel_invite_v1(data['token'], channel_id, u_id))


@APP.route("/user/profile/v2", methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    if u_id.isdigit():
        details = user_profile_v2(token, int(u_id))
    else:
        details = user_profile_v2(token, u_id)
    return jsonify(details)

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


@ APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    return jsonify(channel_leave_v1(data['token'], data['channel_id']))


@APP.route("/channels/create/v2", methods=['POST'])
def channels_create():
    data = request.get_json()
    dict = channels_create_v2(data['token'], data['name'], data['is_public'])
    return jsonify(dict)


@APP.route("/dm/create/v1", methods=['POST'])
def dm_create():
    data = request.get_json()
    dm_dict = dm_create_v1(data['token'], data['u_ids'])

    return jsonify(dm_dict)

@APP.route('/channels/list/v2', methods=['GET'])
def list_channels():
    token = request.args.get('token')
    list = channels_list_v2(token)
    return jsonify(list)
    
@APP.route('/dm/details/v1', methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    if dm_id.isdigit():
        details = dm_details_v1(token, int(dm_id))
    else:
        details = dm_details_v1(token, dm_id)
    
    return jsonify(details)
    
@APP.route('/message/send/v2', methods=['POST'])
def message_send():
    data = request.get_json()
    msg_id = message_send_v2(data['token'], data['channel_id'], data['message'])
    return jsonify(msg_id)


if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
