import sys
from json import dumps
from types import prepare_class

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

from src import config
from src.auth import auth_login_v2, auth_logout_v1, auth_register_v2
from src.channel import (channel_addowner_v1, channel_details_v1,
                         channel_invite_v1, channel_join_v1, channel_leave_v1)
from src.channels import (channels_create_v2, channels_list_v2,
                          channels_listall_v2)
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1, dm_remove_v1
from src.error import AccessError, InputError
from src.helper import is_valid_token
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1
from src.user import user_profile_setname_v2, user_profile_v2


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


@ APP.route("/message/senddm/v1", methods=['POST'])
def message_senddm():
    data = request.get_json()
    return jsonify(message_senddm_v1(data['token'], data['dm_id'], data['message']))


@ APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    return jsonify(channel_leave_v1(data['token'], data['channel_id']))


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
    user_profile_setname_v2(
        data['token'], data['name_first'], data['name_last'])
    return jsonify({})


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


@APP.route('/channels/listall/v2', methods=['GET'])
def listall_channels():
    token = request.args.get('token')
    channels_list = channels_listall_v2(token)
    return jsonify(channels_list)


@APP.route('/dm/details/v1', methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    if dm_id.isdigit():
        details = dm_details_v1(token, int(dm_id))
    else:
        details = dm_details_v1(token, dm_id)

    return jsonify(details)


@APP.route('/dm/invite/v1', methods=['POST'])
def dm_invite():
    data = request.get_json()
    dm_invite_v1(data['token'], data['dm_id'], data['u_id'])
    return jsonify({})


@APP.route('/message/send/v2', methods=['POST'])
def message_send():
    data = request.get_json()
    msg_id = message_send_v2(
        data['token'], data['channel_id'], data['message'])
    return jsonify(msg_id)


@APP.route('/auth/logout/v1', methods=['POST'])
def auth_logout():
    data = request.get_json()
    is_success = auth_logout_v1(data['token'])
    return jsonify(is_success)


@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove():
    data = request.get_json()
    return jsonify(dm_remove_v1(data['token'], data['dm_id']))


if __name__ == "__main__":
    APP.run(port=config.port)  # Do not edit this port
