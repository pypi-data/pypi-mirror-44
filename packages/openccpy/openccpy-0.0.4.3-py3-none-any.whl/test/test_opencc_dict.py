# coding=utf-8
# opencc_const.py 单元测试
# 2019.04.10 create by binbin.hou
from openccpy.opencc_dict import *


class TestOpenccDict(object):
    """
    测试类
    """

    def test_stc(self):
        """
        测试简体转繁体字符的正确性
        :return:
        """
        stc_dict = Dict()
        assert "絲" == stc_dict.stc("丝")

    def test_tsc(self):
        """
        测试繁体转简体字符的正确性
        :return:
        """
        stc_dict = Dict()
        assert "丝" == stc_dict.tsc("絲")

    def test_stc_key_not_exists(self):
        """
        测试简体转繁体字符的正确性-Key 不存在
        :return:
        """
        stc_dict = Dict()
        assert "历练" == stc_dict.stc("历练")

    def test_tsc_key_not_exists(self):
        """
        测试繁体转简体字符的正确性-Key 不存在
        :return:
        """
        stc_dict = Dict()
        assert "历练" == stc_dict.stc("历练")

    def test_stp(self):
        """
        测试简体转繁体词组的正确性
        :return:
        """
        stc_dict = Dict()
        assert "一絲不掛" == stc_dict.stp("一丝不挂")

    def test_tsp(self):
        """
        测试繁体转简体词组的正确性
        :return:
        """
        stc_dict = Dict()
        assert "一目了然" == stc_dict.tsp("一目瞭然")

    def test_stp_key_not_exits(self):
        """
        测试简体转繁体词组的正确性-Key 不存在
        :return:
        """
        stc_dict = Dict()
        assert "对" == stc_dict.stp("对")

    def test_tsp_key_not_exits(self):
        """
        测试繁体转简体词组的正确性-Key 不存在
        :return:
        """
        stc_dict = Dict()
        assert "对" == stc_dict.stp("对")