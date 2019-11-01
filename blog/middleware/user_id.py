#coding:utf-8

import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10

""" django中间件middleware在项目启动时会被初始化，等接收请求后，根据settings中的MIDDLEWARE配置顺序调用，传递request作为参数 """
class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY,uid,max_age=TEN_YEARS,httponly=True)
        return response

    def generate_uid(self,request):
        try:
            uid = request.COOKIES(USER_KEY)
        except KeyError:
            uid = uuid.uuid4().hex
        return uid


