from django.shortcuts import render, redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET


def inputCarNum(request):
    if request.POST.get('inClick') == "입차":
        NOTICE = "입차 요청 하셨습니다."
    else:
        NOTICE = "출차 요청 하셨습니다."
    context = {}
    context['NOTICE'] = NOTICE
    return render(request, 'coreSys/inputCarNum.html', context)
