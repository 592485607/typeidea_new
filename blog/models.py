from django.contrib.auth.models import User
from django.db import models

""" 存放内容相关数据"""
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    name = models.CharField(max_length=50,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    """ 获取分类,区分是否为导航，问题是会产生两次数据库请求，数据量小时可用if判断,
        避免因queryset的懒惰性产生两次I/O操作 
    """
    @classmethod
    def get_navs(cls):
        # 这样只需查一次数据库，拿到数据后，在内存中处理数据
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        # nav_categories = categories.filter(is_nav = True)
        # normal_categories = categories.filter(is_nav = False)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL,'正常'),
        (STATUS_DELETE,'删除'),
    )

    name = models.CharField(max_length=10,verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')  # blank 业务层面允许为空；Null为数据库层面
    content = models.TextField(verbose_name='正文',help_text='正文必须为MarkDown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    category = models.ForeignKey(Category,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    owner = models.ForeignKey(User,verbose_name='作者')
    created_time  = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    """ 调整模型，增加字段pv,uv，统计文章访问量 """
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        # 通过Meta配置它的展示名称为文章，排序规则根据 id 进行降序排列
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    """ 把获取最新文章(post)数据的操作放到Model层,
        select_related方式解决部分链式查询N+1问题
     """
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL)\
                .select_related('owner','category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=Post.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

