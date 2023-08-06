# -*- coding: utf-8 -*-
"""
Desc: Opencc python module.
Author: binbin.hou
Date: 2019-4-10 13:40:20
Since: 0.0.2
"""

from openccpy.opencc_dict import *


class Opencc(object):
    """
    中文繁简体转换对外开放类
    1. 当前版本暂时不支持分词
    2. 准备下一期添加分词功能
    """

    @staticmethod
    def to_simple(traditional):
        """
        繁体转化为简体
        1. 如果字符为空，直接返回
        2. 字符长度为1，返回对应简体字符
        3. 对应长度大于1，返回对应简体词组
        :param traditional: 繁体单词/单个词组
        :return: 对应的简体信息
        """
        new_dict = Dict()
        if len(traditional) == 1:
            return new_dict.tsc(traditional)
        else:
            return new_dict.tsp(traditional)

    @staticmethod
    def to_traditional(simple):
        """
        简体转化为繁体
        1. 如果字符为空，直接返回
        2. 字符长度为1，返回对应繁体字符
        3. 对应长度大于1，返回对应繁体词组
        :param simple: 简体单词/单个词组
        :return: 对应的繁体信息
        """
        new_dict = Dict()
        if len(simple) == 1:
            return new_dict.stc(simple)
        else:
            return new_dict.stp(simple)
