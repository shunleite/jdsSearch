# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/20 15:09
@Auth ： 张顺
@No   : 021321712238
@File ：pdfReader.py
@IDE ：PyCharm

"""
import json
import os
import re

from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage


def parse(pdf_path, result_path):
    # 获取pdf文档
    fp = open(pdf_path, 'rb')

    # 创建一个与文档相关的解释器
    parser = PDFParser(fp)

    # pdf文档的对象，与解释器连接起来
    doc = PDFDocument(parser=parser)
    parser.set_document(doc=doc)

    # 如果是加密pdf，则输入密码
    # doc._initialize_password()

    # 创建pdf资源管理器
    resource = PDFResourceManager()

    # 参数分析器
    laparam = LAParams()

    # 创建一个聚合器
    device = PDFPageAggregator(resource, laparams=laparam)

    # 创建pdf页面解释器
    interpreter = PDFPageInterpreter(resource, device)

    # 获取页面的集合
    for page in PDFPage.get_pages(fp):
        # 使用页面解释器来读取
        interpreter.process_page(page)

        # 使用聚合器来获取内容
        layout = device.get_result()
        for out in layout:
            if isinstance(out, LTFigure):
                pass
                # for out2 in out:
                #     if hasattr(out2, 'get_text'):
                #         print(out2.get_text())
                #
                #         # 写入txt文件
                #         fw = open(result_path, 'a', encoding="utf-8")
                #         fw.write(out2.get_text())

            else:
                if hasattr(out, 'get_text'):
                    print(out.get_text())

                    # 写入txt文件
                    fw = open(result_path, 'a', encoding="utf-8")
                    fw.write(out.get_text())

def getFileOrDirPath(name):
    return os.path.join(os.path.dirname(__file__), name)

def getFileList(path):
    return os.listdir(getFileOrDirPath(path))

def getQuersionDict():
    questionDict = {}
    for i in getFileList("jw"):
        sjson = ''
        with open(getFileOrDirPath("jw/" + i), mode="r", encoding="utf-8") as f:
            temp = json.load(f)
            questionDict[i.split('.')[0]] = temp['data']['questions']
    #      = json.loads(sjson)
    with open(getFileOrDirPath("data/jw.json"), "w+", encoding="utf-8") as fp:
        json.dump(questionDict, fp,ensure_ascii=False)
# def search

if __name__ == '__main__':
    s = getQuersionDict()
    print(s)
    # pdf_path = os.path.join(os.path.dirname(__file__), 'txt/计算机网络谢希仁第七版配套课后答案.pdf')
    # result_path = os.path.join(os.path.dirname(__file__), 'txt/计算机网络谢希仁第七版配套课后答案.txt')
    #
    # parse(pdf_path,result_path)


    # text = []
    # with open(r"txt/计算机网络（第7版）.txt", "r+", encoding="utf-8") as f:
    #     text = f.readlines()
    # searchStr = "RIP 使用".split()
    # searTable = []
    # for line in text:
    #     if all(i in line for i in searchStr):
    #         searTable.append(line.strip())
    # print(searTable)




