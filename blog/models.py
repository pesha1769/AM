# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)


    def __unicode__(self):
        return unicode(self.title) or u''



"""
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog', verbose_name=u'Автор')
    categories = models.ManyToManyField('categories.Category',blank=True, related_name='blog' )
    name = models.CharField(max_length=255)
    is_archive = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
        ordering = 'name', 'id'

    def __unicode__(self):
        return self.name
"""



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'Comment by {} on {}'.format(self.author, self.post)
