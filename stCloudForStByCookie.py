# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/19 20:15
@Auth ： 张顺
@No   : 021321712238
@File ：test.json.py
@IDE ：PyCharm

"""
import base64
import datetime
import json
import os
import random
import time
from urllib.request import urlopen

from bs4 import BeautifulSoup
import pandas as pd
import extra_streamlit_components as stx
import streamlit as st

from stCloud import jdsMain
from tools.utils import searchAnswer
st.set_page_config(page_title='刷题系统单页', menu_items={
        'Report a bug': "http://wpa.qq.com/msgrd?v=3&uin=83118937&site=qq&menu=yes",
        'About': "# 测试项目,近代史答案"
    })
@st.cache(allow_output_mutation=True)
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

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
            line = line.replace(">"," > ")
            line = line.replace("<"," < ")
            for name in searchStr:
                line = line.replace(name,
                             "<div style=\"background-color: rgba(0, 135, 107, 0.2); padding: 1px 6px; margin: 0px 5px; display: inline; vertical-align: middle; border-radius: 3px; font-size: 0.75rem; font-weight: 400;\">" +
                             name + "</div>")
            searTable.append(line.strip())
    return searTable

@st.cache
def getPdfTxtDict(name):
    dicts = {'计算机网络':['计算机网络第8版课件', '计算机网络（第7版）','计算机网络谢希仁第七版配套课后答案'],'近代史':[]}
    return dicts.get(name,[])

@st.cache
def getAllAnswerContent() -> dict:
    content = {}
    with open(getFileOrDirPath("data/jw.json"), "r", encoding="utf-8") as f:
        content = json.load(f)
    for k in content:
        for item in content[k]:
            item['question'] = BeautifulSoup(item['question'], 'lxml').text.strip()
    return content

def getAnswer(name):
    content = getAllAnswerContent()
    questions = []
    answers = []
    for k in content:
        for item in content[k]:
            if name in item['question']:
                answer = BeautifulSoup(item['options'][item['answer'][0]], 'lxml').text.strip()
                questions.append(item['question'])
                answers.append(answer)
    return questions, answers


def set_cookie_dict(cookie:str, val:dict):
    cookie_manager.set(cookie, val)


def get_cookie_dict(cookie:str)->dict:
    return cookie_manager.get(cookie)


def get_cookie(cookie:str):
    return cookie_manager.get(cookie)

def set_cookie(cookie:str,val):
    cookie_manager.set(cookie,val)



if __name__ == "__main__":
    temp = None
    cookies = cookie_manager.get_all()
    if cookies:
        if cookies.get("ajs_anonymous_id"):
            temp = cookies.get("reviewContent" + cookies.get("ajs_anonymous_id"))
        # cookie_manager.delete("reviewContent")
        # st.write(cookies)
        if not temp:
            temp = {}
        if not temp.get('searchStatus'):
            temp['searchStatus'] = False
        if not temp.get('chapter'):
            temp['chapter'] = 0
        if not temp.get('content'):
            temp['content'] = '计算机网络'
        if not temp.get('pageNum'):
            temp['pageNum'] = 1
        if not temp.get('answerStatus'):
            temp['answerStatus']= 3
        if not temp.get('choiceTxt') and temp.get('content'):
            temp['choiceTxt'] =  getPdfTxtDict(temp['content'])

        st.sidebar.info(r"""
        🎈 **NEW:** 刷題单页
        >[Report a bug](http://wpa.qq.com/msgrd?v=3&uin=83118937&site=qq&menu=yes)
        """)
        choice_selectbox = st.sidebar.selectbox(
            "请选择要复习的内容",
            ("计算机网络", "近代史"),index=["计算机网络", "近代史"].index(temp['content']) if temp['content'] else 0
        )
        choice_mode = st.sidebar.selectbox(
            "请选择模式",
            ("刷题模式", "搜题模式")
        )
        if choice_mode == "刷题模式":
            if choice_selectbox == "计算机网络":
                add_selectbox = st.sidebar.selectbox(
                    "请选择复习的章节",
                    ("第{0}章".format(i) for i in range(1, 10)),index=temp['chapter']
                )
                st.sidebar.write('')
                # st.sidebar.write(st.session_state)
                st.sidebar.write('')
                st.sidebar.write('')
                st.sidebar.button("確定")
                nowChapter = ''.join(filter(str.isdigit, add_selectbox))
                data = readJsonJw(count=nowChapter)
                if temp['chapter'] != int(nowChapter) - 1:
                    temp['pageNum'] = 1
                    temp['chapter'] = int(nowChapter) - 1
                    temp['searchStatus'] = False
                nowTotal = len(data.get("data", {}).get("questions", []))
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button('上一题'):
                        temp['pageNum'] = temp['pageNum'] -1
                        if temp['pageNum'] < 1:
                            temp['pageNum'] = 1
                        temp['answerStatus'] = 3
                        temp['searchStatus'] = False
                with col3:
                    if st.button('下一题', key='next'):
                        print("数字是：",temp['pageNum'], type(temp['pageNum']))
                        temp['pageNum'] = temp['pageNum'] + 1
                        if temp['pageNum'] > nowTotal:
                            temp['pageNum'] =  nowTotal
                        temp['answerStatus'] = 3
                        temp['searchStatus'] = False
                with col2:
                    st.write(nowTotal, ":", temp['pageNum'])
                    # if st.button('提交', key='commit'):
                    #     st.session_state['answerStatus'] = True

                submit = False
                i = 1
                for item in data.get("data", {}).get("questions", []):
                    if i == temp['pageNum']:
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
                            temp['answerStatus'] = 1
                        else:
                            if answer and submit:
                                temp['answerStatus'] = 0
                        break
                    i = i + 1
                # print("内容:", st.session_state['answerStatus'])
                if temp['answerStatus'] == 1 and (submit or temp['searchStatus']):
                    st.success("答案正确")
                elif temp['answerStatus'] == 0 and (submit or temp['searchStatus']):
                    st.error("答案错误")
                isClick = False
                searchContent = ''
                # with st.empty():
                #     st.write(f"⏳ ")
                def changeStatusSearch():
                    temp['searchStatus'] = False

                col4,col5 = st.columns(2)

                with col4:
                    searchContent = st.text_input(label=f"⏳ Search ^v^~",value='IP 协议',help="查询字符串之间使用\"空格\"可以过滤查询到的数据", on_change=changeStatusSearch)

                with col5:
                    st.write('   ‍')

                    if st.button('Search'):
                        isClick = True
                        temp['searchStatus'] = True
                    st.text(' ')

                if isClick or temp['searchStatus']:
                    options = st.multiselect(
                        '请选择要参考的PDF',
                        ['计算机网络第8版课件', '计算机网络（第7版）', '计算机网络谢希仁第七版配套课后答案'],
                        temp['choiceTxt'])

                    # st.write('You selected:', options)
                    temp['choiceTxt'] = options
                    for searchC in options:
                        # print(searchC, getFileOrDirPath("txt/" + searchC + ".txt"))
                        searchResult = pdfAnswers(getFileOrDirPath("txt/" + searchC + ".txt"), searchContent)
                        # searchResult
                        st.warning(searchC)
                        # st.table(pd.DataFrame({
                        #     '待选答案':searchResult
                        # }))
                        content = """"""
                        for num, line in enumerate(searchResult,start=1):
                            content += """<tr><td>"""  + str(num) + """</td><td>""" + line + """</td></tr>"""
                        st.markdown("""
                                    <table>
                                <tr>
                                    <th></th>
                                    <th>待选答案</th>
                                </tr>
                                """ + content + """
                            </table>
                            """, unsafe_allow_html=True)
                        st.write("")
            elif choice_selectbox == '近代史':
                st.markdown(f"""
            <div style="display:flex;justify-content:space-between;background:rgb(0,0,0,0);padding:10px;border-radius:5px;margin:10px;">
                <span></span>
                <span></span>
                <div style="float:right;width:30%;background:rgb(0,0,0,0);padding:10px;border-radius:5px;margin:10px;">
                    <h3 style="color:white;letter-spacing:1px;line-height: 1.6;font-family:Arial, Helvetica, sans-serif;">
                        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
                        <br><br>
                    </h3>
                    <h1 style="color: #2980b9;letter-spacing:1px;line-height: 1.6;font-family:Arial, Helvetica, sans-serif;">404</h1>
                </div>
                <div style="float:left;width:50%;background:rgb(0,0,0,0);padding:10px;border-radius:5px;margin:10px;">
                    <img style="max-height:100%;max-width:100%;" src="data:image/png;base64,{base64.b64encode(open("images/ML-removebg.png", "rb").read()).decode()}">
                </div>
            </div>
    """,unsafe_allow_html=True)
        elif choice_mode == '搜题模式':
            # st.markdown('🔎 请搜索题目 / Search~🌈')
            if choice_selectbox == '计算机网络':
                answer = st.text_input(label='🔎 请搜索题目 / Search~🌈', value='RIP')
                choice_type = st.selectbox(
                    "请选择搜题模式",
                    ("本地模式", "第三方云搜"),help="第三方云搜题支持分词搜索（所以问题关键词要尽量写全）"
                )
                questions, answers = [], []
                if choice_type == '本地模式':
                    questions, answers = getAnswer(answer)
                elif choice_type == '第三方云搜':
                    questions, answers = searchAnswer(answer)
                if questions and answers:
                    st.success("查询成功! ")
                else:
                    st.error("查询失败! ")
                    st.info("可以使用第三方云搜试试~")
                st.table(pd.DataFrame({
                    "题目": questions,
                    "答案": answers,
                }))
            elif choice_selectbox == '近代史':
                jdsMain()
        set_cookie_dict("reviewContent" + cookies.get("ajs_anonymous_id"),temp)