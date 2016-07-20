# encoding:UTF-8
# from threading import Thread
import pickle
from configparser import ConfigParser
import os
from os import (path, makedirs, listdir)
from urllib import (request, parse)
import requests
from flask import jsonify
from bs4 import BeautifulSoup

DIRDICT = {'novellist': './novel/list.dat', \
           'noveldata': lambda novelname: './novel/' + novelname + '/info.dat', \
           'chapter_name': lambda novelname: './novel/' + novelname + '/chapter_name.dat', \
           'chapter_link': lambda novelname: './novel/' + novelname + '/chapter_link.dat', \
           'chapter': lambda novelname, index: './novel/' + novelname + '/' + repr(index) + '.txt'}
CONFIG = ConfigParser()
this_dir = "/Users/zhangdesheng/Documents/python-learning/zds-git/novelist/novelget/novel"

CONFIG.read(os.path.join(this_dir, "config.ini"), encoding='utf8')

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'}


def Get_ID():
    '''获取搜索网站设置的ID列表'''
    ID = list()

    for item in CONFIG.sections():
        ID.append(item)
    return ID

if __name__ == '__main__':
    print(Get_ID())

def Search_By_ID(novelname, id='bqg5200'):
    '''获取小说信息（目录）页
    novelname：小说名
    id：网站设置ID
    '''

    opts = CONFIG[id]
    __searchdata = {}
    __searchdata[opts['keyword']] = novelname  # 构建搜索关键词
    url = opts["slink"] + parse.urlencode(__searchdata, encoding='GBK')  # 关键词URL编码
    try:
        data = requests.get(url, headers=header).content  # 读取搜索页面内容
    except:
        return -1  # 网站无法连接
    soup = BeautifulSoup(data, "html.parser")  # 构建BS数据
    string = 'soup.' + opts["novel_link"]
    try:
        url = eval(string)  # 获取小说页面链接
    except:
        return -2
    if not url.startswith('http'):
        url = opts["url"] + url  # 构建小说页面链接
    # try:
    #     data = request.urlopen(url).read()                             #读取小说信息页面内容
    # except:
    #     return -1                                                      #小说信息页面无法连接
    return url

# url = Search_By_ID('雪鹰领主', 'bqg5200')
# print(url)


def Get_Novel_Info(url, id='bqg5200'):
    '''获取小说信息
    url：小说信息（目录）页
    id：网站ID'''
    opts = CONFIG[id]
    noveldata = {}
    try:
        data = requests.get(url, headers=header).content  # 读取小说页面内容
    except:
        return -1  # 小说页面无法连接
    soup = BeautifulSoup(data, "html.parser")  # 构建BS数据
    # --------------------------------------------------抓取小说信息
    noveldata['homepage'] = opts['url']
    noveldata['infolink'] = url
    noveldata['id'] = opts['id']
    noveldata['website'] = opts['name']

    string = 'soup.' + opts['title']
    noveldata['title'] = eval(string)

    try:
        string = 'soup.' + opts['content_link']
        string = eval(string)
        if not string.startswith('http'):
            string = noveldata['homepage'] + string
        noveldata['content_link'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['description']
        noveldata['description'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['category']
        noveldata['category'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['author']
        noveldata['author'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['status']
        noveldata['status'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['update']
        noveldata['update'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['latest']
        noveldata['latest'] = eval(string)
    except:
        pass

    try:
        string = 'soup.' + opts['image']

    except:
        pass
    string = eval(string)
    if not string.startswith('http'):
        string = noveldata['homepage'] + string
    noveldata['image'] = string

    # #--------------------------------------------------创建小说文件夹
    # filename = './novel/' + noveldata['title'] + '/'
    # if not path.exists(filename):
    #     makedirs(filename)
    # #--------------------------------------------------写入小说信息
    # filename = './novel/' + noveldata['title'] + '/' + 'info.dat'
    # pickle.dump(noveldata, open(filename, "wb"))
    # #--------------------------------------------------写入小说列表
    # filename = './novel/' + 'list.dat'
    # novel_list = list()
    # for item in listdir('./novel/'): 
    #     if path.isfile('./novel/'+item+'info.dat'): 
    #         novel_list.append(item)
    # pickle.dump(novel_list, open(filename, "wb"))

    return noveldata
if __name__ == '__main__':
    url = 'http://www.bqg5200.com/xiaoshuo/0/62/'
    novel_data = Get_Novel_Info(url, 'bqg5200')
    print(novel_data)


def Save_Content(noveldata):
    """从预定网站下载章节列表
    noveldata:小说信息字典
    """
    chapter_name = []
    chapter_link = []

    opts = CONFIG[noveldata['id']]

    if 'content_link' in noveldata:
        url = noveldata['content_link']
    else:
        url = noveldata['infolink']
    try:
        data = requests.get(url, headers=header).content  # 读取目录页面内容
    except:
        return -1  # 目录页面无法连接
    soup = BeautifulSoup(data, "html.parser")  # 构建BS数据
    # --------------------------------------------------抓取小说章节列表
    string = 'soup.' + opts['chapter_list']
    chapters = []
    for chapter_list in eval(string):
        string = eval(opts['chapter_name'])
        string = str(string)
        # chapter_name.append(string)
        url = eval(opts['chapter_link'])
        if not url.startswith('http'):
            url = opts['url'] + eval(opts['chapter_link'])
        # chapter_link.append(url)
        chapters.append((string, url))
    # chapters = dict(zip(chapter_link, chapter_name))
    # for key, value in chapters.items():
    #     print(key, value)
    # if end == -1:
    #     end = len(self.chapter_link)
    # for i in range(start,end):
    #     data=request.urlopen(self.chapter_link[i]).read()            #读取章节内容
    #     soup = BeautifulSoup(data,"html.parser")                     #构建BS数据
    #     text = eval('soup.'+self.opts['text'])
    #     filename = './novel/' + self.noveldata['title'] + '/' + repr(i) + '.txt'
    #     fo = open(filename, "wb")
    #     fo.write(text.encode('utf8'))
    #     fo.close()
    return chapters
if __name__ == '__main__':
    Save_Content(noveldata=novel_data)


def Get_New_Chapter_List(noveldata):
    '''从预定网页更新章节列表
    noveldata：小说信息字典'''
    update_noveldata = {}
    chapter_name = []
    chapter_link = []
    update_chapter_name = []
    rt = []
    t = {}

    if 'content_link' in noveldata:
        url = noveldata['content_link']
    else:
        url = noveldata['infolink']
    update_noveldata = Get_Novel_Info(url, noveldata['id'])
    if update_noveldata == -1:
        return '-1'
    if update_noveldata['latest'] == noveldata['latest']:
        return '0'

    opts = CONFIG[noveldata['id']]
    chapter_name = pickle.load(open(DIRDICT['chapter_name'](noveldata['title']), "rb"))
    try:
        data = request.urlopen(url).read()  # 读取目录页面内容
    except:
        return '-1'  # 目录页面无法连接
    soup = BeautifulSoup(data, "html.parser")  # 构建BS数据
    # --------------------------------------------------抓取小说章节列表
    string = 'soup.' + opts['chapter_list']
    for chapter_list in eval(string):
        string = eval(opts['chapter_name'])
        string = str(string)
        update_chapter_name.append(string)
        url = eval(opts['chapter_link'])
        if not url.startswith('http'):
            url = opts['url'] + eval(opts['chapter_link'])
        chapter_link.append(url)
    for chapter in update_chapter_name:
        if not chapter in chapter_name:
            rt.append({"index": update_chapter_name.index(chapter), "name": chapter})
    if 'lastread' in noveldata:
        update_noveldata['lastread'] = noveldata['lastread']
    pickle.dump(update_noveldata, open(DIRDICT['noveldata'](noveldata['title']), "wb"))
    # --------------------------------------------------写入小说目录
    pickle.dump(update_chapter_name, open(DIRDICT['chapter_name'](noveldata['title']), "wb"))
    pickle.dump(chapter_link, open(DIRDICT['chapter_link'](noveldata['title']), "wb"))
    # t['list'] = rt
    return jsonify({'list': rt})


def escape(txt, space=1):
    '''将txt文本中的空格、&、<、>、（"）、（'）转化成对应的的字符实体，以方便在html上显示'''
    txt = txt.replace('&', '&amp;')
    txt = txt.replace(' ', '&nbsp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    txt = txt.replace('\'', '&apos;')
    txt = txt.replace('\r', space * '<br />')
    txt = txt.replace('\n', space * '<br />')
    return txt


def Load_Novel_List():
    '''载入小说列表'''
    try:
        return pickle.load(open(DIRDICT['novellist'], "rb"))
    except:
        print("小说列表未创建")
        return None


def Load_Novel_Data(novelname):
    '''载入小说信息
    novelname：小说名
    '''
    try:
        return pickle.load(open(DIRDICT['noveldata'](novelname), "rb"))
    except:
        print("未找到该小说")
        return None


def Load_Chapter_List(novelname):
    '''载入小说章节列表
    novelname：小说名'''
    try:
        return pickle.load(open(DIRDICT['chapter_name'](novelname), "rb"))
    except:
        print("未找到章节列表")
        return None


def Load_Chapter(novelname, index):
    '''载入本地章节内容
    novelname：小说名
    index：章节标志位
    '''
    if path.isfile(DIRDICT['chapter'](novelname, index)):
        return open(DIRDICT['chapter'](novelname, index), encoding='utf8').read()
    else:
        return -1


def Search_Chapter(novelname, index):
    '''从预定网站下载指定章节
    novelname：小说名
    index：章节标志位
    '''
    noveldata = {}
    chapter_link = []
    try:
        noveldata = pickle.load(open(DIRDICT['noveldata'](novelname), "rb"))
        chapter_link = pickle.load(open(DIRDICT['chapter_link'](novelname), "rb"))
    except:
        return -1

        # 载入网站设置
    opts = CONFIG[noveldata['id']]

    try:
        data = request.urlopen(chapter_link[index]).read()  # 读取章节内容
    except:
        return -2
    soup = BeautifulSoup(data, "html.parser")  # 构建BS数据
    text = eval('soup.' + opts['text'])
    return text


def get_chapter_content(chapter_url, book_website):
    opts = CONFIG[book_website]
    try:
        soup = BeautifulSoup(requests.get(chapter_url, headers=header).content, "html.parser")
        content = eval('soup.' + opts['text'])
    except:
        content = '未找到章节内容,刷新重试'
    return content


def Get_Chapter(novelname, index):
    '''尝试从本地与网站载入章节
    novelname：小说名
    index：章节标志位
    '''
    text = Load_Chapter(novelname, index)
    if text == -1:
        text = Search_Chapter(novelname, index)
        if text == -1:
            return '未找到章节信息！'
        elif text == -2:
            return '未找到章节！'
        else:
            open(DIRDICT['chapter'](novelname, index), "wb").write(text.encode('utf8'))
    return text
