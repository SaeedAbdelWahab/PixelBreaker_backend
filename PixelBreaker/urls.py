from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.Register.as_view()),
    url(r'^login$', views.Login.as_view()),
    url(r'^logout$', views.Logout.as_view()),
    url(r'^test$', views.test.as_view()),
    url(r'^api-imageUpload$', views.ImageDetailsView.as_view()),
    url(r'^CustomerView/(?P<number>[0-9]+)/$', views.CustomerView.as_view()),

]