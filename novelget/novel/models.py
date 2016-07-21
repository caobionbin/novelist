# coding=utf-8

from django.db import models

# Create your models here.


class SearchHistory(models.Model):
    bookname = models.CharField(max_length=100, verbose_name='书名')
    ip = models.CharField(max_length=20, verbose_name='访问ip', blank=True)
    searchtime = models.DateTimeField(auto_now_add=True, verbose_name='搜索时间')


class BookType(models.Model):
    book_type_name = models.CharField(max_length=50, verbose_name='书本分类')


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100, verbose_name='书名')
    book_author = models.CharField(max_length=50, verbose_name='作者', default='暂无作者信息')
    book_img = models.CharField(max_length=200, verbose_name='封面地址', default='')
    book_desc = models.CharField(max_length=1000, verbose_name='简介', default='')
    book_website = models.CharField(max_length=100, verbose_name='书本来源站点')
    book_index_url = models.CharField(max_length=200, verbose_name='书本主页')
    book_local_url = models.CharField(max_length=200, verbose_name='本地文件绝对路径', default='')
    book_add_time = models.DateTimeField(verbose_name='书本入库时间', auto_now_add=True)
    book_tag = models.ForeignKey(BookType, blank=True, null=True)
    # baidu_rank = models.IntegerField(verbose_name='百度排行榜排名', blank=True, default='')


class BookChapter(models.Model):
    book = models.ForeignKey(Book)
    chapter_name = models.CharField(max_length=100, verbose_name='章节名称')
    chapter_url = models.CharField(max_length=200, verbose_name='章节地址')
    chapter_num = models.IntegerField(verbose_name='章节序号')
    chapter_content_path = models.CharField(max_length=100, verbose_name='内容路径', default='')