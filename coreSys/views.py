from django.shortcuts import render, redirect
from django.http import HttpResponse
import xml.etree.ElementTree as ET


def inputCarNum(request):
    # if request.POST.get('state') == "입차":
    #     NOTICE = "입차 요청 하셨습니다."
    # else:
    #     NOTICE = "출차 요청 하셨습니다."
    context = {}
    context['STATE'] = request.POST.get('state')
    # context['NOTICE'] = NOTICE
    return render(request, 'coreSys/inputCarNum.html', context)


def inProcess(request):
    return render(request, 'coreSys/inProcess.html')


def outProcess(request):

    return render(request, 'coreSys/outProcess.html')
