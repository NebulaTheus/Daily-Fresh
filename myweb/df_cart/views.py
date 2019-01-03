#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse
from df_user import user_decorator
from df_cart import models

# Create your views here.



@user_decorator.login
def cart(request):
	uid=request.session.get('user_id')
	g_list=models.CartInfo.objects.filter(user_id=uid)
	num=len(g_list)
	context={
	'title':'天天生鲜-购物车',
	'g_list':g_list,
	'num':num
	}
	if request.is_ajax():
		return JsonResponse({'count':num})
	return render(request,'df_cart/cart.html',context)

@user_decorator.login
def add(request,g_id,num):
	gid=int(g_id)
	user_id=request.session.get('user_id')
	carts=models.CartInfo.objects.filter(good_id=gid,user_id=user_id)
	if len(carts)>0:
		cart=carts[0]
		cart.count=cart.count+int(num)
	else:
		cart=models.CartInfo()
		cart.user_id=user_id
		cart.good_id=gid
		cart.count=int(num)
	cart.save()
	if request.is_ajax():
		carts=models.CartInfo.objects.filter(user_id=user_id)
		count=len(carts)
		return JsonResponse({'count':count})
	else:
		return redirect('/cart')


@user_decorator.login
def edit(request,cart_id,num):
	try:
		cart=models.CartInfo.objects.get(id=int(cart_id))
		cart.count=int(num)
		cart.save()
		return JsonResponse({'result':True})
	except:
		return JsonResponse({'result':False})

@user_decorator.login
def delete(request,cart_id):
	print(cart_id)
	try:
		models.CartInfo.objects.get(id=int(cart_id)).delete()
		print(8888888)
		return JsonResponse({'result':True})
	except:
		print(999)
		return JsonResponse({'result':False})
