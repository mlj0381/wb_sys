"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import search
urlpatterns = [
    #跳转页面
    path('', views.admin),
    path('sign/', views.admin),
    path('table/',views.head),
    path('hotspot/',views.hotsport),
    path('analysis/',views.analysis),
    path('testing/',views.testing),
    path('view/',views.view),
    path('task/',views.task),
    path('task2/',views.task2),
    path('perinfo/',views.perinfo),

    #请求任务

    #登录检查
    path('sign_check/',search.sign),

    #检查登录状态
    path('check_statu/',search.check_statu),
    #请求首页数据
    path('get_home_data/',search.get_home_data),

    #请求分析数据
    path('analysis_data/',search.analysis_data),

    #请求帖子数据
    path('testing_data/',search.testing_data),

    #请求帖子页数
    path('testing_page/',search.testing_page),

    #概览页面信息
    path('view_data/',search.view_data),

    #舆论热点
    path('hot_data/',search.hot_data),

    #查询超话是否存在
    path('search_ch_name/',search.search_ch_name),

    #得到任务
    path('get_task_queue/',search.get_task_queue),

    #改变任务状态
    path('change_task_statu/',search.change_task_statu)

]
