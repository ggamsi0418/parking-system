from django.urls import path
from . import views

urlpatterns = [
    # path('inProcess/', views.inProcess),
    # path('outProcess/', views.outProcess),
    path('inputCarNum/', views.inputCarNum, name="inputCarNum"),
    path('inProcess/', views.inProcess, name="inProcess"),
    path('outProcess/', views.outProcess, name="outProcess"),
]
