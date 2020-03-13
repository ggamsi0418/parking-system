from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Member, User
import datetime
import math
import json
import re


def inputCarNum(request):
    '''
    메인 페이지에서 입차 또는 출차를 선택하면,
    요청에 맞는 차량 번호 입력 페이지를 렌더링 한다.
    '''
    if request.method == 'POST':
        state = request.POST.get('state')
        if state == "입차":  # 메인 페이지에서 입차를 클릭해서 넘어온 경우
            action = "/coreSys/inProcess/"
            name = "inRequest"
            cls_name = "container inCar"
            cover_name = "inCar-corver"
        elif state == "출차":  # 메인 페이지에서 출차를 클릭해서 넘어온 경우
            action = "/coreSys/outProcess/"
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
    else:  # 올바르지 않은 URL 접근을 차단
        return render(request, 'coreSys/errorPage.html', status=405)


def inProcess(request):
    '''
    차량 번호 입력 페이지에서 넘어온 입력값(차량 번호)이 유효한지 검증하고,
    유효하다면 바로 입차 완료 페이지로 넘긴다.
    '''
    if request.method == 'POST':
        msg = {}
        inputCarNum = request.POST.get('inputCarNum')
        regex_car_num = re.compile('\d{2,3}[가-힣]{1}\d{4}$')
        car_num_vaild = False if regex_car_num.match(
            inputCarNum) is None else True
        # 입력 받은 차량 번호 유효성 검증
        if (not car_num_vaild):
            msg['error_msg'] = "자동차 번호가 유효하지 않습니다."
            return HttpResponse(json.dumps(msg), content_type="application/json")
        # 중복 입차 검증
        if User.objects.filter(user_car_number=inputCarNum, state=False).exists():
            msg['error_msg'] = "이미 입차된 자동차 번호입니다."
            return HttpResponse(json.dumps(msg), content_type="application/json")
        else:  # 정상적인 입차 처리
            request_car_number = request.POST.get(
                'inputCarNum')  # 입차 요청한 자동차 번호
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            try:
                members = Member.objects.filter(
                    member_car_number=request_car_number, expiration__gte=nowDate).order_by('-expiration')
                name = members[0].name
                user_type = True
            except IndexError:
                name = "고객"
                user_type = False
            user_car_number = request_car_number
            context = {
                'NAME': name,
            }
            user = User(user_car_number=user_car_number, user_type=user_type)
            user.save()
            html = render_to_string('coreSys/inFinish.html', context)
            msg['error_msg'] = None
            msg['step'] = 'inFinish'
            msg['html'] = html
            return HttpResponse(json.dumps(msg), content_type="applcation/json")
    else:  # 올바르지 않은 URL 접근을 차단
        return render(request, 'coreSys/errorPage.html', status=405)


def outProcess(request):
    '''
    차량 번호 입력 페이지에서 넘어온 입력값(차량 번호)이 유효한지 검증한다.
    정기 회원일 경우 바로 '결제 없이 통과', 일일 방문객일 경우 '결제 요청'.
    '''
    if request.method == 'POST':
        msg = {}
        inputCarNum = request.POST.get('inputCarNum')
        regex_car_num = re.compile('\d{2,3}[가-힣]{1}\d{4}$')
        car_num_vaild = False if regex_car_num.match(
            inputCarNum) is None else True
        # 입력 받은 차량 번호 유효성 검증
        if (not car_num_vaild):
            msg['error_msg'] = "자동차 번호가 유효하지 않습니다."
            return HttpResponse(json.dumps(msg), content_type="application/json")
        # 중복 출차 검증
        if not (User.objects.filter(user_car_number=inputCarNum, state=False).exists()):
            msg['error_msg'] = "입차하지 않았거나, 이미 출차된 자동차 번호입니다."
            return HttpResponse(json.dumps(msg), content_type="application/json")
        # 여기서부터는 정상적인 출차 진행
        request_car_number = request.POST.get('inputCarNum')
        user = User.objects.get(
            state=False, user_car_number=request_car_number)  # 현재 주차장에 입차된 차량(state=False)의 이용객 정보만 가져온다.
        user_type = user.user_type
        if user_type == True:  # 정기 회원인 경우에는 결제 없이 통과
            fee = 0
            user.fee = fee
            user.save()
            msg['error_msg'] = None
            msg['step'] = 'outFinish'
            msg['redirect_url'] = '/coreSys/outProcess/{}/finish'.format(
                request_car_number)
            return HttpResponse(json.dumps(msg), content_type="applcation/json")
        else:  # 일일 방문객일 경우에는 결제 요청
            msg['error_msg'] = None
            msg['step'] = 'payRequest'
            msg['redirect_url'] = '/coreSys/outProcess/{}/payRequest'.format(
                request_car_number)
            return HttpResponse(json.dumps(msg), content_type="applcation/json")
    else:  # 올바르지 않은 URL 접근을 차단
        return render(request, 'coreSys/errorPage.html', status=405)


def payRequest(request, request_car_number):
    '''
    출차를 요청한 일일 방문객의 주차장 이용료를 정산한다.
    주차장 총 이용 시간 및 이용료 정보를 담아
    결제 요청(결제 금액 입력) 페이지를 렌더링 한다.
    '''
    try:
        user = User.objects.get(
            state=False, user_car_number=request_car_number)
    except:
        return render(request, 'coreSys/errorPage.html', status=405)
    now = datetime.datetime.now()
    in_time = user.in_time  # 입차 시간 가져오기
    time_gap = now - in_time  # 현재(출차 요청) 시간과 입차 시간의 차이를 구한다.
    # 주차장 이용 요금은 시간당 1,000원. 초단위 계산은 올림으로 진행.
    fee = math.ceil(time_gap.seconds/3600)*1000
    time_gap_hour = round(time_gap.seconds/3600, 1)  # 시간을 소수 첫째자리까지 표현
    context = {
        'REQUEST_CAR_NUMBER': request_car_number,
        'TIME_GAP_HOUR': time_gap_hour,
        'FEE': fee,
    }
    return render(request, 'coreSys/payment.html', context)


# 결제 확인
# POST를 통해서 자동차 번호를 받으면서, 동시에 URL 주소로도 받았다...
# 여기서는 contex 변수를 받는다. (from payment.html)
def payResponse(request, request_car_number):
    '''
    결제 요청 페이지에서 입력 받은 결제 금액과 정산된 주차장 이용료를 비교한다.
    결제 금액이 정상적이라면 출차 완료 진행,
    비정상적이라면 결제 재요청
    '''
    if request.method == 'POST':
        # request_car_number = request.POST.get('request_car_number')
        fee = request.POST.get('fee')     # 주차장 이용료 (문자)
        money = str(request.POST.get('money'))  # 고객이 지불한 금액 (숫자)
        if fee == money:  # 정상적인 결제
            user = User.objects.get(
                state=False, user_car_number=request_car_number)
            user.fee = fee
            user.save()
            return HttpResponseRedirect('../finish/')
        else:  # 비정상적인 결제
            messages.info(request, '결제를 다시 시도해주시기 바랍니다!')
            return HttpResponseRedirect('../payRequest/')
    else:  # 올바르지 않은 URL 접근을 차단
        return render(request, 'coreSys/errorPage.html', status=405)


def finish(request, request_car_number):
    '''
    정기 회원의 출차 요청시 출차 완료.
    또는 일일 방문객의 주차장 이용료 결제가 정상일 때 출차 완료.
    고객 또는 정기 회원의 이름을 담아 출차 완료 페이지를 렌더링 한다.
    '''
    try:  # 올바르지 않은 URL 접근을 차단
        prev_url = request.META['HTTP_REFERER']
    except:
        return render(request, 'coreSys/errorPage.html', status=405)
    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    out_time = now
    state = True
    user = User.objects.get(
        state=False, user_car_number=request_car_number)
    user.state = state
    user.out_time = out_time
    user.save()
    # 아래부터는 중요하지 않은 과정 (출차 완료시 고객의 이름을 나타내기 위함)
    try:
        members = Member.objects.filter(
            member_car_number=request_car_number, expiration__gte=nowDate).order_by('-expiration')
        name = members[0].name
    except IndexError:  # 비어있는 쿼리셋에 접근하려고 할 때! (정기 회원이 아니라는 의미)
        name = "고객"
    context = {
        'NAME': name,
    }
    return render(request, 'coreSys/outFinish.html', context)
