from django.urls import path
from django.urls import re_path
from df_goods import views


urlpatterns=[
path('',views.index),
re_path('^(\d+)/$',views.detail),
re_path('(\d)-(\d)-(\d+)',views.list),
path('',views.index)



]