from django.db import models
from django.contrib import admin


class Book(models.Model):
    bookname = models.CharField(max_length=30,unique=True)
    bookaddr = models.URLField(max_length=100)
    def __str__(self):
        return str(self.bookname)


class Chapter(models.Model):
    bookname = models.ForeignKey(Book)
    chaptername = models.CharField(max_length=50,verbose_name='章节名称')
    tiebaPage = models.URLField(max_length=100,verbose_name='贴吧阅读地址')
    chapterId = models.IntegerField()
    is_save = models.BooleanField(default=False)
    updateTime = models.DateTimeField()

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('chaptername','bookname','tiebaPage','is_save','updateTime',)
    ordering = ('-tiebaPage',)
    list_filter = ('chaptername','bookname','updateTime')

admin.site.register(Chapter,ChapterAdmin)

