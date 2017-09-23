from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

app_name = 'smedia'

urlpatterns = [
    url(r'^register$', views.UserFormView.as_view(), name='register'),
    url(r'^index$', views.IndexView.as_view(), name='index'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
    # url(r'^tw', TemplateView.as_view(template_name='smedia/twitty.html')),

]
