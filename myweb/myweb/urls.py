"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include
from django.urls import path
from df_user import views
from df_user import urls as user_urls
from df_goods import urls as goods_urls
from df_cart import urls as cart_urls
from df_order import urls as order_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user_urls)),
    path('tinymce',include('tinymce.urls')),
    path('index/',include(goods_urls)),
    path('list/',include(goods_urls)),
    path('',include(goods_urls)),
    path('cart/',include(cart_urls)),
    path('order/',include(order_urls)),
    path('search/',include('haystack.urls'))
    ]
