from django.contrib.admin import AdminSite

"""
    自定制Site，通过定制site实现一个系统对外提供多套admin后台的逻辑
    如需求，用户模块的管理应跟文章分类等数据的管理分开。
"""
class CustomSite(AdminSite):
    site_header = 'Typeidea'
    site_title = 'Typeidea 管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')