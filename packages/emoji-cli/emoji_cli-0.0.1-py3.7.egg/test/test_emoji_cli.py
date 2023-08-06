# coding=utf-8
# emoji_const.py 单元测试
# 2019.04.10 create by binbin.hou
from emoji_cli.emoji_cli import *


class TestEmojiCli(object):

    def test_name(self):
        """
        测试名称
        :return: none
        """
        print()
        EmojiCli.name("❤")

    def test_name_not_exists(self):
        """
        测试名称-不存在
        :return: none
        """
        print()
        EmojiCli.name("redheart")

    def test_emoji(self):
        """
        测试表情
        :return: none
        """
        print()
        EmojiCli.emoji("redheart")

    def test_emoji_not_exists(self):
        """
        测试表情-不存在
        :return: none
        """
        print()
        EmojiCli.emoji("❤")
