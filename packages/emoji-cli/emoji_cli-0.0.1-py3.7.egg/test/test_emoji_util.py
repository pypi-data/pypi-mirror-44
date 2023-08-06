# coding=utf-8
# emoji_util.py 单元测试
# 2019.04.10 create by binbin.hou
from emoji_cli.emoji_util import *


class TestEmojiUtil(object):
    """
    测试类
    """

    def test_is_empty(self):
        """
        测试是否为空
        :return:
        """
        assert True == StrUtil.is_empty(None)
        assert True == StrUtil.is_empty("")
        assert False == StrUtil.is_empty(" ")
        assert False == StrUtil.is_empty("x")

    def test_is_not_empty(self):
        """
        测试是否不为空
        :return:
        """
        assert False == StrUtil.is_not_empty(None)
        assert False == StrUtil.is_not_empty("")
        assert True == StrUtil.is_not_empty(" ")
        assert True == StrUtil.is_not_empty("x")
