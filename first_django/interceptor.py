from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

url_filter_paths = ['/login','/doLogin']

'''登录拦截器'''
class Interceptor(MiddlewareMixin):
    def process_request(self, request):
        session_user = request.session.get('sessionUser', None)
        if url_filter_paths.count(request.path) == 0 and session_user is None:
            return HttpResponseRedirect("/login")
        else:
            pass
