from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('add',views.add),
    path('login',views.login),
    path('success',views.success),
    path('logout',views.logout),
]

