from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from coreSys.models import Member
from .forms import MemberForm
from datetime import date
import json
import re


def homeView(request):
    """
    정기 회원 등록 폼을 만들어서 메인 페이지와 렌더링.
    """
    form = MemberForm()
    return render(request, '../templates/home.html', {'form': form})


def signUpMember(request):
    """
    입력 정보 유효성 검사 및 정기 회원 등록 처리.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        member_car_number = request.POST.get('member_car_number')
        expiration = request.POST.get('expiration')
        regex_name = re.compile('^[가-힣a-zA-Z]+$')
        regex_phone = re.compile('^01[016789]-\d{3,4}-\d{4}$')
        regex_car_num = re.compile('\d{2,3}[가-힣]{1}\d{4}$')
        name_vaild = False if regex_name.match(name) is None else True
        phone_vaild = False if regex_phone.match(phone) is None else True
        car_num_vaild = False if regex_car_num.match(
            member_car_number) is None else True
        msg = {}
        if (not name_vaild) or (not phone_vaild) or (not car_num_vaild):
            msg["error_msg"] = "입력된 정보가 유효하지 않습니다!"
        else:    # 유효성 검사를 통과한 경우
            try:  # 오늘자를 기준으로 만료일이 남아있는 자동차 번호를 Meber 테이블에서 리스트로 가져온다.
                members = Member.objects.filter(expiration__gt=date.today())
                car_list = [member.member_car_number for member in members]
                if member_car_number in car_list:
                    msg["error_msg"] = "이미 등록되어 있는 차량입니다."
                    return HttpResponse(json.dumps(msg), content_type="application/json")
            except:  # 현재 멤버 중 만료일이 남아 있는 사람이 없으므로 무조건 정기 회원 등록 가능
                pass
            msg["error_msg"] = None
            member = Member(name=name, phone=phone,
                            member_car_number=member_car_number, expiration=expiration)
            member.save()
        return HttpResponse(json.dumps(msg), content_type="application/json")
    else:  # 올바르지 않은 URL 접근을 차단
        return render(request, 'coreSys/errorPage.html', status=405)
