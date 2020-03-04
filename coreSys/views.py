from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Member, User
import datetime
import math
import json


def inputCarNum(request):
    state = request.POST.get('state')
    if state == "입차":  # 메인 페이지에서 입차를 클릭해서 넘어온 경우
        action = "../inProcess/"
        name = "inRequest"
        cls_name = "container inCar"
        cover_name = "inCar-corver"
    elif state == "출차":
        action = "../outProcess/"
        name = "outRequest"
        cls_name = "container outCar"
        cover_name = "outCar-corver"
    context = {
        'STATE': state,
        'ACTION': action,
        'NAME': name,
        'CLS_NAME': cls_name,
        'COVER_NAME': cover_name
    }
    return render(request, 'coreSys/inputCarNum.html', context)


def inProcess(request):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    request_car_number = request.POST['inRequest']
    members = Member.objects.all()
    try:
        members = members.filter(
            member_car_number=request_car_number, expiration__gte=nowDate).order_by('-expiration')
        name = members[0].name
        user_type = True
    except IndexError:                # 비어있는 쿼리셋에 접근하려고 할 때!
        # except Member.DoesNotExist: # 객체가 비어 있을 때!
        name = "고객"
        user_type = False
    user_car_number = request_car_number
    context = {
        'name': name,
        'user_car_number': user_car_number,
        'user_type': user_type,
    }
    user = User(user_car_number=user_car_number, user_type=user_type)
    user.save()
    return render(request, 'coreSys/inFinish.html', context)


def outProcess(request):
    request_car_number = request.POST['outRequest']
    # 현재 주차장에 입차된 차량(state=False)의 이용객 정보만 가져온다.
    user = User.objects.get(
        state=False, user_car_number=request_car_number)
    user_type = user.user_type
    if user_type == True:
        fee = 0  # 정기 회원인 경우에는 결제 없이 통과
        user.fee = fee
        user.save()
        return HttpResponseRedirect('./{}/finish'.format(request_car_number))
    else:
        return HttpResponseRedirect('./{}/payRequest'.format(request_car_number))


# 결제 요청
def payRequest(request, request_car_number):
    now = datetime.datetime.now()
    user = User.objects.get(
        state=False, user_car_number=request_car_number)
    in_time = user.in_time  # 입차 시간 가져오기
    time_gap = now - in_time  # 현재(출차 요청) 시간과 입차 시간의 차이를 구한다.
    # 주차장 이용 요금은 시간당 1,000원. 초단위 계산은 올림으로 진행.
    fee = math.ceil(time_gap.seconds/3600)*1000
    context = {
        'REQUEST_CAR_NUMBER': request_car_number,
        'IN_TIME': user.in_time,
        'NOW_TIME': now,
        'FEE': fee,
    }
    return render(request, 'coreSys/payment.html', context)


# 결제 확인
# POST를 통해서 자동차 번호를 받으면서, 동시에 URL 주소로도 받았다...
# 여기서는 contex 변수를 받는다. (from payment.html)
def payResponse(request, request_car_number):
    # request_car_number = request.POST.get('request_car_number')
    fee = request.POST.get('fee')     # 주차장 이용료 (문자)
    money = str(request.POST.get('money'))  # 고객이 지불한 금액 (숫자)
    if fee == money:
        user = User.objects.get(
            state=False, user_car_number=request_car_number)
        user.fee = fee
        user.save()
        return HttpResponseRedirect('../finish/')
    else:
        return HttpResponseRedirect('../payRequest/')
    # context = {
    #     'REQUEST_CAR_NUMBER': request_car_number,
    #     'FEE': fee,
    #     'MONEY': money
    # }


# 출차 완료
def finish(request, request_car_number):
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    out_time = now
    state = True
    user = User.objects.get(
        state=False, user_car_number=request_car_number)
    user.state = state
    user.out_time = out_time
    user.save()
    # 여기 아래로는 필요없는 과정..(이름을 찍어주기 위함)
    try:
        members = Member.objects.filter(
            member_car_number=request_car_number, expiration__gte=nowDate).order_by('-expiration')
        name = members[0].name
    except IndexError:  # 비어있는 쿼리셋에 접근하려고 할 때!
        name = "고객"
    context = {
        'NAME': name,
    }
    return render(request, 'coreSys/outFinish.html', context)
