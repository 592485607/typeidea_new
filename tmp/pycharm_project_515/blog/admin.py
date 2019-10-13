from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post,Category,Tag
from .adminforms import PsotAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin

""" 在同一页面编辑关联的数据，如在分类页面直接编辑文章 """
class PostInline(admin.TabularInline):  # TabularInline 样式不同，可选择继承admin.StackedInline获取不同的展示样式
    fields = ('title','desc','status',)
    extra = 1   # 控制额外多几个
    model = Post

@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):  # class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline,]

    list_display = ('name','status','is_nav','owner','created_time','post_count')
    fields = ('name','status','is_nav')

    # def save_model(self, request, obj, form, change):
    #     """
    #     重写 save_model方法, Given a model instance save it to the database.
    #      request.user为当前登录的用户
    #      request为当前请求，obj为当前要保存的对象，form是页面提交过来的表单之后的对象，change是标志保存的数据是新增还是更新；
    #     """
    #     obj.owner = request.user
    #     # print(obj.owner)
    #     return super(CategoryAdmin,self).save_model(request,obj,form,change)

    # 展示该分类有多少篇文章的统计
    def post_count(self,obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

@admin.register(Tag,site=custom_site)  # admin.site.register(Tag,TagAdmin)
class TagAdmin(BaseOwnerAdmin): # class TagAdmin(admin.ModelAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')

    # def save_model(self, request, obj, form, change):
    #     """
    #      Given a model instance save it to the database.
    #     """
    #     obj.owner = request.user
    #     return super(TagAdmin,self).save_model(request,obj,form,change)
    #
    # def get_queryset(self, request):
    #      qs = super().get_queryset(request)
    #      return qs.filter(owner=request.user)

class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器，只展示当前用户分类. P119"""
    title = "分类过滤"
    parameter_name = 'owner_category'   #查询时URL参数的名称，如查询分类id为1时，URL后面的Query部分是 ?owner_category=1

    def lookups(self, request, model_admin):
        """返回要展示的内容和查询用的id（如?owner_category=1) """
        return Category.objects.filter(owner=request.user).values_list('id','name')

    """
        The get_queryset method on a ModelAdmin returns a QuerySet of all model instances that can be edited by the admin site. 
    """
    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset

@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin): #  class PostAdmin(admin.ModelAdmin)
    # 引用自定义Form
    form = PsotAdminForm

    # 配置列表页面展示哪些字段
    list_display = [
        'title','category','status',
        'created_time','owner','operator',
    ]

    # 配置哪些字段可以作为链接，点击它们，进入编辑页面
    list_display_links = ['title']

    # 配置页面过滤器，需要哪些字段来过滤列表页
    list_filter = [CategoryOwnerFilter]

    # 配置搜素字段
    search_fields = ['title','category__name']

    # 动作执行的相关配置，是否展示在顶部，底部
    actions_on_top = True
    actions_on_bottom = False

    # 保存，保存并增加，保存并继续编辑，按钮是否在顶部展示
    save_on_top = True

    # 新增时，指定哪些字段不展示
    exclude = ('owner',)

    # fields有两个作用，1是限定要展示的字段，2是指定要展示的字段顺序
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    """ fieldsets 用来控制页面展示的布局，要求格式是有两个元素的tuple的list """
    fieldsets = (
        ('基础配置',{
            'description':'基础配置的文字描述说明',
            'fields':(
                ('title','category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collapse',),    # classes 配置板块上加上CSS属性，如collapse和wide
            'fields':('tag',),
        })
    )

    # filter_horizontal = ('tag',)   # 控制多对多字段横向展示
    filter_vertical = ('tag',)   # 控制多对多字段纵向展示

    # 展示自定义字段
    def operator(self,obj):
        return format_html(
            '<a href = "{}">编辑</a>',
            # reverse('admin:blog_post_change',args=(obj.id,))
            reverse('cus_admin:blog_post_change',args=(obj.id,))  # 来源custom_site.py中的 custom_site = CustomSite(name='cus_admin')
        )
    operator.short_description = '操作'    # 指定表头的展示文案

    # def save_model(self, request, obj, form, change):
    #     """
    #     Given a model instance save it to the database.
    #     """
    #     obj.owner = request.user
    #     return super(PostAdmin,self).save_model(request,obj,form,change)
    #
    # def get_queryset(self, request):
    #     """ 只能查看到作者为自己的数据 """
    #     qs = super(PostAdmin,self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    """ 自定义静态资源引入，
        通过自定义的Media类来往页面上增加想要添加的javaScript及CSS资源 
    """
    # class Media:
    #     css = {
    #         'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
    #     }
    #     js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

# from django.contrib.admin.models import LogEntry
# from django.contrib.admin.options import get_content_type_for_model
#
# # 查询某个对象的变更，如，以下拿到文章id为1的所有变更记录
# post = Post.objects.get(id=1)
# log_entries = LogEntry.objects.filter(
#     content_type_id = get_content_type_for_model(post).pk,
#     object_id = post.id,
# )


"""
    LogEntry.action_time:    The date and time of the action.
    
    LogEntry.user:   The user (an AUTH_USER_MODEL instance) who performed the action.
    
    LogEntry.content_type:  The ContentType of the modified object.

    LogEntry.object_id: The textual representation of the modified object’s primary key.

    LogEntry.object_repr: The object`s repr() after the modification.
"""
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','content_type','user',
                    'change_message']