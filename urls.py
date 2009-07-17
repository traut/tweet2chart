from django.conf.urls.defaults import *

from tweet2chart import views

urlpatterns = patterns('',
    (r'data', views.data),
    (r'', views.index),

)

