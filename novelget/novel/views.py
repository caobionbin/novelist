# coding=utf-8

import os
import os.path


from django.shortcuts import render_to_response
from django.http import HttpResponse, StreamingHttpResponse

from novelget.novel.models import SearchHistory
from .findbookinbaidu import findbook, getbook, downloadbook
# Create your views here.


def index(request):
    return render_to_response('novel/search.html')


def search(request):

    if 'bookname' in request.GET and request.GET['bookname']:
        bookname = request.GET['bookname']
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        searchhistory = SearchHistory(bookname=bookname, ip=ip)
        searchhistory.save()
        results = findbook(bookname)
        # results = findbookinbaidu(bookname)
        return render_to_response('novel/search_result.html', {'bookname': bookname, 'results': results})
    else:
        return HttpResponse('输入你想要搜的书名...')


def read(request, booknumber):
    # print(bookname, booknumber)
    chapter_list = getbook(booknumber)

    return render_to_response('novel/read_index.html', {'chapter_list': chapter_list})


def download(request, booknumber):

    file_name = '%s.txt' % booknumber
    response = StreamingHttpResponse(downloadbook(booknumber))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response


def list(request):

    path = '/Users/zhangdesheng/Documents/python-learning/zds-git/novelist/novelget/novel/templates/novel'
    files = []
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            files.append(f)
    return render_to_response('novel/listfile.html', {'files': files})