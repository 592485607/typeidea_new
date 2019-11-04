"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# from blog.views import post_list,post_detail
# from config.views import links
from .custom_site import custom_site

"""
    URL参数解释
    url(<正则或字符串>,<view funtion>,<固定参数context>,<url的名称>)
"""
# urlpatterns = [
#     url(r'^$', post_list),   # 用户访问博客首页，把请求传递到post_list函数中
#     url(r'^category/(?P<category_id>\d+)/$', post_list), # (?P<category_id>\d+) 带分组正则表达
#     url(r'^tag/(?P<tag_id>\d+)/$', post_list),
#     url(r'^post/(?P<post_id>\d+).html$', post_detail),
#     url(r'^links/$', links),
#
#     url(r'^super_admin/', admin.site.urls),
#     url(r'^admin/', custom_site.urls),     # 基于URL上划分两套后台地址，一套管理用户，另一套管理业务
# ]

"""
    reverse作用，通过name反向解析到URL地址;
    在URL定义中增加name
"""
# urlpatterns = [
#     url(r'^$', post_list, name='index'),  # 用户访问博客首页，把请求传递到post_list函数中
#     url(r'^category/(?P<category_id>\d+)/$', post_list,name='category-list'), # (?P<category_id>\d+) 带分组正则表达
#     url(r'^tag/(?P<tag_id>\d+)/$', post_list,name='tag-list'),
#     url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),
#     url(r'^links/$', links,name='links'),
#     url(r'^super_admin/', admin.site.urls, name='super-admin'),
#     url(r'^admin/', custom_site.urls, name='dmin'),     # 基于URL上划分两套后台地址，一套管理用户，另一套管理业务
#
#     # url(r'^about/$', TemplateView.as_view(template_name="about.html")),
#     # url(r'^post/(?P<pk>\d+).html$', PostDetailView.as_view(),name='post-detail'),
# ]

"""使用类视图定义URL"""
# from blog.views import MyView,PostDetailView
# from django.views.generic import TemplateView
# urlpatterns = [
#     # url(r'^about/$', MyView.as_view()),  # 通过as_view函数接受请求并返回响应
#     url(r'^about/$', TemplateView.as_view(template_name="about.html")),
#     url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
#
#     url(r'^super_admin/', admin.site.urls, name='super-admin'),
#     url(r'^admin/', custom_site.urls, name='dmin'),     # 基于URL上划分两套后台地址，一套管理用户，另一套管理业务
# ]

from blog.views import (
    IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView,
)
from config.views import (
    LinkListView,
)
from comment.views import (
    CommentView,
)
from django.contrib.sitemaps import views as sitemap_views
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(),name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^links/$', LinkListView.as_view(),name='links'),
    url(r'^comment/$', CommentView.as_view(),name='comment'),
    url(r'^rss|feed/', LatestPostFeed(),name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),

    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^admin/', custom_site.urls, name='dmin'),     # 基于URL上划分两套后台地址，一套管理用户，另一套管理业务
]