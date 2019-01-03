#coding=utf-8
from django.http import HttpResponseRedirect

def login(func):
	def wrapper(request,*args,**wargs):
		if request.session.has_key('user_id'):
			print(request.session.items())
			return func(request,*args,**wargs)
		else:
			print('用户未登录')
			print(request.get_full_path())
			red=HttpResponseRedirect('/user/login')
			red.set_cookie('url',request.get_full_path())
			return red
	return wrapper



