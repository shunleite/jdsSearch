import os

import pandas as pd
import streamlit as st
import json
import re

tiku = {}

def getFile(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def saveJson():
    with open(getFile("now.txt"), 'r',encoding="utf-8") as f:
        for item in f.readlines():
            if not tiku.get(re.search(r"\((.*?)\)",item).group(1)):
                tiku[re.search(r"\((.*?)\)",item).group(1)] = {}
            tiku[re.search(r"\((.*?)\)",item).group(1)][re.search(r"\)\s(.*?)\s正确答案",item).group(1)] = re.search(r"(正确答案.*)",item).group(1)
    with open("now.json", "w+",encoding="utf-8") as f:
        f.write(json.dumps(tiku,ensure_ascii=False))
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
@st.experimental_singleton
def readJson():
    tiku = {}
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "now.json")):
        saveJson()
    with open(getFile("now.json"), "r+", encoding="utf-8") as f:
        tiku = json.load(f)
    return tiku

st.set_page_config(page_title='近代史答案Search', menu_items={
    'Report a bug': "http://10.102.4.220:8033",
    'About': "# 测试项目,近代史答案"
})

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



