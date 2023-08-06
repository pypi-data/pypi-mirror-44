# -*- coding: utf-8 -*-
"""
Desc: Opencc python dict module.
Author: binbin.hou
Date: 2019-4-10 13:40:20
Since: 0.0.2
"""

# 2019.04.10 binbin.hou created opencc_dict.py at version 0.0.2
import re
import os
from io import open
from openccpy import opencc_const as const
from openccpy.opencc_util import *


class Dict(object):
    """
    获取中文简体和繁体的映射关系类
    """
    # 简体到繁体字典
    __st_char_dict = {}
    __st_phrase_dict = {}

    # 繁体到简体字典
    __ts_char_dict = {}
    __ts_phrase_dict = {}

    # 当前路径
    __current_path = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        """
        初始化方法
        1, 初始化所需要的所有变量信息。
        2. 外部使用此类，建议使用模块导入的方法，保证单例。
        """
        self.__init_dict(const.ST_CHAR_PATH, self.__st_char_dict)
        self.__init_dict(const.ST_PHRASE_PATH, self.__st_phrase_dict)
        self.__init_dict(const.TS_CHAR_PATH, self.__ts_char_dict)
        self.__init_dict(const.TS_PHRASE_PATH, self.__ts_phrase_dict)

    def stc(self, simple):
        """
        获取当前简体字符对应的繁体字符
        :param simple: 简体字符
        :return: 繁体字符
        """
        return Dict.__get_val(simple, self.__st_char_dict)

    def stp(self, simple):
        """
        获取当前简体词组对应的繁体词组
        :param simple: 简体词组
        :return: 繁体词组
        """
        return Dict.__get_val(simple, self.__st_phrase_dict)

    def tsc(self, traditional):
        """
        获取当前简体字符对应的繁体字符
        :param traditional: 繁体字符
        :return: 简体字符
        """
        return Dict.__get_val(traditional, self.__ts_char_dict)

    def tsp(self, traditional):
        """
        获取当前简体词组对应的繁体词组
        :param traditional: 繁体词组
        :return: 简体词组
        """
        return Dict.__get_val(traditional, self.__ts_phrase_dict)

    def __init_dict(self, relative_path, opencc_dict):
        """
        初始化所有的字典信息
        :param relative_path: 相对文件路径
        :param opencc_dict: 原始集合
        :return: 无
        """
        print("Openccpy start init dict...")
        with open(self.__current_path + relative_path, mode="r", encoding=const.DEFAULT_CHARSET) as stc:
            for line in stc:
                regex = re.compile("\s+")
                lines = regex.split(line)
                opencc_dict[lines[0]] = lines[1]
        print("Openccpy start finish dict...")

    @staticmethod
    def __get_val(key, opencc_dict):
        """
        获取对应的值
        1. 如果 key 为空，直接返回
        2. 如果没获取到值，默认返回 key
        3. 如果获取的值为 "\uD86D\uDDF5"，默认返回 key
        :param key: 入参
        :param opencc_dict: 对应的字典信息
        :return: 结果
        """
        if StrUtil.is_empty(key):
            return key
        result = opencc_dict.get(key, key)
        if result == const.EMPTY_RESULT:
            return key
        return result
