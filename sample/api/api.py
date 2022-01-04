# -*- coding: UTF-8 -*-
import json

import attr
import logging

import time
from typing import List

from larksuiteoapi.api import Request, FormData, FormDataFile, set_timeout, set_path_params, set_query_params, \
    set_is_response_stream, set_response_stream, set_tenant_key

from larksuiteoapi import Config, ACCESS_TOKEN_TYPE_TENANT, ACCESS_TOKEN_TYPE_USER, ACCESS_TOKEN_TYPE_APP, \
    DOMAIN_FEISHU, LEVEL_ERROR, LEVEL_DEBUG
from larksuiteoapi.utils.dt import to_json_decorator, make_datatype

from sample.config.config import test_config_with_memory_store, test_config_with_redis_store

# for Cutome APP（企业自建应用）
app_settings = Config.new_internal_app_settings_from_env()

# for redis store and logger(level=debug)
# conf = test_config_with_redis_store(DOMAIN_FEISHU, app_settings)

# for memory store and logger(level=debug)
conf = Config(DOMAIN_FEISHU, app_settings, log_level=LEVEL_DEBUG)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


@attr.s
class Message(object):
    message_id = attr.ib(type=str)


def test_send_message():
    body = {
        "user_id": "77bbc392",
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "[飞书](https://www.feishu.cn)整合即时沟通、日历、音视频会议、云文档、云盘、工作台等功能于一体，成就组织和个人，更高效、更愉悦。"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "value": {"value": 1, "value2": "str"},
                            "text": {
                                "tag": "plain_text",
                                "content": "主按钮"
                            },
                            "type": "primary"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "次按钮"
                            },
                            "type": "default"
                        },
                        {
                            "tag": "button",
                            "text": {
                                "tag": "plain_text",
                                "content": "危险按钮"
                            },
                            "type": "danger"
                        }
                    ]
                }
            ]
        }
    }

    req = Request('/open-apis/message/v4/send', 'POST', ACCESS_TOKEN_TYPE_TENANT, body,
                  output_class=Message, request_opts=[set_timeout(3)])
    resp = req.do(conf)
    print('header = %s' % resp.get_header().items())
    print('request id = %s' % resp.get_request_id())
    print(resp)
    if resp.code == 0:
        print(resp.data.message_id)
    else:
        print(resp.msg)
        print(resp.error)


def test_upload_file():
    with open('./test.png', 'rb') as img:
        formData = FormData()
        formData.add_param('image_type', 'message')
        formData.add_file('image', FormDataFile(img))
        req = Request('image/v4/put', 'POST', ACCESS_TOKEN_TYPE_TENANT, formData)
        resp = req.do(conf)
        print('request id = %s' % resp.get_request_id())
        print(resp)
        if resp.code == 0:
            print(resp.data)
        else:
            print(resp.msg)
            print(resp.error)


def test_download_file(timeout=False):
    body = {
        "image_key": "img_6b6fe6d0-75d8-47d2-9725-54b6d535d86g",
    }
    operations = [set_is_response_stream()]
    if timeout:
        operations += [set_timeout(0.001)]

    f = open('./a1.png', 'wb')
    operations += [set_response_stream(f)]

    req = Request('image/v4/get', 'GET',
                  [ACCESS_TOKEN_TYPE_TENANT], body, request_opts=operations)
    resp = req.do(conf)
    print('request id = %s' % resp.get_request_id())
    print('http status code = %s' % resp.get_http_status_code())
    if resp.code != 0:
        print(resp.msg)
        print(resp.error)


if __name__ == '__main__':
    test_send_message()
    # test_download_file()
    # test_upload_file()
    # test_user_update()
