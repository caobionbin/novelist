import os
import time
import configparser
import re
from random import randint
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'}
# this_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
this_dir = os.getcwd()


def findbookinbaidu(bookname):
    baidu_url = 'https://www.baidu.com/s'
    # google_url = 'https://www.google.com/webhp#'

    pn = 0
    result = []
    times = 5
    while not result and times:
        times -= 1

        try:
            params = {'ie': 'utf-8', 'pn': pn, 'wd': bookname + 'site:23wx.com'}
            res = requests.get(baidu_url, params=params, headers=header)
        except Exception as e:
            print(e, "failed to find %s in baidu ..." % bookname)
            continue

        if res.status_code != 200:
            print(res.status_code)
            print('error in search %s' % bookname)
            continue

        soup = BeautifulSoup(res.content.decode('utf8'), "lxml")
        for h3 in soup.find_all('h3'):
            # print(h3)
            print(h3.text, h3.a['href'])
            result.append((h3.text, h3.a['href']))
    return result

config_filename = os.path.join(this_dir, 'source.ini')
# print(config_filename)
cf = configparser.ConfigParser()
# cf.read('/Users/zhangdesheng/Documents/python-learning/zds-git/novelist/novelget/source.ini')
cf.read(config_filename)
# print(cf.sections())

def findbook(bookname):

    result = []
    prefix = cf['hchuag']['url']
    slink = cf['hchuag']['slink']
    __searchdata = {'q': bookname}
    # params = {'q': quote(bookname.encode('utf8').decode('gbk'))}
    slink = slink + '?' + urlencode(__searchdata, encoding='gbk')
    res = None
    retry_time = 5
    if not result and retry_time > 1:
        retry_time -= 1
        try:
            # res = requests.get(slink, params=params, headers=header)
            res = requests.get(slink, headers=header)
        except Exception as e:
            if retry_time == 1:
                print(e)
            else:
                pass
    html = res.content.decode('gbk', 'ignore')
    soup = BeautifulSoup(html, "html.parser")
    findstring = 'soup.' + cf['hchuag']['s_list']
    s_list = eval(findstring)
    for d in s_list:

        t = eval('d.'+cf['hchuag']['s_list_title'])
        u = prefix+ eval('d.'+cf['hchuag']['s_list_url'])
        # print(t, u)
        booknumber = re.findall('/(\d+)/', u)[0]
        # print(booknumber)
        result.append((t, u, booknumber))
    return result


def getbook(booknumber):
    result = []
    prefix = cf['hchuag']['url']
    url = prefix + '/' + booknumber + '/'
    try:
        res = requests.get(url, headers=header)
    except Exception as e:
        print(e)

    soup = BeautifulSoup(res.content.decode('gbk', 'ignore'), "html.parser")
    all_chapter_links = []
    try:
        string = 'soup.' + cf['hchuag']['chapter_list']
        all_chapter_links = eval(string)
    except Exception as e:
        print(e)

    for u in all_chapter_links:
        result.append((u.text, prefix+u['href']))
    return result


def downloadbook(booknumber):

    prefix = cf['hchuag']['url']
    url = prefix + '/' + booknumber + '/'
    try:
        res = requests.get(url, headers=header)
    except Exception as e:
        print(e)

    soup = BeautifulSoup(res.content.decode('gbk', 'ignore'), "lxml")
    all_chapter_links = []
    try:
        string = 'soup.' + cf['hchuag']['chapter_list']
        all_chapter_links = eval(string)
    except Exception as e:
        print(e)
    # print(all_chapter_links)
    for i, u in enumerate(all_chapter_links):
        # print(i, u)
        # print('fetch %d chapter begin...' % i)
        try:
            # chapter_url = url+u['href']
            # print(chapter_url)
            content = requests.get(prefix+u['href'], headers=header).content.decode('gbk', 'ignore')
            content = re.sub('<br />','\n', content)
            contentsoup = BeautifulSoup(content, "lxml")
        except Exception as e:
            print(e)
            print('fetch %d chapter error...' % i)
        # print(contentsoup)
        title_string = 'contentsoup.' + cf['hchuag']['chapter_title']
        content_string = 'contentsoup.' + cf['hchuag']['chapter_content']
        try:
            # print(title_string)
            # print(content_string)
            title = (eval(title_string))
            text = (eval(content_string))
        except Exception as e:
            print(e)
            print('fetch %d chapter error...' % i)
        # print(title)
        # print(text)
        yield title +'\n' + text
        # break
f = open('xxx.txt', 'w')
for content in downloadbook('28966'):
    f.write(content+'\n')