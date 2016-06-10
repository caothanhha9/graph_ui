# -*- coding: utf-8 -*-
import unicodedata


ENCODE_TYPE = 'utf-8'

""" Static functions for processing utf-8 string or unicode"""


def str_normalize(string):
    """
    This function normalize unicode, standard NFC
    :param string: unicode input to be normalized
    :return: normalized unicode
    """
    if isinstance(string, unicode):
        string = unicodedata.normalize('NFC', string)
    return string


def str_encode(string):
    """
    This function encode unicode to str type UTF-8
    :param string: unicode input to be encoded
    :return: encoded str
    """
    string = str_normalize(string)
    if isinstance(string, unicode):
        string = string.encode(encoding=ENCODE_TYPE)
    return string


def str_decode(string):
    """
    This function decode str type UTF-8 to UNICODE
    :param string: str input to be decoded
    :return: unicode
    """
    if isinstance(string, str):
        string = string.decode(encoding=ENCODE_TYPE)
    string = str_normalize(string)
    return string


