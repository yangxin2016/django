from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from . import admin,menu
import json

# 模拟登录用户
admins = []
for i in range(1, 10):
    adminUser = admin.Admin("%s@qq.com" % i, 'password%d' % i, 'super')
    admins.append(adminUser)


def to_home():
    redirect("/home")


# 主页
def home(request):
    menus = []
    menu1 = menu.Menu(1, "主页", '/index/', None, "icon-home")
    menu2 = menu.Menu(2, '系统管理', None,
                      [menu.Menu(3, '用户管理', '/user/', None, "icon-user"),
                       menu.Menu(4, '角色管理', '/role/', None, "icon-user-md")], "icon-cog")
    menus.append(menu1)
    menus.append(menu2)
    return render(request, 'home.html', {'menus': menus})


# 登录页
def login(request):
    if request.session.get('sessionUser', None) is not None:
        # json转字典
        admin_dic = json.loads(request.session['sessionUser'])
        sessionUser = admin.Admin(admin_dic['email'], None, admin_dic['role'])
        sessionUser.printAdmin()
        return redirect("/home")
    else:
        return render(request, 'login.html')


# 提交登录
@csrf_exempt
def doLogin(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    for admin in admins:
        if admin.email == email and admin.password == password:
            # 对象转字典再转json
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


# 注销登录
def logout(request):
    if request.session.get('sessionUser', None) is not None:
        request.session['sessionUser'] = None
    return redirect("/login")