from django.conf.urls import url
from . import views

urlpatterns = [
    # post views
    #url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^$', views.post_list, name='post_list'),

    url(r'^create/$', views.PostCreate.as_view(), name='create'),

    url(r'^(?P<pk>\d+)/edit/$', views.PostEdit.as_view(),
        name='edit'),

    url(r'^(?P<pk>\d+)/delete/$', views.PostDelete.as_view(),
        name='delete'),

    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),

    url(r'^(?P<pk>\d+)/$',
        views.post_detail,
        name='post_detail'),

    url(r'^(?P<pk>\d+)/share/$', views.post_share, name='post_share'),
]