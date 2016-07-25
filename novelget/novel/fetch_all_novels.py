#coding: utf8

import pymysql
import time
from time import gmtime, strftime
import requests
from bs4 import BeautifulSoup
import re
import os.path, os

from fetch_novel import Get_Novel_Info, Save_Content, get_chapter_content

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'}

base_url = 'http://www.xs111.com'

# engine = create_engine("pymysql+connect://novelist:novelist#@119.29.201.221:3306/novel")
# DBSession = sessionmaker(bind=engine)

def fetch_and_save_book():
    conn = pymysql.connect(host='119.29.201.221', port=3306, user='novelist', db='novel', password='novelist#')
    cur = conn.cursor()
    for i in range(1000):
        url = base_url + '/book/' + str(i) + '/'
        print(url)

        noveldata = Get_Novel_Info(url)
        if not noveldata.get('title', None):
            continue
        print(noveldata['title'])
        if 'content_link' in noveldata.keys():
            print(noveldata['content_link'])
        else:
            print(noveldata['infolink'])

    cur.close()
    conn.close()


# 获取笔趣阁5200排行榜所有小说
def fetch_toplist_books(id='bqg5200'):
    conn = pymysql.connect(host='119.29.201.221', port=3306, user='novelist', db='novel', password='novelist#')
    cur = conn.cursor()
    top_url = 'http://www.bqg5200.com/paihang.html'
    try:
        r = requests.get(top_url, headers=header)
    except:
        raise "访问排行榜失败,请重试"
    alist = re.findall(r'http://www.bqg5200.com/book/[0-9]+', r.content.decode('gbk', 'ignore'))
    for link in set(alist):
        print(link)

        try:
            r = requests.get(link, headers=header)
        except Exception as e:
            print('获取小说信息失败 %s ' % e)
            continue
        if r.status_code != 200:
            continue
        noveldata = get_noveldata(content=r.content.decode('gbk', 'ignore'), url=link)
        if noveldata == -1:
            continue
        # print(noveldata)
        if not noveldata.get('title', None):
            continue
        cur.execute("select count(1) from novel_book where book_name = '%s'" % noveldata['title'])
        count = 0
        for row in cur:
            count = row[0]
            break
        if count:
           continue
        book_tag = 0
        try:
            sql = "select id from novel_booktype where book_type_name = '%s' " % noveldata['category']
            print(sql)
            cur.execute(sql)
            book_tag = 0
            for row in cur:
                book_tag = row[0]
                break
            if book_tag:
                book_tag = book_tag
            else:
                cur.execute("insert into novel_booktype (book_type_name) VALUES ('%s')" % noveldata['category'])
                continue
        except:
            pass

        add_time = strftime("%Y-%m-%d %H:%M:%S.0000", gmtime())
        print(book_tag)
        try:
            sql = "insert into novel_book (book_name, book_author, book_img, book_desc, book_website, book_index_url, book_add_time, book_tag_id, book_local_url) " \
                  "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', %d, 'Mac') " % (
                noveldata['title'], noveldata['author'], noveldata['image'], noveldata['description'],
                id, noveldata['infolink'], add_time, book_tag
            )
            cur.execute(sql)
        except Exception as e:
            print(e)
            print('保存失败 %s' % noveldata['title'])
        time.sleep(0.2)
    conn.commit()
    cur.close()
    conn.close()


def get_noveldata(id='bqg5200', content=None, url=None):
    if not content:
        raise "没有网页内容"
    soup = BeautifulSoup(content, "html.parser")
    noveldata = {}
    noveldata['infolink'] = url
    noveldata['id'] = id
    try:
        noveldata['title'] = soup.find(name='div', attrs={'class': 'booktitle'}).h1.text
    except:
        pass
    try:
        noveldata['description'] = soup.find(name='div', attrs={'id': 'bookintro'}).text.replace("ads_yuedu_txt();","").replace("\xa0\xa0\xa0\xa0","\n")
    except:
        pass
    try:
        noveldata['category'] = soup.find(name='div', attrs={'id': 'count'}).span.text
    except:
        pass
    try:
        noveldata['author'] = soup.find(name='div', attrs={'id': 'author'}).text
    except:
        pass
    try:
        noveldata['image'] = soup.find(name='div', attrs={'id': 'bookimg'}).img['src']
    except:
        pass
    print(noveldata)
    return noveldata


def get_novel_chapters():
    conn = pymysql.connect(host='119.29.201.221', port=3306, user='novelist', db='novel', password='novelist#')
    cur = conn.cursor()
    sql = "select book_id, book_website, book_index_url from novel_book "
    cur.execute(sql)
    cur2 = conn.cursor()
    for row in cur:
        book_id, book_website, book_index_url = row[0], row[1], row[2]
        cur2.execute("select count(1) from novel_bookchapter where book_id = %s " % book_id)
        chapter_count = 0
        for r in cur2:
            chapter_count = int(r[0])
        if chapter_count:
            continue
        noveldata = {}
        noveldata['id'] = book_website
        noveldata['content_link'] = book_index_url
        try:
            chapters = Save_Content(noveldata)
            if chapters == -1:
                continue
            for chapter_num, chapter in enumerate(chapters):
                # print(chapter)
                chapter_title, chapter_url = chapter
                bookchapter = None
                sql = "insert into novel_bookchapter (book_id, chapter_name, chapter_url, chapter_num, chapter_content_path) " \
                      "VALUES (%s, '%s', '%s', %s, '')" % (book_id, chapter_title, chapter_url, chapter_num)
                cur2.execute(sql)
        except Exception as e:
            print(e)
            continue
    conn.commit()
    cur.close()
    cur2.close()
    conn.close()


def save_all_chapters():
    save_dir = '/tmp/novelist/book'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    sql = "select c.book_id, c.chapter_num, c.chapter_url, c.chapter_name, b.book_website from novel_bookchapter c, novel_book b where " \
          "b.book_id = c.book_id order by c.book_id, c.chapter_num "
    conn = pymysql.connect(host='119.29.201.221', port=3306, user='novelist', db='novel', password='novelist#')
    cur = conn.cursor()
    cur.execute(sql)
    for row in cur:
        book_id, chapter_num, chapter_url, chapter_name, book_website = row
        print(book_id, chapter_num, chapter_url, book_website)
        book_dir = os.path.join(save_dir, str(book_id))
        if not os.path.exists(book_dir):
            os.mkdir(book_dir)
            with open(os.path.join(book_dir, str(chapter_num)), "w") as fw:
                content = get_chapter_content(chapter_url, book_website)
                if content == '未找到章节内容,刷新重试':
                    print('can not get the content')
                    continue
                fw.write(chapter_name+'\n'+content)
                time.sleep(0.2)
    cur.close()
    conn.close()

if __name__ == '__main__':
    save_all_chapters()