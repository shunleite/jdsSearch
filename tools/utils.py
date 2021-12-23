# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/23 16:15
@Auth ： 张顺
@No   : 021321712238
@File ：ProxyContent.py
@IDE ：PyCharm

"""
import json
import random
from concurrent import futures
import requests
from urllib.parse import quote
from faker import Faker
def getProxys() -> list:
    proxys = []
    urls = ["http://pro.shunleite.com"]
    url = random.choice(urls)

    payload = {}
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload,timeout=5)
        s = json.loads(response.content)
        for item in s:
            if item.get("proxy"):
                proxys.append(item.get("proxy"))
    except Exception as e:
        pass
    return proxys
def searchAnswer(question,useProxy=False):
    if not isinstance(question, str):
        return [],[]
    question = question.split()
    questionStr = ''
    for i in question:
        questionStr += quote(i) + "&"
    url = "http://imnu.52king.cn/api/wk/index.php?c=" + questionStr
    proxies = {}
    if useProxy:
        proxys = getProxys()
        if proxys:
            proxy = random.choice(proxys)
            proxies = {"http": "http://" + proxy, "https": "http://" + proxy}
        print("代理是:", proxies)
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en,en-US;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        'User-Agent': Faker().chrome()

    }
    try:
        response = requests.request("GET", url, headers=headers, proxies=proxies,timeout=5)
        print(response.text,url)
        tempDict = json.loads(response.text.strip().replace("\n",""))
        if not tempDict.get("title"):
            if not useProxy:
                searchAnswer(question, useProxy=True)
            return ["查找失败请重新尝试"], ["查找失败请重新尝试"]
        return [tempDict.get("title").strip()], [tempDict.get("answer", "答案获取失败").strip()]
    except IndexError as e:
        if not useProxy:
            searchAnswer(question, useProxy=True)
        return ["查找失败请重新尝试"], ["查找失败请重新尝试"]

if __name__ == "__main__":
    print(searchAnswer('近代史'))
