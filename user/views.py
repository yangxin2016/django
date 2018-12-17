from django.core.paginator import Paginator
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import Http404

logging.basicConfig(level=logging.DEBUG) #  设置日志级别，只有高于debug级别的日志能输出


#  用户模块主页
@csrf_exempt  #此注解保证post请求通过CRSF验证
def index(request):
    return render(request, 'users/index.html')

totalPage = 0


#  列表页
@csrf_exempt
def list(request):
    page = int(request.POST.get('page'))
    if page is None:
        page = 1
    pageSize = request.POST.get('pageSize')
    if pageSize is None:
        pageSize = 1
    logging.info("page:%d,pageSize:%d", page, int(pageSize))
    all_user_list = User.objects.order_by('update_time').all()
    paginator = Paginator(all_user_list, int(pageSize))
    try:
        user_list = paginator.page(page)
    except:
        user_list = []
    return render(request, 'users/user_list.html', {'user_list': user_list, "totalCount": paginator.count, 'page': paginator.page(page), 'currentPage': int(page)})


#  跳转编辑页
@csrf_exempt
def to_update(request):
    try:
        user = User.objects.get(pk=request.POST.get('id'))
    except user.DoesNotExist:
        raise Http404("用户不存在")
    return render(request, 'users/update.html', {'user': user})


#  跳转新增页
@csrf_exempt
def to_add(request):
    return render(request, 'users/add.html')


#  保存新增或修改结果
@csrf_exempt
def save(request):
    id = request.POST.get('id')
    user_name = request.POST.get('user_name')
    sex = request.POST.get('sex')
    age = request.POST.get('age')
    address = request.POST.get('address')
    logging.info(id, user_name, sex, age, address)
    resp = {}
    try:
        user = None
    #    raise Exception("出错啦.....")   #模拟异常处理
        if id is None:
            user = User()
            user.user_name = user_name
            user.sex = sex
            user.age = age
            user.address = address
        else:
            try:
                user = User.objects.get(pk=id)
                user.user_name = user_name
                user.sex = sex
                user.age = age
                user.address = address
            except user.DoesNotExist:
                raise Http404("用户已经不存在了")
        user.save()
        resp = {'status': '0000', 'respMsg': '保存成功'}
    except Exception as e:
        resp = {'status': '0001', 'respMsg': '保存失败，原因：'+str(e)}
    return JsonResponse(resp)
