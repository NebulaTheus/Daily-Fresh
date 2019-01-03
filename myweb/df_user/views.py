#coding=utf-8
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from df_user import models
from df_goods import models as g_models
from df_order.models import OrderInfo,DetailInfo
from hashlib import sha1
from df_user import user_decorator


# Create your views here.

def register(request):

	return render (request,'df_user/register.html')

def register_handle(request):
	post=request.POST
	uname=post.get('user_name')
	upwd=post.get('pwd')
	upwd2=post.get('cpwd')
	uemail=post.get('email')
	print(uname,type(uname))
	if upwd != upwd2:
		return redirect('/user/register')
	user=models.UserInfo()
	user.uname=uname
	user.uemail=uemail
	s1=sha1()
	s1.update(upwd.encode('utf-8'))
	user.upwd=s1.hexdigest()
	user.save()
	return redirect('/user/login')
def login(request):
	uname=request.COOKIES.get('uname','')
	context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname,'upwd':''}

	return render(request,'df_user/login.html',context)

def register_exist(request):
	uname=request.GET.get('uname')
	count=models.UserInfo.objects.filter(uname=uname).count()
	return JsonResponse({'count':count})

def login_handle(request):
	post=request.POST
	uname=post.get('username')
	upwd=post.get('pwd')
	jizhu=post.get('jizhu',0)
	print(uname,upwd,jizhu)
	users=models.UserInfo.objects.filter(uname=uname)
	if len(users)==1:
		s1=sha1()
		s1.update(upwd.encode('utf-8'))
		upwd2=s1.hexdigest()
		if upwd2==users[0].upwd:
			u_url=request.COOKIES.get('url','/')
			print(u_url)
			red=HttpResponseRedirect(u_url)
			if jizhu==1:
				red.set_cookie('uname',uname)
			else:
				red.set_cookie('uname','',max_age=-1)
			request.session['user_id']=users[0].id
			request.session['user_name']=uname
			request.session.set_expiry(0)
			return red
		else:
			context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':''}
			print(222,context)
			return render(request,'df_user/login.html',context)
		
	else:
		context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':''}
		print(333,context)
		return render(request,'df_user/login.html',context)
@user_decorator.login
def info(request):
	user_email=models.UserInfo.objects.get(id=request.session['user_id']).uemail
	goods_ids=request.COOKIES.get('goods_ids')
	g_list=[]
	if goods_ids !=None:
		id_list=goods_ids.split(',')
		for id in id_list:
			good=g_models.GoodsInfo.objects.get(id=id)
			g_list.append(good)

	context={'title':'用户中心',
	         'user_email':user_email,
	         'user_name':request.session['user_name'],
	         'g_list':g_list

	}
	return render(request,'df_user/user_center_info.html',context)
	
@user_decorator.login
def order(request):
	user_id=request.session['user_id']
	orderlist_payed=OrderInfo.objects.filter(ouser_id=user_id,opay=True)
	orderlist_unpay=OrderInfo.objects.filter(ouser_id=user_id,opay=False)
	

	context={'title':'订单中心','paylist':orderlist_payed,'unpaylist':orderlist_unpay }
	return render(request,'df_user/user_center_order.html',context)






@user_decorator.login
def site(request):
	user=models.UserInfo.objects.get(id=request.session['user_id'])
	if request.method=='POST':
		post=request.POST
		user.receiver=post.get('receiver')
		user.address=post.get('address')
		user.postalcode=post.get('postalcode')
		user.phone=post.get('phone')
		user.save()
	context={'title':'用户中心','user':user}
	return render(request,'df_user/user_center_site.html',context)

def logout(request):
	request.session.flush()
	return redirect('/')
	








	



