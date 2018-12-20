from django.core.paginator import Paginator
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import Http404
import json


logging.basicConfig(level=logging.DEBUG) #  设置日志级别，只有高于debug级别的日志能输出


#  用户模块主页
@csrf_exempt  #此注解保证post请求通过CRSF验证
def user(request):
    return render(request, 'users/user.html')

totalPage = 0

#  列表
@csrf_exempt
def getUserList(request):
    params = json.loads(request.body)
    page = params.get('pageNumber')
    if page is None:
        page = 1
    pageSize = params['pageSize']
    if pageSize is None:
        pageSize = 1

    keyword = ''
    if 'keyword' in params:
        keyword = params['keyword']

    logging.info("page:%d,pageSize:%d", page, int(pageSize))
    all_user_list = User.objects.filter(user_name__icontains=keyword)
    paginator = Paginator(all_user_list, pageSize)
    rows = []
    for i in paginator.page(page):
        user={}
        user['id'] = i.id
        user['user_name'] = i.user_name
        user['age'] = i.age
        user['sex'] = i.sex
        user['address'] = i.address
        user['create_time'] = i.create_time
        user['update_time'] = i.update_time
        rows.append(user)
    resp = {'status': '0000', 'content': {'total': paginator.count, 'rows': rows}}
    return JsonResponse(resp)


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

#删除
@csrf_exempt
def delete(request):
    ids = request.POST.get('ids').split(',')
    print(ids)
    status = '0000'
    msg = '删除成功'
    for id in ids:
        try:
            user = User.objects.get(pk=id)
            if user is not None:
                user.delete()
        except Exception as e:
            status = '0001'
            msg = '删除失败'
    res = {'msg': msg, 'status': status}
    return JsonResponse(res)
