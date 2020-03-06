from django.views.generic import TemplateView
from .forms import MemberForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from coreSys.models import Member


#--- TemplateView
# class HomeView(TemplateView):
#     """
#     HomeView는 특별한 처리 로직 없이 단순히 템플릿만 보여주는 로직.
#     """
#     template_name = 'home.html'

def HomeView(request):
    """
    정기 회원 등록 폼을 만들어서 메인 페이지와 렌더링.
    """
    form = MemberForm()
    return render(request, '../templates/home.html', {'form': form})


def signUpMember(request):
    """
    정기 회원 등록 처리.
    """
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    member_car_number = request.POST.get('member_car_number')
    expiration = request.POST.get('expiration')
    member = Member(name=name, phone=phone,
                    member_car_number=member_car_number, expiration=expiration)
    member.save()
    return HttpResponseRedirect('../')
