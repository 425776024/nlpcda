NLP Chinese Data Augmentation / 一键中文数据增强工具
~~~~~~~~~~~~~~~~~~~~~~~~

API
---

随机【（等价）实体】替换
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from nlpcda.tools.randomword import Randomword

    test_str = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    smw = Randomword(create_num=3, change_rate=0.3)
    rs1 = smw.replace(test_str)

    print('随机实体替换>>>>>>')
    for s in rs1:
        print(s)
    '''
    随机实体替换>>>>>>
    这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    这个中国通信服务很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    这个瑞丰光电很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    '''

随机同义词替换
~~~~~~~~~~~~~~

.. code:: python

    from nlpcda.tools.similarword import Similarword

    test_str = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    smw = Similarword(create_num=3, change_rate=0.3)
    rs1 = smw.replace(test_str)

    print('随机同义词替换>>>>>>')
    for s in rs1:
        print(s)

    '''
    随机同义词替换>>>>>>
    这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    这天大药业很毋庸置疑啊，测试测试。这是一场疫情失控的鸦片战争、总体战、阻击战，习近平总书记亲指挥、亲自布置。筹措 指挥若定辄把人民群众生命安全和身体健康放在第一位
    这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自布。运筹帷幄 指挥若定尽把人民群众生命安全和身体健康放在第一位
    '''

随机近义字替换
~~~~~~~~~~~~~~

.. code:: python

    from nlpcda.tools.homophone import Homophone

    test_str = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    smw = Homophone(create_num=3, change_rate=0.3)
    rs1 = smw.replace(test_str)

    print('随机近义字替换>>>>>>')
    for s in rs1:
        print(s)

    '''
    随机近义字替换>>>>>>
    这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    籷个兲大药业很部错啊，测试测視。这駛义场幆情防控的人民战争、总体战、阻击战，习埐平总輸记亲自指挥、亲胔部署。运筹帷仴 指挥若定始终把靱民群众生命安全和身体健钪放在第一蝛
    这个天大药业很不错啊，测试萴试。这蒔一鱨疫情防悾的人民榐争、总蹄战、阻击詹，吸近平昮鄃羈吢嗞指挥、懃自瓿署。运筹骩幄 憄挥若椗匙终把人民群众生命安牷和身体監康放在第一位
    '''

随机字删除
~~~~~~~~~~

.. code:: python

    from nlpcda.tools.randomdeletechar import RandomDeleteChar

    test_str = '''这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    smw = RandomDeleteChar(create_num=3, change_rate=0.3)
    rs1 = smw.replace(test_str)

    print('随机字删除>>>>>>')
    for s in rs1:
        print(s)

    '''
    随机字删除>>>>>>
    这个天大药业很不错啊，测试测试。这是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位
    这个天大药业不错啊，测试测试这是一场疫情防控人民战争总体战、阻击战，习近平总书记亲自指挥亲自部署运筹帷幄 指挥若定始终人民群众生命安全和身体健康放在
    这个天大药业不错，测试测试这是一场疫情防控的人民战争、总体战阻击战习近平总书记亲自指挥、亲自部署。运筹帷幄指挥若定始终人民群众生命安全身体健康放在
    '''

添加自定义词典
~~~~~~~~~~~~~~

.. code:: python

    from nlpcda.tools.randomword import Randomword
    from nlpcda.tools.similarword import Similarword
    from nlpcda.tools.homophone import Homophone
    from nlpcda.tools.randomdeletechar import RandomDeleteChar

    Randomword.add_word('张杰')
    Randomword.add_words(['张杰','谢娜','马化腾','中国人民银行'])
    # Similarword，Homophone，RandomDeleteChar 同上

