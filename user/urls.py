from django.urls import path
from . import views
urlpatterns = [
    path('', views.user, name='user'),  # 用户管理首页
    path('getUserList', views.getUserList, name='getUserList'),  # 用户列表
    # ex: /user/5/
    path('update/', views.to_update, name='to_update'),  # 修改页
    # ex: /user/update/
    path('save', views.save, name='save'),  # 保存编辑
    path('add/', views.to_add, name='to_add')
]
