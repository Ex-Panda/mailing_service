from django.shortcuts import render, redirect
from django.views import View
from pytils.translit import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class ProtectedView(View):
    #переопределение get, чтобы анонимный пользователь не мог взаимодействовать
    def get(self, *args, **kwargs):
        if self.request.user.id is None:
            return redirect('user_auth:login')
        else:
            return super().get(*args, **kwargs)


class BlogCreateView(ProtectedView, CreateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'is_publication')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(ProtectedView, UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'is_publication')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object


class BlogDeleteView(ProtectedView, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

