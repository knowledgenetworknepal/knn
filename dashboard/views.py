from typing import List
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .permissions import IsAdminMixin

from django.contrib.auth import get_user_model
from books.models import Book
from userapp.models import Request, Deposit

User = get_user_model()

class BaseMixin(IsAdminMixin):
    ...


class UserMixin(BaseMixin, ListView):
    model = User
    template_name = 'dashboard/userlist.html'
    paginate_by = 30


class UserListView(UserMixin):
    queryset = User.objects.all()


class ApprovedUserList(UserMixin):
    queryset = User.objects.filter(approved=True)


class UnapprovedUserList(UserMixin):
    queryset = User.objects.filter(approved=False)


class ApproveUser(BaseMixin):
    pass


class RejectUser(BaseMixin):
    pass


class AddEvents(BaseMixin):
    pass


class BookMixin(BaseMixin, ListView):
    model = Book
    template_name = 'dashboard/booklist.html'
    paginate_by = 30


class BookList(BookMixin):
    queryset = Book.objects.all().order_by('-id')


class AvailabelBookList(BookMixin):
    queryset = Book.objects.all().order_by('-id')


class AddBook(BaseMixin, CreateView):
    pass


class BookDetail(BaseMixin, DetailView):
    pass


class RequestList(BaseMixin):
    model = Request
    template_name = 'dashboard/request_list.html'
    paginate_by = 30
    queryset = Request.objects.filter(status=False).order_by('-id')


class Notification(BaseMixin):
    pass


class UserNotificationList(BaseMixin):
    pass


class CreateNotification(BaseMixin):
    pass


class AddCategory(BaseMixin, CreateView):
    pass


class CategoryList(BaseMixin, ListView):
    pass


class CategoryDetail(BaseMixin, DetailView):
    pass


class DepositList(BaseMixin, ListView):
    model = Deposit
    template_name = 'dashboard/deposit_list.html'
    paginate_by = 30
    queryset = Deposit.objects.all().order_by('-id')


class DepositDetail(BaseMixin, DetailView):
    pass

