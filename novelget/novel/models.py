# coding=utf-8

from django.db import models

# Create your models here.


class SearchHistory(models.Model):
    bookname = models.CharField(max_length=50, verbose_name='书名')
    ip = models.CharField(max_length=20, verbose_name='访问ip', blank=True)
    searchtime = models.DateTimeField(auto_now_add=True, verbose_name='搜索时间')
