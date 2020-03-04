from django.urls import path
from . import views

app_name = 'coreSys'

urlpatterns = [
    # path('inProcess/', views.inProcess),
    # path('outProcess/', views.outProcess),
    path('inputCarNum/', views.inputCarNum, name="inputCarNum"),
    path('inProcess/', views.inProcess, name="inProcess"),
    path('outProcess/', views.outProcess, name="outProcess"),
    path('outProcess/<str:request_car_number>/payRequest/',
         views.payRequest, name="payRequest"),
    path('outProcess/<str:request_car_number>/payResponse/',
         views.payResponse, name="payResponse"),
    path('outProcess/<str:request_car_number>/finish/',
         views.finish, name="finish"),
]
