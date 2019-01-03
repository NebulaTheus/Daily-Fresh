from django.urls import path
from django.urls import re_path
from df_cart import views

urlpatterns=[
path('',views.cart),
re_path('^add-(\d+)-(\d+)$',views.add),
re_path('^edit-(\d+)-(\d+)$',views.edit),
re_path('^delete-(\d+)$',views.delete)



]