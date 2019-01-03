from django.urls import path
from django.urls import re_path
from df_order import views

urlpatterns=[
path('',views.order),
path('handle',views.order_handle)
]
