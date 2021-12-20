# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/19 20:15
@Auth ： 张顺
@No   : 021321712238
@File ：test.json.py
@IDE ：PyCharm

"""
import json
import os
import random
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st


def getFileOrDirPath(name):
    return os.path.join(os.path.dirname(__file__), name)


@st.cache
def readJsonJw(count='1'):
    # for item in os.listdir(getFileOrDirPath("jw")):
    choice_selectbox = {0: 'A',1: 'B', 2 :'C', 3: 'D' }
    s = {}
    url = "https://cdn.jsdelivr.net/gh/shunleite/jdsSearch@main/jw/" + ("work" if random.randint(0,1)==0 else "exam") + count + ".json"
    u = urlopen(url)
    s = json.loads(u.read().decode('utf-8'))
    random.shuffle(s.get("data", {}).get("questions", []))
    for item in s.get("data",{}).get("questions",[]):
        # print(BeautifulSoup(item.get("question"),'lxml').text)
        if item.get("type_text") == '单选题':
            realAnwser = item.get('options')[item.get('answer')[0]]
            temp = list(item.get('options').values())
            random.shuffle(temp)
            item.get('answer').pop()
            item.get('answer').append(choice_selectbox[temp.index(realAnwser)])
            for i in choice_selectbox.keys():
                item.get('options')[choice_selectbox[i]] = temp[i]
    return s


def generateQuestion(data: dict, num=1, place=None):
    # print(num + 1)
    if num < 1:
        num = 1
    i = 1
    for item in data.get("data", {}).get("questions", []):
        if i == num:
            with st.form(key='form' + str(i)):
                st.write(item.get("question"), unsafe_allow_html=True)
                slider_val = st.slider("题")
                checkbox_val = st.checkbox("A选项")

                # Every form must have a submit button.
                submitted = st.form_submit_button("提交")
                if submitted:
                    st.write("slider", slider_val, "checkbox", checkbox_val)
            break
        i = i + 1
    answerTip = True

    if answerTip:
        st.success('恭喜你答对了')
    st.empty()


@st.cache
def getPdfText(path:str) -> list:
    text = []
    if not os.path.exists(path):
        return text
    with open(path, "r+", encoding="utf-8") as f:
        text = f.readlines()
    return text

def pdfAnswers(path:str,searchStr:str) -> list:
    text = getPdfText(path)
    if not searchStr:
        return []
    searchStr = searchStr.split()
    searTable = []
    for line in text:
        if all(i in line for i in searchStr):
            searTable.append(line.strip())
    return searTable

@st.cache
def getPdfTxtDict(name):
    dicts = {'计算机网络':['计算机网络（第7版）','计算机网络谢希仁第七版配套课后答案'],'近代史':[]}
    return dicts.get(name,[])


if __name__ == "__main__":
    st.set_page_config(page_title='刷题系统单页', menu_items={
        'Report a bug': "http://10.102.4.220:8033",
        'About': "# 测试项目,近代史答案"
    })
    if 'pageNum' not in st.session_state:
        st.session_state['pageNum'] = 1
    if 'answerStatus' not in st.session_state:
        st.session_state['answerStatus'] = 3
    if 'reviewContent' not in st.session_state:
        st.session_state['reviewContent'] = {'content': '计算机网络', 'chapter': 0,'searchStatus':False}
    if not st.session_state['reviewContent'].get('choiceTxt'):
        st.session_state['reviewContent']['choiceTxt'] =  getPdfTxtDict(st.session_state['reviewContent']['content'])
    # print("能正确输出：",st.session_state['reviewContent'])

    st.sidebar.title("刷题测试单页")
    choice_selectbox = st.sidebar.selectbox(
        "请选择要复习的内容",
        ("计算机网络", "近代史")
    )
    st.session_state['reviewContent']['content'] = choice_selectbox
    if choice_selectbox == "计算机网络":
        add_selectbox = st.sidebar.selectbox(
            "请选择复习的章节",
            ("第{0}章".format(i) for i in range(1, 10)),index=st.session_state['reviewContent']['chapter']
        )
    nowChapter = ''.join(filter(str.isdigit, add_selectbox))
    data = readJsonJw(count=nowChapter)
    if st.session_state['reviewContent']['chapter'] != int(nowChapter) - 1:
        st.session_state['pageNum'] = 1
        st.session_state['reviewContent']['chapter'] = int(nowChapter) - 1
    nowTotal = len(data.get("data", {}).get("questions", []))
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('上一题'):
            st.session_state['pageNum'] -= 1
            if st.session_state['pageNum'] < 1:
                st.session_state['pageNum'] = 1
            st.session_state['answerStatus'] = 3
            st.session_state['reviewContent']['searchStatus'] = False
    with col3:
        if st.button('下一题', key='next'):
            st.session_state['pageNum'] += 1
            if st.session_state['pageNum'] > nowTotal:
                st.session_state['pageNum'] = nowTotal
            st.session_state['answerStatus'] = 3
            st.session_state['reviewContent']['searchStatus']  = False
    with col2:
        st.write(nowTotal, ":", st.session_state['pageNum'])
        # if st.button('提交', key='commit'):
        #     st.session_state['answerStatus'] = True

    submit = False
    i = 1
    for item in data.get("data", {}).get("questions", []):
        if i == st.session_state['pageNum']:
            answer = None
            with st.form(key='form' + str(i)):
                if item.get("type_text") == '判断题':
                    genre = st.radio(
                        # st.write(item.get("question"),unsafe_allow_html=True),
                        BeautifulSoup(item.get("question"), "lxml").text,
                        tuple(
                            ('√' if key == 'A' else '×') + ". " + value for key, value in item.get("options").items()),
                    )
                    if genre[0] == '√':
                        answer = 'A'
                    else:
                        answer = 'B'
                else:
                    genre = st.radio(
                        # st.write(item.get("question"),unsafe_allow_html=True),
                        BeautifulSoup(item.get("question"), "lxml").text,
                        tuple(key + ". " + BeautifulSoup(value, 'lxml').text for key, value in
                              item.get("options").items()),
                    )
                    answer = genre[0]
                # # Every form must have a submit button.
                submitted = st.form_submit_button("提交")
                if submitted:
                    submit = True
            if answer == item.get('answer')[0]:
                st.session_state['answerStatus'] = 1
            else:
                if answer and submit:
                    st.session_state['answerStatus'] = 0
            break
        i = i + 1
    # print("内容:", st.session_state['answerStatus'])
    if st.session_state['answerStatus'] == 1 and (submit or st.session_state['reviewContent']['searchStatus']):
        st.success("答案正确")
    elif st.session_state['answerStatus'] == 0 and (submit or st.session_state['reviewContent']['searchStatus']):
        st.error("答案错误")
    isClick = False
    searchContent = ''
    # with st.empty():
    #     st.write(f"⏳ ")
    def changeStatusSearch():
        st.session_state['reviewContent']['searchStatus'] = False

    col4,col5 = st.columns(2)

    with col4:
        searchContent = st.text_input(label=f"⏳ Search ^v^~",value='IP 协议',help="查询字符串之间使用\"空格\"可以过滤查询到的数据", on_change=changeStatusSearch)

    with col5:
        st.write('   ‍')

        if st.button('Search'):
            isClick = True
            st.session_state['reviewContent']['searchStatus'] = True
        st.text(' ')

    if isClick or st.session_state['reviewContent']['searchStatus']:
        options = st.multiselect(
            '请选择要参考的PDF',
            ['计算机网络（第7版）', '计算机网络谢希仁第七版配套课后答案'],
            st.session_state['reviewContent']['choiceTxt'])

        # st.write('You selected:', options)
        st.session_state['reviewContent']['choiceTxt'] = options
        for searchC in options:
            # print(searchC, getFileOrDirPath("txt/" + searchC + ".txt"))
            searchResult = pdfAnswers(getFileOrDirPath("txt/" + searchC + ".txt"), searchContent)
            # searchResult
            st.warning(searchC)
            st.table(pd.DataFrame({
                '待选答案':searchResult
            }))