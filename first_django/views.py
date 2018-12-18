from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import admin
import json

admins = []
for i in range(1, 10):
    adminUser = admin.Admin("%s@qq.com" % i, 'password%d' % i, 'super')
    admins.append(adminUser)


def home(request):
    menus = [{'name': '主页', 'url': '/index/'}, {'name': '用户管理', 'url': '/user/'}]
    return render(request, 'main.html', {'menus': menus})


def login(request):
    if request.session.get('sessionUser', None) is not None:
        admin_dic = json.loads(request.session['sessionUser'])
        sessionUser = admin.Admin(admin_dic['email'], None, admin_dic['role'])
        sessionUser.printAdmin()
        return redirect("/home")
    else:
        return render(request, 'login.html')

@csrf_exempt
def doLogin(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    for admin in admins:
        if admin.email == email and admin.password == password:
            request.session['sessionUser'] = json.dumps(admin.__dict__)
            status = '0000'
            msg = 'success'
            return JsonResponse({'status': status, 'msg': msg})

    status = '0001'
    msg = '用户名或密码错误'
    return JsonResponse({'status': status, 'msg': msg})





@csrf_exempt
def index(request):
    respMsg = "欢迎进入主页"
    return render(request, 'index.html', {'respMsg': respMsg})