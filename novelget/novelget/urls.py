"""novelget URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'novel.views.index', name='index'),
    url(r'^search/', 'novel.views.search', name='search'),
    url(r'^read/(\d+)', 'novel.views.read', name='read'),
    url(r'^book/(?P<book_id>[0-9]+)/$', 'novel.views.book_index', name='book_index'),
    url(r'^update/(?P<book_id>[0-9]+)/$', 'novel.views.update', name='update'),
    url(r'^book/(?P<book_id>[0-9]+)/(?P<chapter_num>[0-9]+)/$', 'novel.views.chapter', name='chapter'),
    # url(r'^articles/(?P<year>[0-9])/$', views.year_archive),
    # url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^download/(\d+)', 'novel.views.download', name='download'),
    url(r'^toplist/$', 'novel.views.toplist', name='toplist'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
