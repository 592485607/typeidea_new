from django.test import TestCase,Client
from .models import Category
import time
class CategoryTestCase(TestCase):
    # def setUp(self) -> None:
    #     Category.objects.create(
    #         name = 'models单元测试',
    #         created_time = time.time()
    #     )
    #
    # # 1 models层单元测试
    # def test_create_and_sex_show(self):
    #     category = Category.objects.create(
    #         name='huyang',
    #         created_time=time.time()
    #     )
    #     self.assertEqual(category.status, '正常', '字段内容与展示不一致')
    #     # 对于字段配置了choices，django提供不get_xxx_display方法，如get_sex_display = sex_show

    # 2 view层单元测试
    def test_get_index(self):
        # 测试首页可用性
        client = Client()
        response = client.get('/')
        # print(response.content)
        self.assertEqual(response.status_code, 200, 'status code must be 200!')
