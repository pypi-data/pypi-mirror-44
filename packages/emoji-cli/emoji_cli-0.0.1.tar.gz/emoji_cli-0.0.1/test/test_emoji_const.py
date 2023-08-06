# coding=utf-8
# emoji_const.py 单元测试
# 2019.04.10 create by binbin.hou
from emoji_cli import emoji_const as const


class TestEmojiConst(object):

    def test_const(self):
        """
        测试常量
        :return: none
        """
        assert "UTF-8" == const.DEFAULT_CHARSET
        assert "/db/emoji.data" == const.EMOJI_DATA_PATH
