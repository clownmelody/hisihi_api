# -*- coding: utf-8 -*-
import unittest
from herovii.libs.lean_cloud_system_message import LeanCloudSystemMessage
from herovii.service.im import curl_service_to_lean_cloud


class TestCurlLeanCloud(unittest.TestCase):

    # def test_curl(self):
    #     code, resp = curl_service_to_lean_cloud("Remove", '5552c0c6e4b0846760927d5a', ["LarryPage"])
    #     print(code//100)
    #     print(code)
    #     print(resp)

    def test_send_sys_message(self):
        code, resp = LeanCloudSystemMessage.push_removed_from_group_message("Remove", '5552c0c6e4b0846760927d5a', ["LarryPage"])
        print(code)
        print(resp)

