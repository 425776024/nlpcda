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

try:
    from .tools.Simbert import Simbert

    no_simbert = False
except Exception as e:
    no_simbert = True
    print('Simbert将不能正常使用，除非你安装keras后端：tensorflow ....', e)
__author__ = 'Jiang.XinFa'

if no_simbert:
    __all__ = ["Homophone", "Ner", "RandomDeleteChar", "Randomword", "Similarword", "CharPositionExchange",
               "baidu_translate", "EquivalentChar"]
else:
    __all__ = ["Homophone", "Ner", "RandomDeleteChar", "Randomword", "Similarword", "CharPositionExchange",
               "baidu_translate", "EquivalentChar", "Simbert"]
