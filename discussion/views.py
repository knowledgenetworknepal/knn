from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DetailView, FormView
from .models import Quesiton, Comment, DiscussionVote
from .form import CommentForm, DicussionForm
from books.views import BaseMixin
from books.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin


class ListMyQuestionsView(BaseMixin, ListView):
    model = Quesiton
    template_name = 'discusison/all_question.html'

    def get_queryset(self):
        return Quesiton.objects.filter(user=self.request.user)


class AllQuestionsView(BaseMixin, ListView):
    model = Quesiton
    paginate_by = 10
    queryset = Quesiton.objects.select_related('user').filter(status=True)
    template_name = 'discusison/all_question.html'


class CategoryDiscussioView(BaseMixin, ListView):
    model = Quesiton
    paginate_by = 10
    template_name = 'discusison/all_question.html'

    def get_queryset(self, **kwargs):
        category = Category.objects.get(slug=self.kwargs.get('slug'))
        return Quesiton.objects.select_related('user').filter(category=category)


class DiscussionDetail(BaseMixin, DetailView):
    model = Quesiton
    template_name = 'discusison/detail.html'
    queryset = Quesiton.objects.all()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['comment_form'] = CommentForm
        context_data['comments'] = Comment.objects.select_related('comment_by').filter(question=self.get_object()).order_by('-id')
        return context_data


class AddDiscussion(LoginRequiredMixin, BaseMixin, CreateView):
    model = Quesiton
    template_name = 'discusison/add.html'
    form_class = DicussionForm
    queryset = Quesiton.objects.none()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_list')


class AddComment(LoginRequiredMixin, CreateView):
    model = Quesiton
    queryset = Quesiton.objects.all()
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.comment_by = self.request.user
        form.instance.question = get_object_or_404(Quesiton, slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_detail', kwargs={'slug':self.kwargs.get('slug')})
