#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import os
import sqlite3
# import importlib
# importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed



# 解析pdf 文本
def parse(path):


    text = ''
    fp = open(path, 'rb') # 以二进制读模式打开
    #用文件对象来创建一个pdf文档分析器
    praser = PDFParser(fp)
    # 创建一个PDF文档
    doc = PDFDocument()
    # 连接分析器 与文档对象
    praser.set_document(doc)
    doc.set_parser(praser)

    # 提供初始化密码
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf 资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # 创建一个PDF解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        for page in doc.get_pages(): # doc.get_pages() 获取page列表
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                        results = x.get_text()
                        text += results + '\n'
    return(text)                      

def re_order(text):    
    Order_Number = re.findall('[A-Z][0-9]{2}-[0-9]{6}', text)   #订单号
    Order_Date = re.findall('CHINA\n+([0-9]{2}-[A-Z][a-z]{2}-[0-9]{4})\n+PAGE', text)   #订单日期
    Product_Number = re.findall('[A-Z0-9]{15}', text)       #货号PN
    Product_Quantity = re.findall('([0-9,]+\.[0-9]{2})\s+[PCSET]', text)    #订单数量
    Product_Unitprice = re.findall('[0-9,]+\.[0-9]{6}', text)         #产品单价，总价由计算得出，再计算总价核对读取分析结果是否正确
    Product_ETADate = re.findall('([0-9]{2}-[A-Z][a-z]{2}-[0-9]{4})(?!\n+PAGE)', text)
    Grand_Total = re.findall('GRAND TOTAL\s+([0-9,]+\.\d{2})',text)  #总金额，用于核对

    amount = 0
    order = []

    for index in range(len(Product_Number)):    
        quantity = float(Product_Quantity[index].replace(',',''))
        price = float(Product_Unitprice[index].replace(',',''))
        order.append((Order_Number[0], Order_Date[0], Product_Number[index], quantity, price, Product_ETADate[index], quantity*price))
        amount += quantity*price  

    # for item in order:
    #     print(item)
    db_name = 'shanglin.db'
    insert_data(db_name,order)

    g_total = float(Grand_Total[0].replace(',',''))
    print('共计%d条记录' % (len(order)))
    print('计算总价：%.2f' % (amount))
    print('读取总价：%.2f' % (g_total))
    if round(amount,2) == g_total:
        print('核对正确，请放心保存！')
    else:
        print('核对错误，请检查！')

def file_name(path):   
    for root, dirs, files in os.walk(path):  
        # print(root) #当前目录路径  
        # print(dirs) #当前路径下所有子目录  
        return(files) #当前路径下所有非目录子文件  

def insert_data(db_name,data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print("Opened database successfully")
    print(data)

    sql = "INSERT INTO Orders (OrderNumber,OrderDate,ProductNumber,Quantity,UnitPrice,ETADate,Amount) \
              VALUES (?,?,?,?,?,?,?)"

    try:
        c.executemany(sql ,data)

                # OrderNumber     integer,
                # OrderDate       text,                
                # ProductNumber   text,
                # Quantity        integer,
                # UnitPrice       real,                
                # ETADate         text,
                # Amount          real,
                # Primary Key(ProductNumber)     

        conn.commit()
        print("Records created successfully")

    except BaseException as e:
        print("错误！",e)

    finally:
        conn.close()
        print("close conn")
    print("end")


if __name__ == '__main__':
    path = r'D:\code\python\pdf'
    file_names = file_name(path)
    for file in file_names:
        if re.search(r'.pdf',file) == None:
            print('跳过非pdf文件！')
        else:
            file = path + '\\' + file
            print(file)
            text = parse(file)
            re_order(text)


