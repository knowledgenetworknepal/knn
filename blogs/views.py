from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Blog, Comment
from .forms import CommentForm

class BlogList(ListView):
    model = Blog
    template_name = 'blogs/blog_list.html'
    queryset = Blog.objects.all().order_by('-id')
    paginate_by = 12


class BlogDetail(DetailView):
    model = Blog
    template_name = 'blogs/blog.html'
    queryset = Blog.objects.all()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['comment_form'] = CommentForm
        context_data['comments'] = Comment.objects.filter(blog=self.get_object()).order_by('-id')
        return context_data


class AddComment(CreateView):
    model = Blog
    queryset = Blog.objects.all()
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.comment_by = self.request.user
        form.instance.blog = get_object_or_404(Blog, slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'slug':self.kwargs.get('slug')})

