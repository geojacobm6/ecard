from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^scheme/$', views.SchemeView.as_view()),
]