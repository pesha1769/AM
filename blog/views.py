# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, reverse
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
from django import forms
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostCreate(CreateView):
    model = Post
    fields = 'title', 'body', 'status', 'tags'
    template_name = 'blog/post/create.html'
    context_object_name = 'post'
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreate, self).form_valid(form)

class PostEdit(UpdateView):
    model = Post
    fields = 'title', 'body', 'status', 'tags'
    template_name = 'blog/post/edit.html'
    context_object_name = 'post'
    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})
    def get_queryset(self):
        queryset = super(PostEdit, self).get_queryset()
        return queryset.filter(author=self.request.user)

class PostDelete(DeleteView):
    model = Post
    fields = 'title',
    template_name = 'blog/post/delete.html'
    context_object_name = 'post'
    def get_success_url(self):
        return reverse('blog:post_list')



def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts,
                                                   'tag': tag})


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body', )



def post_detail(request, pk=None):
    post = get_object_or_404(Post, id=pk, status='published')
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted


        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


def post_share(request, pk=None):
    # Retrieve post by id
    post = get_object_or_404(Post, id=pk, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = reverse('blog:post_detail', kwargs={'pk': post.pk})
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@admin.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
