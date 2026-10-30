#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xinfa.jiang
# @File    : Translate.

import hashlib
import random

import requests


# 百度翻译方法
def baidu_translate(content, appid, secretKey, t_from="en", t_to="zh", timeout=10):
    if len(content) > 4891:
        return "输入请不要超过4891个字符！"
    salt = str(random.SystemRandom().randint(0, 2**32 - 1))
    # 申请网站 http://api.fanyi.baidu.com/api/trans
    sign = appid + content + salt + secretKey
    sign = hashlib.md5(sign.encode(encoding="UTF-8")).hexdigest()
    head = {
        "q": f"{content}",
        "from": t_from,
        "to": t_to,
        "appid": f"{appid}",
        "salt": f"{salt}",
        "sign": f"{sign}",
    }
    response = requests.get(
        "https://api.fanyi.baidu.com/api/trans/vip/translate", params=head, timeout=timeout
    )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise RuntimeError("Baidu translation returned an invalid response")
    if "error_code" in data:
        raise RuntimeError(
            "Baidu translation error %s: %s"
            % (data["error_code"], data.get("error_msg", "unknown error"))
        )
    results = data.get("trans_result")
    if (
        not isinstance(results, list)
        or not results
        or any(
            not isinstance(item, dict) or not isinstance(item.get("dst"), str) for item in results
        )
    ):
        raise RuntimeError("Baidu translation returned an invalid response")
    return "\n".join(item["dst"] for item in results)


def test():
    a = "Free translation for each platform"
    s = baidu_translate(a, appid="xxx", secretKey="xxx")
    print(s)
