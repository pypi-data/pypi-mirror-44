# coding=utf-8
# opencc_const.py 单元测试
# 2019.04.10 create by binbin.hou
from openccpy import opencc_const as const


class TestOpenccConst(object):
    """
    测试类
    """

    def test_const(self):
        """
        测试常量
        :return:
        """
        assert "UTF-8" == const.DEFAULT_CHARSET
        assert "\uD86D\uDDF5" == const.EMPTY_RESULT
        assert const.ST_CHAR_PATH == "/db/STCharacters.txt"
        assert const.ST_PHRASE_PATH == "/db/STPhrases.txt"
        assert const.TS_CHAR_PATH == "/db/TSCharacters.txt"
        assert const.TS_PHRASE_PATH == "/db/TSPhrases.txt"
