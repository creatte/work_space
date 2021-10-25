"""
目标：豆瓣top250电影信息
    名称，发布年限，评分，评价人数

思路：
    1.拿到页面源代码
    2.使用re正则去提取数据
    3.存储到文件中。。。
"""

import requests
import re
import xlwt

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }
    obj = re.compile(r'<div class="item">.*?<span class="title">(?P<name>.*?)</span>'
                     r'.*?<br>(?P<year>.*?)&nbsp;'
                     r'.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                     r'.*?<span>(?P<num>.*?)人评价</span>',re.S) #re.S可以让re匹配到换行符

    for i in range(1,11):
        page = (i-1) * 25
        url = "https://movie.douban.com/top250?start=page&filter="
        resp = requests.get(url , headers = headers) # 处理一个小反爬
        resp.encoding = "utf-8"
        # print(resp.text)
        result = obj.finditer(resp.text)
        for item in result:
            dic = item.groupdict()
            dic['year'] = dic['year'].strip() #去掉年份左右俩端的空白
            print(dic)
        print("第{}面爬取完毕".format(i))

if __name__ == '__main__':
    main()
    print("爬取完毕")
# def saveData(datalist):
#     # 创建workbook对象(创建表文件)
#     workbook = xlwt.Workbook(encoding="utf-8")
#     # 创建工作表单
#     worksheet = workbook.add_sheet('top250')
#     col = ("电影中文名", "电影年份", "电影评分", "电影参评人数")
#     # 写入数据
#     for i in range(0,4):# 写入列名
#         worksheet.write(0,i,col[i])
#     for i in range(0,250):
#         print("第%d条"%(i+1))
#         data = datalist[i]
#         for j in range(0,4):
#             worksheet.write(i+1,j,data[j])  #数据写入
#     # 保存数据表
#     workbook.save("top250.xls")


