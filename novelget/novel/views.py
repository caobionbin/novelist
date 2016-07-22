# coding=utf-8

import os
import os.path


from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.utils.http import urlquote
from django.template import RequestContext

from .models import SearchHistory, BookType, Book, BookChapter
from .findbookinbaidu import findbook, getbook
from .fetch_novel import Search_By_ID, Get_Novel_Info, Save_Content, Get_ID, get_chapter_content, escape
# Create your views here.


def index(request):
    return render_to_response('novel/search.html')
    # return redirect('http://www.xs111.com/')


def search(request):

    # print(Get_ID())
    mycontext = {}
    if 'bookname' in request.GET and request.GET['bookname']:
        bookname = request.GET['bookname']
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        searchhistory = SearchHistory(bookname=bookname, ip=ip)
        searchhistory.save()
        noveldata = {}
        try:
            book = Book.objects.get(book_name=bookname)
            book_id = book.book_id
            bookname = book.book_name
            book_author = book.book_author
            book_img = book.book_img
            book_website = book.book_website
            book_url = book.book_index_url
            book_desc = book.book_desc
            book_tag = book.book_tag
            try:
                book_tag.book_type_name
            except:
                book_tag = '暂无标签'
        except Book.DoesNotExist:
            print('cannot find local book, fetch from website')
            novelurl = 0
            for id in Get_ID():
                novelurl = Search_By_ID(novelname=bookname, id=id)
                if novelurl == -1 or novelurl == -2:
                    continue
                noveldata = Get_Novel_Info(novelurl, id)
                # print(noveldata)
                if noveldata.get('title', None):
                    break
            # print(novelurl)
            if novelurl == -1 or novelurl == -2 or not noveldata.get('title', None):
                mycontext['nobook'] = False
                return render_to_response('novel/search_result.html', context=mycontext,
                                          context_instance=RequestContext(request))

            # 如果查询结果的书本名称和查询请求不一致,将重新判断novel_book里是否已经存在该书
            if bookname != noveldata.get('title', None):
                try:
                    book = None
                    book = Book.objects.filter(book_name=noveldata.get('title', None)).first()
                except:
                    pass
                if book:
                    mycontext.update({'book': book})
                    return render_to_response('novel/search_result.html', context=mycontext,
                                              context_instance=RequestContext(request))

            # print('website: %s' % novelurl)
            # for key, value in noveldata.items():
            #     print(key+':'+value)
            booktype = None
            if 'category' in noveldata.keys():
                try:
                    booktype = BookType.objects.get(book_type_name=noveldata['category'])
                except BookType.DoesNotExist:
                    booktype = BookType(book_type_name=noveldata['category'])
                    booktype.save()
                except:
                    pass
            try:
                bookname = noveldata['title']
                book_author = noveldata.get('author', '')
                book_img = noveldata.get('image', '')
                book_website = noveldata.get('id', '')
                if 'content_link' in noveldata.keys():
                    book_url = noveldata['content_link']
                else:
                    book_url = noveldata['infolink']
                book_desc = noveldata.get('description', '暂无简介')
                book_tag = booktype
                book = Book(book_name=bookname, book_author=book_author, book_desc=book_desc, book_img=book_img, book_website=book_website,
                            book_index_url=book_url, book_tag=book_tag)
                book_tag = noveldata.get('category', '')
                # print(bookname)
                print(book_img)
                book.save()
                book_id = book.book_id
            except Exception as e:
                print('save book info error: %s ' % e)
                mycontext['nobook'] = False
                return render_to_response('novel/search_result.html', context=mycontext,
                                          context_instance=RequestContext(request))
        # print(book_url)
        mycontext.update({'book': book})
        return render_to_response('novel/search_result.html', context=mycontext, context_instance=RequestContext(request))
    else:
        mycontext['nobook'] = True
        return render_to_response('novel/search_result.html', context=mycontext, context_instance=RequestContext(request))


def book_index(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
        chapters = BookChapter.objects.filter(book=book).order_by('chapter_num')
        book_type = book.book_tag.book_type_name
        return render_to_response('novel/book_index.html', {'book': book, 'chapters': chapters, 'book_type': book_type})
    except Book.DoesNotExist:
        print('book does not exist')
        return redirect('/')
    # except Exception as e:
    #     print(e)
    #     print('获取书籍章节信息出错')
    #     return redirect('/')


def update(request, book_id):
    try:
        book = Book.objects.get(book_id=book_id)
        # print(book.book_name, book.book_website, book.book_index_url)
        noveldata = {}
        noveldata.update({'id': book.book_website})
        noveldata.update({'content_link': book.book_index_url})
        chapters = Save_Content(noveldata=noveldata)
        for chapter_num, chapter in enumerate(chapters):
            # print(chapter)
            chapter_title, chapter_url = chapter
            bookchapter = None
            try:
                bookchapter = BookChapter.objects.filter(book=book).filter(chapter_num=chapter_num).first()
            except:
                pass
            if not bookchapter:
                bookchapter = BookChapter(book=book, chapter_name=chapter_title, chapter_url=chapter_url, chapter_num=chapter_num)
                bookchapter.save()
        return redirect('book_index', book_id=book_id)
    except Book.DoesNotExist:
        print('book does not exist')
        return redirect('/')


def chapter(request, book_id, chapter_num):
    print(book_id, chapter_num)
    mycontext = {}
    try:
        book = Book.objects.get(book_id=book_id)
        chapter_count = BookChapter.objects.filter(book=book).count()
        chapter = BookChapter.objects.filter(book=book).filter(chapter_num=chapter_num).first()
        book_website = book.book_website
        chapter_name = chapter.chapter_name
        chapter_url = chapter.chapter_url
        content = get_chapter_content(chapter_url, book_website)
        # content
        # content = escape(content)
        mycontext.update({'book_id': book.book_id})
        mycontext.update({'book_name': book.book_name})
        mycontext.update({'chapter_name': chapter_name})
        mycontext.update({'chapter_content': content})
        if int(chapter_num) > 0:
            mycontext.update({'previous_chapter_num': str(int(chapter_num)-1)})
        if int(chapter_num) < chapter_count - 1:
            mycontext.update({'next_chapter_num': int(chapter_num) + 1})

        # print(mycontext['chapter_content'])
        # book.get_next_by_pk
        return render_to_response('novel/chapter.html', context=mycontext)
    except Book.DoesNotExist:
        return redirect('/')
    except:
        mycontext.update({'error': 'fetch content error, please reclick..'})
        return redirect('/book/%s' % book_id)
    # except Exception as e:
    #     print(e)
    #     return redirect('/book/%s'%book_id)


def read(request, booknumber):
    # print(bookname, booknumber)
    chapter_list = getbook(booknumber)

    return render_to_response('novel/read_index.html', {'chapter_list': chapter_list})


def download(request, book_id):

    book = Book.objects.get(pk=book_id)
    file_name = book.book_name + '.txt'
    print(file_name)
    def downloadbook():
        chapters = BookChapter.objects.filter(book=book).order_by('chapter_num')
        for chapter in chapters:
            title = chapter.chapter_name
            content = get_chapter_content(chapter_url=chapter.chapter_url, book_website=book.book_website)
            yield title + '\n' + content

    response = StreamingHttpResponse(downloadbook())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(file_name))
    return response


def toplist(request):
    if Book.objects.count() < 100:
        books = Book.objects.all()
    else:
        books = Book.objects.all()[99]
    return render_to_response('novel/toplist.html', {'books': books})