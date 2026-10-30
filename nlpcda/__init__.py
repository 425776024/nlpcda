#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ._version import __version__
from .tools.Char_position_exchange import CharPositionExchange
from .tools.Equivalent_char import EquivalentChar
from .tools.Homophone import Homophone
from .tools.Ner import Ner
from .tools.Random_delete_char import RandomDeleteChar
from .tools.Random_word import Randomword
from .tools.Simbert import Simbert
from .tools.Similar_word import Similarword
from .tools.Translate import baidu_translate

__author__ = "Jiang.XinFa"

__all__ = [
    "Homophone",
    "Ner",
    "RandomDeleteChar",
    "Randomword",
    "Similarword",
    "CharPositionExchange",
    "baidu_translate",
    "EquivalentChar",
    "Simbert",
    "__version__",
]
