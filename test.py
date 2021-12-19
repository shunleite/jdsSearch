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

from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def getFileOrDirPath(name):
    return os.path.join(os.path.dirname(__file__), name)

@st.cache
def readJsonJw(count='1'):
    # for item in os.listdir(getFileOrDirPath("jw")):
    s={}
    with open(getFileOrDirPath("jw/work" + count + ".json"),"r+",encoding='utf-8') as f:
        s = json.load(f)
        random.shuffle(s.get("data", {}).get("questions", []))
    # for item in s.get("data",{}).get("questions",[]):
    #     print(BeautifulSoup(item.get("question"),'lxml').text)
    # os.getcwd()
    return s


def generateQuestion(data:dict, num=1,place=None):
    print(num+1)
    if num < 1:
        num = 1
    i = 1
    for item in data.get("data",{}).get("questions",[]):
        if i == num:
            print('form' + str(i))
            with st.form(key='form' + str(i)):
                st.write(item.get("question"),unsafe_allow_html=True)
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




if __name__ == "__main__":
    st.set_page_config(page_title='刷题系统单页', menu_items={
        'Report a bug': "http://10.102.4.220:8033",
        'About': "# 测试项目,近代史答案"
    })
    st.sidebar.title("刷题测试单页")
    choice_selectbox = st.sidebar.selectbox(
        "请选择要复习的内容",
        ("计算机网络", "近代史")
    )
    if choice_selectbox == "计算机网络":
        add_selectbox = st.sidebar.selectbox(
            "请选择复习的章节",
            ("第{0}章".format(i) for i in range(1,10))
        )
    data=readJsonJw(count=''.join(filter(str.isdigit,add_selectbox)))
    if 'pageNum' not in st.session_state:
        st.session_state['pageNum'] = 1
    if 'answerStatus' not in st.session_state:
        st.session_state['answerStatus'] = 3
    nowTotal = len(data.get("data",{}).get("questions",[]))
    col1,col2, col3 = st.columns(3)
    with col1:
        if st.button('上一题'):
            st.session_state['pageNum'] -= 1
            if st.session_state['pageNum'] < 1:
                st.session_state['pageNum'] = 1
            st.session_state['answerStatus'] = 3
    with col3:
        if st.button('下一题', key='next'):
            st.session_state['pageNum'] += 1
            if st.session_state['pageNum'] > nowTotal:
                st.session_state['pageNum'] = nowTotal
            st.session_state['answerStatus'] = 3
    with col2:
        st.write(nowTotal,":",st.session_state['pageNum'])
        # if st.button('提交', key='commit'):
        #     st.session_state['answerStatus'] = True

    submit = False
    i = 1
    for item in data.get("data",{}).get("questions",[]):
        if i == st.session_state['pageNum']:
            print('form' + str(i))
            answer = None
            with st.form(key='form' + str(i)):
                if item.get("type_text")=='判断题':
                    genre = st.radio(
                        # st.write(item.get("question"),unsafe_allow_html=True),
                        BeautifulSoup(item.get("question"), "lxml").text,
                        tuple(('√' if key=='A' else '×') + ". " + value for key, value in item.get("options").items()),
                    )
                    if genre[0] == '√':
                        answer = 'A'
                    else:
                        answer = 'B'
                else:
                    genre = st.radio(
                        # st.write(item.get("question"),unsafe_allow_html=True),
                        BeautifulSoup(item.get("question"), "lxml").text,
                        tuple(key + ". " + BeautifulSoup(value,'lxml').text for key, value in item.get("options").items()),
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
    print("内容:", st.session_state['answerStatus'])
    if st.session_state['answerStatus'] == 1 and submit:
        st.success("答案正确")
    elif st.session_state['answerStatus'] == 0 and submit:
        st.error("答案错误")
