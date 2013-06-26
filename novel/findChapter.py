from urllib import request
from bs4 import BeautifulSoup
from time import sleep

from models import *

def findChapter(main_url):

    html = open('zzjs_total.htm','r').read()
    soup = BeautifulSoup(html)

    posts = soup.find_all('div',{'class' : "d_post_content j_d_post_content"})

    '''zds on the website add a commit .'''
