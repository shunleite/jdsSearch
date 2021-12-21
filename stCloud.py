# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/19 18:30
@Auth ： 张顺
@No   : 021321712238
@File ：stCloud.py
@IDE ：PyCharm

"""
from urllib.request import urlopen

import pandas as pd
import streamlit as st
import json
import re
import os


@st.experimental_singleton
def readJson():
    u = urlopen("https://cdn.jsdelivr.net/gh/shunleite/jdsSearch@main/now.json")
    tiku = json.loads(u.read().decode('utf-8'))
    return tiku

def searchContent(data={}, choice=None,content=None):
    if not data and not choice and not content:
        return [],[]
    questions = []
    answers = []
    for k,v in data.get(choice,{}).items():
        if content in k:
            questions.append(k)
            answers.append(v)
    return questions,answers

def jdsMain():
    tiku = readJson()
    option = st.selectbox(
        '请选择题模式',
        ('单选题', '多选题'))
    content = st.text_input('问题', '运动')
    st.success("查询成功！")
    questions,answers = searchContent(data=tiku,choice=option, content=content)
    st.table(pd.DataFrame({
        '问题': questions,
        '答案': answers
    }))
if __name__ == "__main__":
    st.set_page_config(page_title='近代史答案Search', menu_items={
        'Report a bug': "http://10.102.4.220:8033",
        'About': "# 测试项目,近代史答案"
    })
    jdsMain()

