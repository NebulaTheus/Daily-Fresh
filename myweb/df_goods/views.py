#coding=utf-8

from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from  df_goods import models

# Create your views here.



def index(request):
	typelist=models.TypeInfo.objects.all()
	type0=typelist[0].goodsinfo_set.order_by('-id')[0:4]
	type01=typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
	type1=typelist[1].goodsinfo_set.order_by('-id')[0:4]
	type11=typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
	type2=typelist[2].goodsinfo_set.order_by('-id')[0:4]
	type21=typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
	type3=typelist[3].goodsinfo_set.order_by('-id')[0:4]
	type31=typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
	type4=typelist[4].goodsinfo_set.order_by('-id')[0:4]
	type41=typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
	type5=typelist[5].goodsinfo_set.order_by('-id')[0:4]
	type51=typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
	
	context={'title':'天天生鲜-首页',
	'type0':type0,'type01':type01,
	'type1':type1,'type11':type11,
	'type2':type2,'type21':type21,
	'type3':type3,'type31':type31,
	'type4':type4,'type41':type41,
	'type5':type5,'type51':type51,

	}
	return render(request,'df_goods/index.html',context)

def detail(request,id):
	good=models.GoodsInfo.objects.get(pk=int(id))
	good.gclick+=1
	good.save()
	adv_list=good.gtype.goodsinfo_set.order_by('-id')[0:2]
	context={'title':'天天生鲜-商品详情','good':good,'adv_list':adv_list}
	response=render(request,'df_goods/detail.html',context)

	goods_ids=request.COOKIES.get('goods_ids','')
	g_id=str(id)
	g_list=[]
	if goods_ids !='':
		g_list=goods_ids.split(',')
		if g_list.count(g_id)>=1:
			g_list.remove(g_id)
			g_list.insert(0,g_id)
		else:
			g_list.insert(0,g_id)

		if len(g_list)>=6:
			del g_list[5]

	else:
		g_list.append(g_id)

	goods_ids=','.join(g_list)
	response.set_cookie('goods_ids',goods_ids)
	return response


def list(request,tid,sort,pid):
	typeinfo=models.TypeInfo.objects.get(pk=int(tid))
	adv_list=typeinfo.goodsinfo_set.order_by('-id')[0:2]
	if int(sort)==1:
		goods=typeinfo.goodsinfo_set.order_by('-id')
		paginator=Paginator(goods,15)
		g_list=paginator.get_page(int(pid))
		pages=paginator.page_range
		num=paginator.num_pages
	if int(sort)==2:
		goods=typeinfo.goodsinfo_set.order_by('gprice')
		paginator=Paginator(goods,15)
		g_list=paginator.get_page(int(pid))
		pages=paginator.page_range
		num=paginator.num_pages
	if int(sort)==3:
		goods=typeinfo.goodsinfo_set.order_by('-gclick')
		paginator=Paginator(goods,15)
		g_list=paginator.get_page(int(pid))
		pages=paginator.page_range
		num=paginator.num_pages
	context={'title':'天天生鲜-商品列表',
	'adv_list':adv_list,
	'g_list':g_list,
	'tid':tid,
	'sort':sort,
	'pages':pages,
	'pid':pid,
	'num':num

	}

	return render(request,'df_goods/list.html',context)





