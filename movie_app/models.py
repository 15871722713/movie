#coding:utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Movie(models.Model):
    vod_name = models.CharField(u'影片名称', blank=True, null=True, max_length=30)
    list_name = models.CharField(u'影片类型', blank=True, null=True, max_length=30) 
    vod_actor = models.CharField(u'影片演员', blank=True, null=True, max_length=50)
    vod_year = models.CharField(u'上映年份', blank=True, null=True, max_length=30)
    vod_data = models.CharField(u'上映日期', blank=True, null=True, max_length=30)
    vod_addtime = models.CharField(u'更新时间', blank=True, null=True, max_length=30)
    vod_continu = models.CharField(u'影片状态', blank=True, null=True, max_length=50) 
    vod_pic = models.CharField(u'影片图片', blank=True, null=True, max_length=256)
    vod_director = models.CharField(u'影片导演', blank=True, null=True, max_length=50)
    vod_language = models.CharField(u'影片语言', blank=True, null=True, max_length=50)
    vod_area = models.CharField(u'影片地区', blank=True, null=True, max_length=30) 
    vod_url = models.CharField(u'播放地址', blank=True, null=True, max_length=256)
    vod_content = models.CharField(u'剧情介绍', blank=True, null=True, max_length=256)
     
    def to_dict(self):
        return dict([(attr, str(getattr(self, attr))) for attr in [f.name for f in self._meta.fields]])

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = verbose_name = u'电影信息'