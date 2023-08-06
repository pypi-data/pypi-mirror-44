# coding=utf-8
# emoji_const.py 单元测试
# 2019.04.10 create by binbin.hou
from emoji_cli.emoji_dict import *


class TestEmojiDict(object):

    def test_name(self):
        """
        测试名称
        :return: none
        """
        emoji_dict = Dict()
        assert "redheart" == emoji_dict.name("❤")

    def test_emoji(self):
        """
        测试表情
        :return: none
        """
        emoji_dict = Dict()
        assert ['❤'] == emoji_dict.emoji("redheart")