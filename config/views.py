from django.views.generic import ListView

from blog.views import CommonViewMixin
from .models import Link

from django.shortcuts import render
from django.http import HttpResponse

# def links(request):
#     return HttpResponse('links')

# Ôö¼ÓÓÑÁ´
class LinkListView(CommonViewMixin,ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'