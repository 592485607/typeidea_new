from django.shortcuts import render
from .models import Post,Tag
from django.http import HttpResponse

# def post_list(request,category_id = None,tag_id = None):
#     content = 'post_list category_id={category_id},tag_id={tag_id}'.format(
#         category_id = category_id,
#         tag_id = tag_id,
#     )
#     return HttpResponse(content)
# def post_detail(request,post_id):
#     return HttpResponse('detail')

""" 使用模板处理，render参数如下：
    request:封装HTTP请求的request对象；
    template_name:模板名称；
    context:字典数据；
    content_type:页面编码类型，默认是text/html
    status:状态码，默认是200
    using:使用哪个模板引擎解析，在setting中配置，默认django自带的模板。
 """
def post_list(request,category_id = None,tag_id = None):
    # return render(request,'blog/list.html',context={'name':'post_list'})
    """ 使用Model从数据库中批量取数据，然后展示到页面  """
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except:
            post_list = []
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            post_list = post_list.filter(category_id=category_id)
    return render(request,'blog/list.html',context={'post_list':post_list})

def post_detail(request,post_id):
    # return render(request,'blog/detail.html',context=None,content_type=None,status=None,
    #               using=None)
    """ 使用Model从数据库中批量取数据，然后展示到页面  """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post':post})