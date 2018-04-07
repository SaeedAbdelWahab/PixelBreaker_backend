from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register$', views.Register.as_view()),
    url(r'^login$', views.Login.as_view()),
    url(r'^logout$', views.Logout.as_view()),
    url(r'^test$', views.test.as_view())
]