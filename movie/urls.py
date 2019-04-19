"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from movie_app.basic import main

import xadmin

urlpatterns = [
    url(r'^admin/', include(xadmin.site.urls)),
    url(r'^$', main.mainfunc),
    url(r'^spider', main.spiderfunc),
    url(r'^mainspider', main.spidermain),

    url(r'^movie/(?P<id>[0-9A-Z]+)$',main.movie_detail),
    url(r'^dy/(?P<id>[0-9A-Z]+)$',main.dyselections),
    url(r'^ds/(?P<id>[0-9A-Z]+)$',main.dsselections),
    url(r'^dm',main.dmselections),
    url(r'^zy',main.zyselections),
    url(r'^ss',main.find),
    # url(r'^admin/', include(xadmin.site.urls)),
    # url(r'^admin/', include(xadmin.site.urls)),
    # url(r'^admin/', include(xadmin.site.urls)),
    # url(r'^admin/', include(xadmin.site.urls)),
]
