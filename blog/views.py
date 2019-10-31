from django.db.models import Q  # Django提供的条件表达式，完成复杂操作
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Tag,Category
from config.models import SideBar
from django.http import HttpResponse

from comment.forms import CommentForm
from comment.models import Comment

from django.views import View
from django.views.generic import DetailView,ListView

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
# def post_list(request,category_id = None,tag_id = None):
#     # return render(request,'blog/list.html',context={'name':'post_list'})
#     """ 使用Model从数据库中批量取数据，然后展示到页面  """
#     if tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except:
#             post_list = []
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             post_list = post_list.filter(category_id=category_id)
#     return render(request,'blog/list.html',context={'post_list':post_list})
# 7.2 完善模板信息
# def post_list(request,category_id = None,tag_id = None):
#     # return render(request,'blog/list.html',context={'name':'post_list'})
#     """ 使用Model从数据库中批量取数据，然后展示到页面  """
#     tag = None
#     category = None
#
#     if tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except Tag.DoesNotExist:
#             post_list = []
#         else:
#             post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
#             # print(post_list)
#     else:
#         post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
#         if category_id:
#             try:
#                 category = Category.objects.get(id=category_id)
#             except Category.DoesNotExist:
#                 category = None
#             else:
#                 post_list = category.filter(category_id=category_id)
#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#     }
#     return render(request,'blog/list.html',context=context)

""" 重构post_list视图：
    1.对于主函数post_list来说，只要通过tag_id拿到文章列表和tag对象
    2.造成post_list函数复杂根源是把多个URL的处理放在一起
    3.抽取两个函数处理标签和分类，定义到Model层
 """
# def post_list(request,category_id = None,tag_id = None):
#     # return render(request,'blog/list.html',context={'name':'post_list'})
#     """ 使用Model从数据库中批量取数据，然后展示到页面  """
#     tag = None
#     category = None
#
#     if tag_id:
#         post_list,tag = Post.get_by_tag(tag_id)
#     elif category_id:
#         post_list,tag = Post.get_by_tag(category_id)
#     else:
#         post_list = Post.latest_posts()
#
#     context = {
#         'category':category,
#         'tag':tag,
#         'post_list':post_list,
#         'sidebars': SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     return render(request,'blog/list.html',context=context)

# def post_detail(request,post_id=None):
#     # return render(request,'blog/detail.html',context=None,content_type=None,status=None,
#     #               using=None)
#     """ 使用Model从数据库中批量取数据，然后展示到页面  """
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     return render(request, 'blog/detail.html', context={'post':post})

# def post_detail(request,post_id=None):
#     """ 使用Model从数据库中批量取数据，然后展示到页面  """
#     try:
#         post = Post.objects.get(id=post_id)
#     except Post.DoesNotExist:
#         post = None
#     context = {
#         'post':post,
#         'sidebars':SideBar.get_all(),
#     }
#     context.update(Category.get_navs())
#     # return render(request, 'blog/detail.html', context={'post':post})
#     return render(request, 'blog/detail.html', context=context)

"""
    什么时候使用类方式实现视图逻辑，特征：代码逻辑被重复使用，同时有需要共享数据时； 
    class-based view 是一个可接受请求，返回响应的可调用对象。
    view:基础的view，实现基于HTTP方法的分发（dispatch）逻辑，比如，GET请求会调用对应的get方法
    TemplateView，继承View，是可以直接用来返回指定的模板。实现了get方法，传递变量到模板中进行数据展示
    DetailView，继承View，实现了get方法，且可绑定一个模板，获取单个实例数据
    ListView，继承View，实现了get方法，通过绑定模板来批量获取数据
    
    DetailView提供属性和接口有：
        model 属性,指定当前要使用的Model
        queryset 属性,,跟model一样，两者中选一个。设定基础数据集，Model的设定没有过滤功能，可通过queryset=
            Post.objects.fileter(status=Post.STATUS_NORMAL)进行过滤； 
        template_name 属性,，模板名称
        get_queryset 接口,同queryset方法一样，用来获取数据，如果设定了queryset，则直接返回queryset;
        get_object 接口，根据URL参数，从queryset上获取对应的实例；
        get_context_data 接口，获取渲染到模板中的上下文。
    
    ListView 跟DetailView类似，但ListView是获取多条数据； 
"""
# class MyView(View):
#     """ 好处：解耦了HTTP 方法的请求，如GET，POST...等，
#         如果需要增加POST请求逻辑，不需要修改原有函数，只需要重写即可
#     """
#     def get(self,request):
#         return HttpResponse('result')
# class PostDetailView(DetailView):
#     """ DetailView：获取1条数据 """
#     model = Post
#     template_name = 'blog/detail.html'
#     pk_url_kwarg = 'post_id'
# class PostListView(ListView):
#     """ ListView:获取多条数据"""
#     queryset = Post.latest_posts()
#     paginate_by = 1  # 设置分页，每页多少数量
#     context_object_name = 'post_list'   # 如果不设此项，在模板中需使用object_list 变量
#     template_name = 'blog/list.html'

""" 改造代码 """
class CommonViewMixin:
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars':SideBar.get_all()
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin,ListView):
    """
        queryset 中的数据需要根据当前选择的分类或标签进行过滤；
        渲染到模板中的数据需要加上当前选择的分类数据。
        故需要重写两个方法，一个是get_context_data，用来获取上下文数据并传入模板；
        一个是get_queryset,用来获取指定Model或Queryset的数据
    """
    queryset = Post.latest_posts()
    paginate_by = 3
    context_object_name = 'post_list'   # 如果不设此项，在模板中需使用object_list 变量
    template_name = 'blog/list.html'

class CategoryView(IndexView):
    """重写get_context_data，用来获取上下文数据并传入模板"""
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category,
        })
        return context

    def get_queryset(self):
        """get_queryset，根据分类过滤 """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    """重写get_context_data，用来获取上下文数据并传入模板"""
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag,pk=tag_id) # 快捷方式，获取对象实例，如不存在，则抛出404错误
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        """get_queryset，根据分类过滤 """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')  # self.kwargs中的数据其实是从URL定义中拿到的
        return queryset.filter(tag__id=tag_id)  # 跨表查询的显著特点是__双下划线

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,**kwargs):
        """通过View层把CommentForm和评论的数据传递到模板层"""
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form':CommentForm,
            'comment_list':Comment.get_by_target(self.request.path),
        })
        return context

# 增加搜索功能
class SearchView(IndexView):
    """重写get_context_data，用来获取上下文数据并传入模板"""
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword':self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        """get_queryset，根据分类过滤 """
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

# 增加作者页面
class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


