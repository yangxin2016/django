from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def main(request):
    menus = [{'name': '主页', 'url': '/index/'}, {'name': '用户管理', 'url': '/user/'}]
    return render(request, 'main.html', {'menus': menus})

@csrf_exempt
def index(request):
    respMsg = "欢迎进入主页"
    return render(request, 'index.html', {'respMsg': respMsg})