import xlwings as xw
import sqlite3

# excel_file = r'test.xlsx'
# D:\code\python\excel\花园灯20130620.xls

# app=xw.App(visible=True,add_book=False)
# wb=app.books.open(excel_file)
# wb就是新建的工作簿(workbook)，下面则对wb的sheet1的A1单元格赋值
# for i in range(5):
#     gd = 'A' + str(i+1)
#     # print(gd)
#     insert_data = i
#     # print(insert_data)
#     wb.sheets['sheet1'].range(gd).value=insert_data

# wb.sheets['sheet1'].range('B9').value=[('Foo 1', 'Foo 2', 'Foo 3'), (10.0, 20.0, 30.0)]

# sht.range('A1').options(transpose=True).value = [1,2,3,4]   竖写

# start_grid = 'C8'
# excel_data = wb.sheets['sheet1'].range(start_grid).expand().value
# print(excel_data)

# xw.Range('A5').options(transpose=True).value = [('Foo 1', 'Foo 2', 'Foo 3'), (10.0, 20.0, 30.0)]

# wb.save()
# wb.close()
# app.quit()
def insert_data(db_name,data):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print("Opened database successfully")
    print(data)

    sql = "INSERT INTO Products (Product_name,Product_name_cn,PartNumber,Description,Description_cn,UnitPrice) VALUES (?,?,?,?,?,?)"
    try:
        c.executemany(sql ,data)
        # c.execute(sql ,data)

                # Product_name 
                # Product_name_cn 
                # # PartNumber          text,
                # # Description         text,
                # # Description_cn      text,
                # # UnitPrice           real, 

        conn.commit()
        print("Records created successfully")

    except BaseException as e:
        print("错误！",e)

    finally:
        conn.close()
        print("close conn")
    print("end")

def check_duplicate(content_list)
    for item in content_list:
        if item

def read_activesheet(data_range):
    sht=xw.sheets.active
    result = sht[data_range].value
    return(result)

if __name__ == '__main__':
    # 设定~~~~~~~~~~~~~~~~~
    db_name = 'shanglin.db'  
    data_range = 'C8:G20'
    Product_name = 'SPIKE LIGHT'
    Product_name_cn = '花园灯'
    # PartNumber          text,
    # Description         text,
    # Description_cn      text,
    # UnitPrice           real,
    # Primary Key(PartNumber)
    # 设定~~~~~~~~~~~~~~~~~

    content = read_activesheet(data_range)
    print(content)

    quotation_list = []
    for part in content:
        quotation_list.append((Product_name, Product_name_cn, part[2], str(part[3]).replace('\xa0', ''), str(part[0]).replace('\xa0', '')+' '+str(part[1]).replace('\xa0', ''), part[4]))

    for part in quotation_list:        
        print(part)

    response = input("请确认是否写入数据库(y/n)?: ")
    if response.lower() == 'y':
        insert_data(db_name, quotation_list)





""" 
直接读写打开的文件
import xlwings as xw
xw.Range('A1').value = 'something'   

app = xw.apps.active


sht=xw.books[0].sheets['sheet1']

引用活动工作簿
wb=xw.books.active

引用活动页
sht=xw.sheets.active

sht['A1:B5'].value
sht[:5,:5].value

xw.Range((1,1),(3,3)).value


常用函数和方法
Book 工作簿常用的api
wb=xw.books[‘工作簿名称']
wb.activate()激活为当前工作簿
wb.fullname 返回工作簿的绝对路径
wb.name 返回工作簿的名称
wb.save(path=None) 保存工作簿，默认路径为工作簿原路径，若未保存则为脚本所在的路径
-wb. close() 关闭工作簿
代码例子：
# 引用Excel程序中，当前的工作簿
wb=xw.books.acitve
# 返回工作簿的绝对路径
x=wb.fullname
# 返回工作簿的名称
x=wb.name
# 保存工作簿，默认路径为工作簿原路径，若未保存则为脚本所在的路径
x=wb.save(path=None)
# 关闭工作簿
x=wb.close()
sheet 常用的api
# 引用某指定sheet
sht=xw.books['工作簿名称'].sheets['sheet的名称']
# 激活sheet为活动工作表
sht.activate()
# 清除sheet的内容和格式
sht.clear()
# 清除sheet的内容
sht.contents()
# 获取sheet的名称
sht.name
# 删除sheet
sht.delete
range常用的api
# 引用当前活动工作表的单元格
rng=xw.Range('A1')
# 加入超链接
# rng.add_hyperlink(r'www.baidu.com','百度',‘提示：点击即链接到百度')
# 取得当前range的地址
rng.address
rng.get_address()
# 清除range的内容
rng.clear_contents()
# 清除格式和内容
rng.clear()
# 取得range的背景色,以元组形式返回RGB值
rng.color
# 设置range的颜色
rng.color=(255,255,255)
# 清除range的背景色
rng.color=None
# 获得range的第一列列标
rng.column
# 返回range中单元格的数据
rng.count
# 返回current_region
rng.current_region
# 返回ctrl + 方向
rng.end('down')
# 获取公式或者输入公式
rng.formula='=SUM(B1:B5)'
# 数组公式
rng.formula_array
# 获得单元格的绝对地址
rng.get_address(row_absolute=True, column_absolute=True,include_sheetname=False, external=False)
# 获得列宽
rng.column_width
# 返回range的总宽度
rng.width
# 获得range的超链接
rng.hyperlink
# 获得range中右下角最后一个单元格
rng.last_cell
# range平移
rng.offset(row_offset=0,column_offset=0)
#range进行resize改变range的大小
rng.resize(row_size=None,column_size=None)
# range的第一行行标
rng.row
# 行的高度，所有行一样高返回行高，不一样返回None
rng.row_height
# 返回range的总高度
rng.height
# 返回range的行数和列数
rng.shape
# 返回range所在的sheet
rng.sheet
#返回range的所有行
rng.rows
# range的第一行
rng.rows[0]
# range的总行数
rng.rows.count
# 返回range的所有列
rng.columns
# 返回range的第一列
rng.columns[0]
# 返回range的列数
rng.columns.count
# 所有range的大小自适应
rng.autofit()
# 所有列宽度自适应
rng.columns.autofit()
# 所有行宽度自适应
rng.rows.autofit()
books 工作簿集合的api
# 新建工作簿
xw.books.add()
# 引用当前活动工作簿
xw.books.active
sheets 工作表的集合
# 新建工作表
xw.sheets.add(name=None,before=None,after=None)
# 引用当前活动sheet
xw.sheets.active





"""