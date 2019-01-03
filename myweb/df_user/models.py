from django.db import models

# Create your models here.
class UserInfo(models.Model):
	uname=models.CharField(max_length=10)
	upwd=models.CharField(max_length=40)
	uemail=models.CharField(max_length=30)
	receiver=models.CharField(max_length=10,default='')
	address=models.CharField(max_length=80,default='')
	postalcode=models.CharField(max_length=6,default='')
	phone=models.CharField(max_length=11,default='')
