# -*- coding: utf-8 -*-
"""
Desc: Opencc python module.
Author: binbin.hou
Date: 2019-4-10 13:40:20
Since: 0.0.1
"""

import fire

from emoji_cli.emoji_dict import dict_singleton


class EmojiCli(object):
    """
    1. 当前版本暂时不支持分词
    2. 准备下一期添加分词功能
    """

    @staticmethod
    def emoji(name):
        """
        获取 emoji 说明的结果
        1. name 目前支持英文，大小写不限
        :param name: 目前支持英文，大小写不限
        :return: 对应的 emoji 列表信息
        """
        print(" ".join(dict_singleton.emoji(name)))

    @staticmethod
    def name(emoji):
        """
        获取 emoji 对应的英文
        :param emoji: emoji 表情
        :return: 对应的名称
        """
        print(dict_singleton.name(emoji))


def main():
    fire.Fire(EmojiCli)


if __name__ == '__main__':
    main()
