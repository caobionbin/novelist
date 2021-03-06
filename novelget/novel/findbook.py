# coding=utf-8

import re, time
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


def nujiangzhizhan():

    url = 'http://www.kanunu8.com/files/terrorist/201102/1741.html'

    html = requests.get(url, headers=HEADER).content.decode('gbk', 'ignore')
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all('a'):
        if re.findall('(17(\d+)/(\d+))', str(a)):
            # print(a['href'])
            u = 'http://www.kanunu8.com/files/terrorist/201102/' + a['href']
            # print(u)
            h = requests.get(u, headers=HEADER).content.decode('gbk', 'ignore')
            s = BeautifulSoup(h, "lxml")
            title = s.title.text
            content = s.find(name='td', attrs={'width': '820'}).text
            print(title)
            print(content)


def guanlufengliu():
    fw = open('guanlufengliu.txt', 'w')
    url = 'http://www.guanlufengliu.com/'
    html = requests.get(url, headers=HEADER).content.decode('utf8', 'ignore')
    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    for a in soup.find_all('a'):
        if re.findall('wangluoban/(\d+)', str(a)):
            # print(a)
            if not a['href'].startswith('http'):
                u = 'http://www.guanlufengliu.com' + a['href']
            else:
                u = a['href']
            print(u)
            getsite = requests.get(u, headers=HEADER)
            print(getsite.status_code)
            while getsite.status_code != 200:
                getsite = requests.get(u, headers=HEADER)
            h = getsite.content.decode('utf8', 'ignore')
            s = BeautifulSoup(h, "html.parser")
            title = s.title.text.split('-')[0]
            # print(h)
            if not s:
                content = '没有抓取到 %s ' % u
            else:
                try:
                    content = s.find(name='div', attrs={'class': 'span9'}).text
                except Exception as e:
                    content = s.find(name='div', attrs={'class': 'span12'}).text
                    print(e)
                except:
                    content = '没有抓取到 %s ' % u
                string = "(adsbygoogle = window.adsbygoogle || []).push({});"
                if string in content:
                    content = content.split(string)[1]
                else:
                    pass
                # print(content)
            # break
            fw.write(title+'\n')
            fw.write(content+'\n')
            time.sleep(0.5)


def guandaozhisejie():
    url = 'http://www.kanunu8.com/book3/6967/'
    f = open('guandaozhishejie', 'w')
    html = requests.get(url, headers=HEADER).content.decode('gbk', 'ignore')
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all('a'):
        if re.findall('(13[56](\d+).html)', str(a)):
            # print(a['href'])
            u = 'http://www.kanunu8.com/book3/6967/' + a['href']
            # print(u)
            h = requests.get(u, headers=HEADER).content.decode('gbk', 'ignore')
            s = BeautifulSoup(h, "lxml")
            title = s.title.text
            content = s.find(name='td', attrs={'width': '820'}).text
            # print(title)
            # print(content)
            f.write(title+'\n')
            f.write(content + '\n')


def gaoshoujimo2():
    time_start = time.time()
    url = 'http://www.shumilou.co/gaoshoujimo2'
    f = open('高手寂寞2.txt', 'w')
    s = requests.session()
    HEADER.update({'Host': 'www.shumilou.co'})
    HEADER.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
    html = s.get(url, headers=HEADER, timeout=10).content.decode('utf8', 'ignore')
    soup = BeautifulSoup(html, "lxml")
    ul = soup.find('ul')
    for a in ul.find_all('a'):
        u = 'http://www.shumilou.co' + a['href']
        try:
            content = s.get(u).content.decode('utf8', 'ignore')
        except ConnectionError:
            time.sleep(2)
            content = s.get(u).content.decode('utf8', 'ignore')
        except Exception:
            time.sleep(2)
            content = s.get(u).content.decode('utf8', 'ignore')
        _soup = BeautifulSoup(content, "lxml")
        f.write(_soup.title.text.split('高手寂寞2')[0] + '\n')
        for p in _soup.find_all('p'):
            if not p.text.startswith('书迷楼最快更新'):
                f.write(p.text + '\n')
        time.sleep(0.2)
    time_end = time.time()
    print(time_end-time_start)


# 多线程抓取www.shumilou.co小说
def fetch_shumilou():
    pass


if __name__ == '__main__':
    try:
        gaoshoujimo2()
    except Exception as e:
        print(e+'...try again')
