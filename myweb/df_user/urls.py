from django.urls import path
from django.urls import re_path
from df_user import views


urlpatterns = [
    path('register',views.register),
    path('register_handle',views.register_handle),
    path('login',views.login),
    path('register_exist/',views.register_exist),
    path('login_handle',views.login_handle),
    path('info',views.info),
    path('order',views.order),
    path('site',views.site),
    path('logout',views.logout),
]
