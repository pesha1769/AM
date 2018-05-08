"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

    url(r'^core/login/$', core_views.login),
    url(r'^core/logout/$', core_views.logout),
    url(r'^core/register/$', core_views.register),
    url(r'^core/profile/$', core_views.profile),
"""

from django.conf.urls import url, include
from django.contrib import admin
from core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),


    url(r'^blog/', include('blog.urls',
                           namespace='blog',
                           app_name='blog')),

    url(r'^', include('account.urls')),
    url('social-auth/', include('social_django.urls', namespace='social')),

]

