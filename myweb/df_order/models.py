#coding=utf-8
from django.db import models

# Create your models here.
class OrderInfo(models.Model):
	oid=models.CharField(max_length=20,primary_key=True)
	ouser=models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
	odate=models.DateTimeField(auto_now=True)
	ototal=models.DecimalField(max_digits=6,decimal_places=2)
	opay=models.BooleanField(default=False)
	oaddress=models.CharField(max_length=150)

class DetailInfo(models.Model):
	order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
	good=models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
	price=models.DecimalField(max_digits=5,decimal_places=2)
	count=models.IntegerField()




