from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    抽象出一个基类BaseOwnerAdmin，重写save方法（需设置对象的owner）,重写get_queryset方法（展示列表数据）
    1.用来自动补充文章，分类，标签，侧边栏，友链这些Model的owner字段
    2.用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.owner = request.user
        return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin,self).get_queryset(request)
        return qs.filter(owner=request.user)