#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .tools.Homophone import Homophone
from .tools.Ner import Ner
from .tools.Random_delete_char import RandomDeleteChar
from .tools.Random_word import Randomword
from .tools.Similar_word import Similarword
from .tools.Char_position_exchange import CharPositionExchange
from .tools.Translate import baidu_translate
from .tools.Equivalent_char import EquivalentChar

__author__ = 'Jiang.XinFa'

__all__ = ["Homophone", "Ner", "RandomDeleteChar", "Randomword", "Similarword", "CharPositionExchange",
           "baidu_translate", "EquivalentChar"]
