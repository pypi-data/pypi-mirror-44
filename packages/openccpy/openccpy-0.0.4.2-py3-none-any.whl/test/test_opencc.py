# coding=utf-8
# opencc_util.py 单元测试
# 2019.04.10 create by binbin.hou
from openccpy.opencc import *


class TestOpencc(object):
    """
    核心转换测试类
    """

    def test_to_simple(self):
        """
        测试转换为简体
        :return: 结果
        """
        assert "丝" == Opencc.to_simple("絲")
        assert "一目了然" == Opencc.to_simple("一目瞭然")

    def test_to_traditional(self):
        """
        测试转化为繁体
        :return:
        """
        assert "絲" == Opencc.to_traditional("丝")
        assert "一目瞭然" == Opencc.to_traditional("一目了然")
