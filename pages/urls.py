from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'signin/$', views.signin, name='signin'),
    url(r'signup/$', views.signup, name='signup'),
)
