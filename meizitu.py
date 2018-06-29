# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
                        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
           ,'Referer':'http://www.mzitu.com/',}

url = 'http://www.mzitu.com/all/'

start_html = requests.get(url,headers = headers)   #获取页面
# print(start_html.text)            #打印网页源码

Soup = BeautifulSoup(start_html.content,'lxml')
all_a = Soup.find('div',class_='all').findAll('a')

# print(os.getcwd())
all_path = os.getcwd()+'\\tupian\\'
# print(all_path)


b = 0
for a in all_a:
    # print(a,type(a))   #<class 'bs4.element.Tag'>类型
    title = a.get_text()   #   title = a.get_text()
    title = title.replace('?',' ')
    title = title.replace(':',' ')
    path = str(title).strip()
    # print('在前面')
    try:
        os.makedirs(os.path.join(all_path,path))   #os.path.join   将多个路径组合后返回
        os.chdir(all_path+path)
        b += 1
    except FileExistsError:
        continue
    except NotADirectoryError and OSError as e:
        print(e)
        break
    print('通过')
    href = a['href']
    print(href)
    html = requests.get(href,headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()   #获取这个套图的总页数
    count = 0
    for page in range(1,int(max_span)+1):
        page_url = href + '/' +str(page)
        img_html = requests.get(page_url,headers = headers)
        #解析页面
        img_Soup = BeautifulSoup(img_html.content,'lxml')



        tupian = img_Soup.find('div',class_='main-image').find('img')['src']
        name = tupian[-9:-4]
        tp = requests.get(tupian,headers=headers)
        with open(name + '.jpg', 'ab') as f:
            f.write(tp.content)
        count +=1
        if count >= 10000:   #设置每个文件夹爬取的张数
            break
    if b >= 30000:    #设置爬取多少次，因为没什么流量
        break

# x = requests.get('http://images2015.cnblogs.com/blog/140867/201601/140867-20160103115154339-792142004.png',headers=headers)
# print(x.content)
# f = open('1'+'.jpg','ab')
# f.write(x.content)
# f.close()


