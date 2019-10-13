from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    抽象出一个基类BaseOwnerAdmin，重写save方法（需设置对象的owner）,重写get_queryset方法（展示列表数据）
    1.用来自动补充文章，分类，标签，侧边栏，友链这些Model的owner字段
    2.用来针对queryset过滤当前用户的数据
    """

    # 指定哪些字段不展示
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        """
        重写 save_model方法, Given a model instance save it to the database.
         request.user为当前登录的用户
         request为当前请求，obj为当前要保存的对象，form是页面提交过来的表单之后的对象，change是标志保存的数据是新增还是更新；

        """
        obj.owner = request.user
        return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)

    def get_queryset(self, request):
        """ 只能查看到作者为自己的数据 """
        qs = super(BaseOwnerAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)