import json
import os
import zipfile

import requests
import re
import xlwt
from lxml import etree

# 域名
baseurl = "https://theme.npm.edu.tw/opendata/"
# UA伪装
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
}
# 压缩包下载位置
unzip_path = 'D:/work_spce_python/让台北故宫文物回家/zip'

# reptile_json位置
jsons_path = 'D:/work_spce_python/让台北故宫文物回家/reptile_json'


def main():
    # url = "https://theme.npm.edu.tw/opendata/DigitImageSets.aspx?pageNo=161"
    # 正则表达式预编译
    obj = re.compile(r'<div class="project-detail">.*?</span>(?P<id>.*?)</li>'
                     r'.*?</span>(?P<dynasty>.*?)</li>'
                     r'.*?</span>(?P<category>.*?)</li>'
                     r'.*?</span>(?P<function>.*?)</li>'
                     r'.*?</span>(?P<material>.*?)</li>'
                     r'.*?</span>(?P<exposition>.*?)</li>')
    # 创建excel
    book = xlwt.Workbook()
    sheet = book.add_sheet("文物")
    # 初始化excel
    init_excel(sheet)
    # 文物数为1
    row = 1
    # （2-1445；2-1782）
    # 第161面-第198面
    for i in range(161, 162):
        page = i
        url = "https://theme.npm.edu.tw/opendata/DigitImageSets.aspx?pageNo="
        url = url + str(page)
        baseresp = requests.get(url, headers=headers)  # 处理一个小反爬
        baseresp.encoding = "utf-8"
        et = etree.HTML(baseresp.text)
        # 使用xpath找到超链接位置
        baseresult = et.xpath("//ul[@class='painting-list']/li/a/@href")
        for baseitem in baseresult:
            # 将获取的超链接与域名结合形成完整地文物链接
            url = baseurl + baseitem
            resp = requests.get(url, headers=headers)
            resp.encoding = "utf-8"
            result = obj.finditer(resp.text)
            for item in result:
                dic = item.groupdict()
                # write_excel(dic, row, book, sheet)  # 将爬取的信息文物写入excel
                diction = {}

                # 给字典赋值
                Id = '文物圖檔編號：'
                Iinformation = dic.get('id')

                diction[Id] = Iinformation

                Dynasty = '朝代：'
                Dinformation = dic.get('dynasty')
                diction[Dynasty] = Dinformation

                Category = '類別：'
                Cinformation = dic.get('category')
                diction[Category] = Cinformation

                Function = '功能：'
                Finformation = dic.get('function')
                diction[Function] = Finformation

                Material = '質材：'
                Minformation = dic.get('material')
                diction[Material] = Minformation

                Exposition = '說明文：'
                Einformation = dic.get('exposition')
                diction[Exposition] = Einformation

                # 将字典转变为json
                json_dict = json.dumps(diction, indent=2, ensure_ascii=False)
                print("第{}个文物爬取成功".format(row), json_dict)

                # 将爬取的数据写入json文件中
                write_json(diction, Iinformation)

                # 下载本文物的压缩包
                down_zip(url, Iinformation)
                # 文物数+1
                row = row + 1
                # print(resp.text)


# 初始化excel
def init_excel(sheet):
    title = ["文物圖檔編號", "朝代", "類別", "功能", "質材", "說明文"]
    for i in range(len(title)):  # 循环列
        sheet.write(0, i, title[i])


# 将信息写入excel
def write_excel(d, row, book, sheet):
    column = 0
    for value in d.values():  # 循环字典
        sheet.write(row, column, value)
        column = column + 1
    book.save('让台北故宫的文物回家1.xls')


# 将文物数据写入json文件中,dic：文物字典，ID：文物编号
def write_json(dic, ID):
    json_file_save = './reptile_json/' + ID + '.json'
    with open(json_file_save, "w+", encoding='utf-8') as code:
        json.dump(dic, code, ensure_ascii=False,indent=2) #indent=2缩进，让其换行
        print("保存json文件成功")


# 下载压缩包 传入文物链接及文物ID，url：文物链接，ID:文物编号
def down_zip(url, ID):
    resp = requests.get(url, headers=headers)
    etzip = etree.HTML(resp.text)
    # 找寻文物下载链接
    zipresult = etzip.xpath("//div[@class='project-img']/a[@class='download-btn']/@href")
    for zipistem in zipresult:
        zipurl = baseurl + zipistem
        print(zipurl)
        # print(zip_save)
        # 下载压缩包
        zip_file_save = "./zip/" + ID + ".zip"
        zipresp = requests.get(zipurl)
        # 将压缩包写入zip文件夹
        with open(zip_file_save, "wb") as code:
            code.write(zipresp.content)
        print("{}.zip下载成功！".format(ID))


def unzip_zip(file_path):
    # 读取file_path目录下的所有文件名
    file = os.listdir(file_path)  # 获取目录下所有文件名
    for file_name in file:
        path = os.path.join(file_path, file_name)
        zip_file = zipfile.ZipFile(path)  # 获取压缩文件
        newfilepath = file_name.split(".", 1)[0]  # 获取压缩文件的文件名
        newfilepath = os.path.join(file_path, newfilepath)
        os.mkdir(newfilepath)  # 创建装压缩文件的文件夹
        for name in zip_file.namelist():  # 解压文件
            zip_file.extract(name, newfilepath)
        zip_file.close()

        if os.path.exists(path):  # 删除原先压缩包
            os.remove(path)
        print("解压{0}成功".format(file_name))


# 补充文物json文件
def merge_json(file_path):
    file = os.listdir(file_path)  # 获取目录下所有文件名
    for file_name in file:
        ID = file_name.split(".", 1)[0]  # 获取压缩文件的文件名
        merges_path = './zip/' + ID + '/' + ID + '.json'
        # a 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入
        with open('./reptile_json/{}.json'.format(ID), 'r', encoding='utf-8') as f_r:
            # 储存为一个列表形式
            lines = f_r.readlines()
        with open(merges_path, 'a', encoding='utf-8') as f_w:
            for line in lines:
                f_w.writelines(line)
        f_w.close()
        print('{}文物补充完成'.format(ID))


if __name__ == '__main__':
    #main()
    unzip_zip(unzip_path)
    merge_json(jsons_path)
    print("爬取成功")
