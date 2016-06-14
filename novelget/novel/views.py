from django.shortcuts import render_to_response
from django.http import HttpResponse

from .findbook import findbook
# Create your views here.

def index(request):
    return render_to_response('novel/search.html')

def search(request):

    if 'bookname' in request.GET and request.GET['bookname']:
        bookname = request.GET['bookname']
        results = findbook(bookname)
        return render_to_response('novel/search_result.html', {'bookname': bookname, 'results': results})
    else:
        return HttpResponse('输入你想要搜的书名...')
