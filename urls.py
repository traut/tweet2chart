from django.conf.urls.defaults import *

from tweet2chart import views

urlpatterns = patterns('',
    (r'data', views.data),
    (r'/(?P<user>.*)/?(?P<mark>.*)/?(?P<howmuch>.*)', views.search),    
    (r'', views.index),

)
