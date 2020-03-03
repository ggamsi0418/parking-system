from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Member, User
import datetime

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')


def inputCarNum(request):
    state = request.POST.get('state')
    if state == "입차":  # 메인 페이지에서 입차를 클릭해서 넘어온 경우
        action = "../inProcess/"
        name = "inRequest"
        cls_name = "container inCar"
    elif state == "출차":
        action = "../outProcess/"
        name = "outRequest"
        cls_name = "container outCar"
    context = {
        'STATE': state,
        'ACTION': action,
        'NAME': name,
        'CLS_NAME': cls_name
    }
    return render(request, 'coreSys/inputCarNum.html', context)


def inProcess(request):
    request_car_number = request.POST['inRequest']
    members = Member.objects.all()
    try:
        members = members.filter(
            member_car_number=request_car_number, expiration__gte=nowDate).order_by('-expiration')
        name = members[0].name
        user_type = True
    except IndexError:                # 쿼리셋이 없을 때!
        # except Member.DoesNotExist: # 객체가 없을 때!
        name = "고객"
        user_type = False
    user_car_number = request_car_number
    contetx = {
        'name': name,
        'user_car_number': user_car_number,
        'user_type': user_type,
    }
    users = User(user_car_number=user_car_number, user_type=user_type)
    users.save()
    return render(request, 'coreSys/inProcess.html', contetx)


def outProcess(request):
    return render(request, 'coreSys/outProcess.html')
