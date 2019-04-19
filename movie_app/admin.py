import xadmin
from .models import Movie
from django.contrib import admin

# Register your models here.
class MovieAdmin(object):
    list_display = ('id','vod_name','list_name','vod_actor','vod_year','vod_data','vod_addtime','vod_continu','vod_pic','vod_director','vod_language','vod_area','vod_content')
    search_fields = ('id','vod_name','list_name','vod_actor','vod_year','vod_data','vod_addtime','vod_continu','vod_pic','vod_director','vod_language','vod_area','vod_content')

xadmin.site.register(Movie, MovieAdmin)