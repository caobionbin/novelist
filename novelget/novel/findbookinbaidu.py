import time

import requests
from bs4 import BeautifulSoup


def findbookinbaidu(bookname):
    baidu_url = 'https://www.baidu.com/s'

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'}

    s = requests.session()
    s.keep_alive = False
    pn = -10
    result = []
    while not result:
        pn += 10
        try:
            params = {'ie': 'utf-8', 'pn': pn, 'wd': bookname + 'site:qidian.com'}
            res = s.get(baidu_url, params=params, headers=header)
        except Exception as e:
            print(e, "failed to find %s in baidu ..." % bookname)
            continue

        if res.status_code != 200:
            print(res.status_code)
            print('error in search %s' % bookname)
            continue

        soup = BeautifulSoup(res.content.decode('utf8'), "lxml")
        for h3 in soup.find_all('h3'):
            print(h3)
            # print(h3.text, h3.a['href'])
            result.append((h3.text, h3.a['href']))
    return result


def getbook(url):
    '''
    从给定的url获取书本的章节,暂时只支持顶点小说网"http://www.23wx.com/"
    yield 本章内容, 下章url, 目录url.
    '''
    pass

findbookinbaidu('斗罗大陆')

