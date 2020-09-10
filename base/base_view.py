# -*- coding:utf-8 -*-
import traceback
import abc
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect


class BaseView(View, metaclass=abc.ABCMeta):
    """
        all request view parent view
    """

    # 继承该类的子类，共用参数
    __solts__ = ['request_params',  # get或post请求相关的参数集合
                 'request_meta',  # 每次请求的一些服务参数，如ip等
                 'request_cookies',  # 请求带上的cookies
                 ]

    def post(self, request):
        self.prepare(request)
        return self.__run(request)

    def get(self, request):
        self.prepare(request)
        return self.__run(request)

    def __get_request_params(self, request):
        """
        封装请求参数，无论是get, post，都统一到一个参数集合
        :param request:
        :return request_params: {key: value}
        """
        # 统一参数遍历
        request_params = dict([(k, v) for k, v in list(request.GET.items())])
        if request.method == "POST":
            post_params = dict([(k, v) for k, v in list(request.POST.items())])
            request_params.update(post_params)
        return request_params

    def __get_resp(self, request):
        # 初始化请求数据返回结构
        return {
            'code': 200,
            'msg': '',
            'data': {},
        }

    def prepare(self, request):
        """
            完成一些初始化的工作
            :param request:
            :return:
        """

        # meta数据
        self.request_meta = request.META
        self.request_cookies = request.COOKIES

        # 初始化返回的结果json
        # 初始化返回的结果json
        self.resp = self.__get_resp(request)
        # 解析request中的请求参数，让业务方忽略GET/POST请求对应的参数传递问题
        self.request_params = self.__get_request_params(request)
        # 初始化页面跳转默认参数
        self.__redirect_url = None

    def __run(self, request):
        self.token = request.META.get("HTTP_X_TOKEN")
        if not self.token or self.token != 'admin-token':
            self.set_error(201, 'access defined is fail')
            return self.finish(request)
        try:
            resp_data = self.do_logic(request)
        except:
            error_data = traceback.format_exc()
            self.set_error(500, error_data)
            resp_data = {}
        self.set_data(resp_data)
        return self.finish(request)

    @abc.abstractmethod
    def do_logic(self, request):
        """
            重写业务逻辑
        """
        return []

    def set_redirect(self, url):
        """
            设置页面跳转url
        """
        self.__redirect_url = url

    def set_error(self, code, msg=''):
        """
            设置错误码及错误信息
        """
        self.resp['code'] = code
        self.resp['msg'] = msg

    def set_data(self, resp_data):
        """
            # 设置返回数据
        """
        self.resp['data'] = resp_data

    def finish(self, request):
        """
            清理请求完成之后的相关事项
        """
        if self.__redirect_url:
            return HttpResponseRedirect(self.__redirect_url)
        else:
            response = JsonResponse(self.resp)
            return response
