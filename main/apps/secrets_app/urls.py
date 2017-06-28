from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^success/(?P<id>\d+)$', views.success),
    url(r'^login$', views.login),
    url(r'^post$', views.post),
    url(r'^delete/(?P<secret_id>\d+)$', views.delete),
    url(r'^like/(?P<secret_id>\d+)$', views.like),
    url(r'^popular$', views.popular),
    url(r'^back$', views.back),
    url(r'^deletepop/(?P<secret_id>\d+)$', views.deletepop),
    url(r'^likepop/(?P<secret_id>\d+)$', views.likepop),
    url(r'^logout$', views.logout)
    
]



#ISSUES TO FIX:
# - can't like something multiple times
# can't like own secrets


