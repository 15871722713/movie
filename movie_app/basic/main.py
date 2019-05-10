#coding:utf-8

import re
import json
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from movie_app.models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def count_pages(movies,request):
	paginator = Paginator(movies, 20)
	page = int(request.GET.get('page',1))
	try:
		# contacts = paginator.page(page)
		if paginator.num_pages > 7:
			if page - 3 < 1:
				page_range = range(1,8)
			elif page + 3 > paginator.num_pages:
				page_range = range(paginator.num_pages-6,paginator.num_pages+1)
			else:
				page_range = range(page-3,page+4)
		else:
			page_range = paginator.page_range
		contacts = paginator.page(page)				
	except PageNotAnInteger:
		contacts = paginator.page(1)
	except EmptyPage:
		contacts = paginator.page(paginator.num_pages)
	return contacts,page_range

def mainfunc(request):
	movie01 = Movie.objects.filter(Q(list_name="动作片") | Q(list_name="爱情片") | Q(list_name="喜剧片") | Q(list_name="科幻片") | Q(list_name="恐怖片") | Q(list_name="剧情片") | Q(list_name="战争片") | Q(list_name="韩剧") | Q(list_name="泰剧") | Q(list_name="日本剧") | Q(list_name="欧美剧") | Q(list_name="国产剧") | Q(list_name="香港剧") | Q(list_name="台湾剧") | Q(list_name="动漫") | Q(list_name="综艺")).order_by('-vod_data')[0:10]
	movie02 = Movie.objects.filter(Q(list_name="动作片") | Q(list_name="爱情片") | Q(list_name="喜剧片") | Q(list_name="科幻片") | Q(list_name="恐怖片") | Q(list_name="剧情片") | Q(list_name="战争片")).order_by('-vod_data')[0:10]
	movie03 = Movie.objects.filter(Q(list_name="韩剧") | Q(list_name="泰剧") | Q(list_name="日本剧") | Q(list_name="欧美剧") | Q(list_name="国产剧") | Q(list_name="香港剧") | Q(list_name="台湾剧")).order_by('-vod_data')[0:10]
	movie04 = Movie.objects.filter(list_name="动漫").order_by('-vod_data')[0:10]
	movie05 = Movie.objects.filter(list_name="综艺").order_by('-vod_data')[0:10]
	return render(request,'index.html',{"movie01":movie01,"movie02":movie02,"movie03":movie03,"movie04":movie04,"movie05":movie05})

def spiderfunc(request):
	return render(request,'spider.html')

def spidermain(request):
	idx = request.GET.get('id',default='1')

	url = 'http://www.dbzyz.com/inc/feifei3/?p=%s' % idx
	print "Start to craw url:%s" % url 
	html = requests.get(url).text
	datalist = json.loads(html)

	pagecount = datalist['page']['pagecount']
	pageindex = datalist['page']['pageindex']

	print "Page = %s , pagecount = %s." % (pageindex,pagecount)

	datas = datalist['data']

	for data in datas:
		res = Movie.objects.filter(vod_name=data['vod_name'])
		voddatas = re.search(r'(\d{4}-\d{2}-\d{2})',data['vod_pic'])
		if voddatas is not None:
			voddata = voddatas.group(0)
		else:
			voddata = ''
		if len(res) ==0:
			Movie.objects.create(
				vod_name = data['vod_name'],
				list_name =  data['list_name'],
				vod_actor = data['vod_actor'],
				vod_year = data['vod_year'],
				vod_data = voddata,
				vod_addtime = data['vod_addtime'],
				vod_continu =  data['vod_continu'],
				vod_pic = data['vod_pic'],
				vod_director = data['vod_director'],
				vod_language = data['vod_language'],
				vod_area =  data['vod_area'],
				vod_url = data['vod_url'],
				vod_content = data['vod_content'],
				)
		elif len(res[0].vod_url) != len(data['vod_url']):
			Movie.objects.filter(vod_name=data['vod_name']).update(vod_url = data['vod_url'])


	if int(idx) > int(pagecount):
		return HttpResponse(None)
	return render(request,'spider_table.html',{'data':datas,'pages':json.dumps(datalist['page'])})

def movie_detail(request,id):
	movie = Movie.objects.get(id=id)
	# 1080高清国语无水印$https://db.ucxzz.com:888/share/tFpC0zQtWjnvf2hn$$$1080高清国语无水印$https://db.ucxzz.com:888/2019/03/17/tFpC0zQtWjnvf2hn/playlist.m3u8
	movie_datas = {}
	data_dbyun = []
	data_dbm3u8 = []

	# print 'list_name',movie.list_name
	if movie.list_name.endswith('剧'):
		print 'dianshiju'
		print 'url',movie.vod_url
		if "$$$" in movie.vod_url:
			a = movie.vod_url.split("$$$")
			dbyun = a[0]
			dbm3u8 = a[1]

			if '\r\n' in dbyun:
				b = dbyun.split('\r\n')
				for x in b:
					b = x.split('$')
					data_dbyun.append({'title':b[0],'url':b[1]})
			else:
				b = dbyun.split("$")
				data_dbyun.append({'title':b[0],'url':b[1]})
			movie_datas['dbyun'] = data_dbyun

			if '\r\n' in dbm3u8:
				b = dbm3u8.split('\r\n')
				for x in b:
					b = x.split('$')
					data_dbm3u8.append({'title':b[0],'url':b[1]})
			else:
				b = dbm3u8.split("$")
				data_dbm3u8.append({'title':b[0],'url':b[1]})
			movie_datas['dbm3u8'] = data_dbm3u8
	else:
		print 'dianying'
		if "$$$" in movie.vod_url:
			a = movie.vod_url.split("$$$")
			dbyun = a[0]
			dbm3u8 = a[1]
			b = dbyun.split("$")
			data_dbyun.append({'title':b[0],'url':b[1]})
			b = dbm3u8.split("$")
			data_dbm3u8.append({'title':b[0],'url':b[1]})
			movie_datas['dbyun'] = data_dbyun
			movie_datas['dbm3u8'] = data_dbm3u8
	# print 'movie.data:',movie_datas
	movie.vod_url = movie_datas
	movie.vod_language = movie_datas['dbm3u8'][0]['url']
	return render(request,'movie_detail.html',{"movie":movie})

def dyselections(request,id):
	if str(id) == '0':
		movies = Movie.objects.filter(Q(list_name="动作片") | Q(list_name="爱情片") | Q(list_name="喜剧片") | Q(list_name="科幻片") | Q(list_name="恐怖片") | Q(list_name="剧情片") | Q(list_name="战争片") ).order_by('-vod_data')
	if str(id) == '1':
		movies = Movie.objects.filter(list_name="动作片").order_by('-vod_data')
	if str(id) == '2':
		movies = Movie.objects.filter(list_name="爱情片").order_by('-vod_data')
	if str(id) == '3':
		movies = Movie.objects.filter(list_name="喜剧片").order_by('-vod_data')
	if str(id) == '4':
		movies = Movie.objects.filter(list_name="科幻片").order_by('-vod_data')
	if str(id) == '5':
		movies = Movie.objects.filter(list_name="恐怖片").order_by('-vod_data')
	if str(id) == '6':
		movies = Movie.objects.filter(list_name="剧情片").order_by('-vod_data')
	if str(id) == '7':
		movies = Movie.objects.filter(list_name="战争片").order_by('-vod_data')
	if str(id) == '8':
		movies = Movie.objects.filter(list_name="伦理片").order_by('-vod_data')
	if str(id) == '9':
		movies = Movie.objects.filter(list_name="美女热舞写真").order_by('-vod_data')
	if str(id) == '10':
		movies = Movie.objects.filter(list_name="VIP视频秀").order_by('-vod_data')

	contacts,page_range = count_pages(movies, request)

	return render(request,'movie_type.html',{"movies":contacts,"page_range":page_range})

def dsselections(request,id):
	if str(id) == '0':
		movies = Movie.objects.filter(Q(list_name="韩剧") | Q(list_name="泰剧") | Q(list_name="日本剧") | Q(list_name="欧美剧") | Q(list_name="国产剧") | Q(list_name="香港剧") | Q(list_name="台湾剧") ).order_by('-vod_data')
	if str(id) == '1':
		movies = Movie.objects.filter(list_name="韩剧").order_by('-vod_data')
	if str(id) == '2':
		movies = Movie.objects.filter(list_name="泰剧").order_by('-vod_data')
	if str(id) == '3':
		movies = Movie.objects.filter(list_name="日本剧").order_by('-vod_data')
	if str(id) == '4':
		movies = Movie.objects.filter(list_name="欧美剧").order_by('-vod_data')
	if str(id) == '5':
		movies = Movie.objects.filter(list_name="国产剧").order_by('-vod_data')
	if str(id) == '6':
		movies = Movie.objects.filter(list_name="香港剧").order_by('-vod_data')
	if str(id) == '7':
		movies = Movie.objects.filter(list_name="台湾剧").order_by('-vod_data')

	contacts,page_range = count_pages(movies, request)

	return render(request,'movie_type.html',{"movies":contacts,"page_range":page_range})

def dmselections(request):
	movies = Movie.objects.filter(list_name="动漫").order_by('-vod_data')

	contacts,page_range = count_pages(movies, request)

	return render(request,'movie_type.html',{"movies":contacts,"page_range":page_range})

def zyselections(request):
	movies = Movie.objects.filter(list_name="综艺").order_by('-vod_data')

	contacts,page_range = count_pages(movies, request)

	return render(request,'movie_type.html',{"movies":contacts,"page_range":page_range})

def find(request):
	name = request.POST.get('find_name',None)
	data = Movie.objects.filter(vod_name__iexact=name)
	return render(request,'movie_type.html',{'movies':data})