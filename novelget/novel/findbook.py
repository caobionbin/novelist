# coding=utf-8

from urllib.parse import quote, unquote

from bs4 import BeautifulSoup
import requests


DINGDIAN = 'http://www.23wx.com/'
WU200 = 'http://www.5200xs.org/'
HUNHUN = 'http://www.hunhun520.com/'
JJZW = 'http://www.99zw.cn/'
WU200_SEARCH = 'http://www.5200xs.org/search.php'
SOURCE_WEBSITE = [DINGDIAN, WU200, 'xxx']

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
}

def findbook(bookname):
    """
    输入一个书名,返回在盗版网站的搜索结果
    """
    find_list = []

    for source in SOURCE_WEBSITE:

        if source == WU200:
            search_url = source + 'search.php?type=bookname&key=' + quote(bookname, encoding='gbk')
            sattrs = {'class': 'list'}
        else:
            print('暂时不支持从%s搜索...' % source)
            continue
        print(search_url)
        try:
            res = requests.get(search_url, headers=HEADER)
        except ConnectionError as e:
            print(e)
            print('查询%s碰到一点困难...' % source)
            continue
        except Exception as e:
            print(e)
            print('查询%s碰到一点困难...' % source)
            continue
        # print(res.headers)
        if res.status_code == 200:
            try:
                html = res.content.decode('gbk')
            except Exception as e:
                html = res.text

            # print(html)
            soup = BeautifulSoup(html, "lxml")
            results_list = soup.find_all(name='div', attrs=sattrs)
            # print(results_list)
            if results_list:
                for r in results_list:
                    print(r.h1.a.text, '|||', r.h1.a['href'])
                    find_list.append((r.h1.a.text, r.h1.a['href'], source))

            else:
                print('no reuslt for %s ' % bookname)
        else:
            print('can not find target [%s]' % search_url)

    return find_list


findbook('xxx')
