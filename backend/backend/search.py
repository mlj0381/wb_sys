
from .SQL import user_sign
from .SQL.check_statu import statu
from .SQL.get_data import get_data
from .SQL.check_ch_name import check_name
from .SQL.change_task_statu import change_statu

from django.http import HttpResponse,JsonResponse
from django.shortcuts import render


from bson import json_util

import json

def sign(request):
    sign = user_sign.sign().main(request.GET['account'],request.GET['passwd'],request.GET['cookie'])
    if(sign):
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})

def check_statu(request):
    sign = statu().main(request.GET['cookie'])
    if(sign):
        return JsonResponse(sign)
    else:
        return JsonResponse({'statu':0})

def get_home_data(request):
    datas = get_data().get_home_data(request.GET['user_id'])
    return JsonResponse(datas)

def analysis_data(request):
    data = get_data().get_analysis_data(request.GET['Ch_name'],request.GET['date'],request.GET['cookie'])
    if(data):
        print(data)
        dic = {'post_num': data['post:num'],"comment_num":data['comment_num'],"grade":data['grade'],"active_time":data['active_time'],
               'hot_words':data['hot_words'],"map":data['map'],"sex_ration":data['sex_ratio'],"age":data['age'],'statu':1}
        return JsonResponse(dic)
    else:
        return JsonResponse({'statu':0})

def testing_data(request):
    data=get_data().get_testing_data(request.GET['Ch_name'],request.GET['date'],request.GET['page'],request.GET['key_word'],request.GET['attitude'],request.GET['cookie'])
    print(request.GET['cookie'], request.GET['Ch_name'], request.GET['date'], request.GET['attitude'],
          request.GET['key_word'] == '', request.GET['page'])

    return JsonResponse({'statu':1,'number':data[1],'data':data[0]})

def testing_page(request):
    page = get_data().get_iniv_number(request.GET['Ch_name'],request.GET['date'],request.GET['attitude'],request.GET['key_word'],request.GET['cookie'])
    return JsonResponse({'page': page})

def view_data(request):
    data=get_data().get_view_data(request.GET['cookie'])
    return JsonResponse({'data': data})

def hot_data(request):
    data = get_data().get_hot_data(request.GET['cookie'],request.GET['Ch_name'],request.GET['date'])
    return JsonResponse({'data': data})

def search_ch_name(request):
    statu = check_name().main(request.GET['cookie'],request.GET['Ch_name'])
    return JsonResponse({"statu":statu})

def get_task_queue(request):
    data =get_data().get_task_queue(request.GET['cookie'])
    return JsonResponse({'data':data})

def change_task_statu(request):
    change_statu().main(request.GET['Ch_name'],request.GET['statu'])
    return JsonResponse({'statu':1})
