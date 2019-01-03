#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db import transaction
from df_order import models
from df_cart import models as cart_models
from df_user import models as user_models
from df_user import user_decorator
import time
import decimal

# Create your views here.


@user_decorator.login
def order(request):
	user_id=request.session['user_id']
	user=user_models.UserInfo.objects.get(id=user_id)
	name=user.uname
	address=user.address
	phone=user.phone
	reciver_info=address+'  ('+name+' 收)  '+phone
	

	carts=request.GET.get('cart_id')
	cart_list=carts.split('_')
	c_list=[]
	for cart_id in cart_list:
		cart=cart_models.CartInfo.objects.get(id=cart_id)
		c_list.append(cart)
	context={
	'title':'天天生鲜-提交订单',
	're_info':reciver_info,
	'g_list':c_list

	}
	return render(request,'df_order/place_order.html',context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
	tran_p=transaction.savepoint()
	print(request.POST)
	if request.method=='POST':
		ids=request.POST.getlist('ids[]')
		freight=request.POST.get('freight')
		total=request.POST.get('total')
	user_id=request.session['user_id']
	try:
		error_msg=''
		user=user_models.UserInfo.objects.get(id=user_id)
		uname=user.uname
		uaddress=user.address
		uphone=user.phone
		re_info=uaddress+'  ('+uname+' 收)  '+uphone
		print(re_info)
		order=models.OrderInfo()
		order.oid=time.strftime('%Y%m%d%H%M%S',time.localtime())+str(user_id)
		order.ouser_id=user_id
		order.ototal=decimal.Decimal(total)
		order.opay=False
		order.oaddress=re_info
		order.save()
		for id in ids:
			cart=cart_models.CartInfo.objects.get(id=int(id))
			if cart.count<=cart.good.gstock:
				print(cart.good.gtitle,'原库存',cart.good.gstock)
				cart.good.gstock-=cart.count
				cart.good.save()
				print(cart.good.gtitle,'现库存',cart.good.gstock)
				d_order=models.DetailInfo()
				d_order.order=order
				d_order.good=cart.good
				d_order.price=cart.good.gprice
				d_order.count=cart.count
				d_order.save()
				cart.delete()
				# transaction.savepoint_commit(tran_p)
				result=True
			else:
				error_msg=cart.good.gtitle+'  库存不足'
				result=False
				transaction.savepoint_rollback(tran_p)
		transaction.savepoint_commit(tran_p)
	except Exception as e:
		print(111,e)
		error_msg=e
		result=False
		transaction.savepoint_rollback(tran_p)
	context={'result':result,'msg':error_msg}
	print(context)	

	return JsonResponse(context)
