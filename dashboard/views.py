from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect

from .permissions import IsAdminMixin

from django.contrib.auth import get_user_model
from books.models import Book, Category, BookUpload
from userapp.models import Request, Deposit
from books.forms import BookForm

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


class UserDetail(BaseMixin, DetailView):
    model = User
    template_name = 'dashboard/user_detail.html'
    queryset = User.objects.all()


class ApproveUser(BaseMixin):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user.approved = True
        user.save()
        return redirect(request.META.get("HTTP_REFERER"))


class RejectUser(BaseMixin):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user.approved = False
        user.save()
        return redirect(request.META.get("HTTP_REFERER"))


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
    model = Book
    template_name = 'dashboard/create_category.html'
    queryset = Book.objects.none()
    form_class = BookForm

    def post(self, request, *args, **kwargs):
        form = BookForm(request.POST, request.FILES)        
        if form.is_valid():
            isbn = form.cleaned_data.get('isbn_number')
            print(isbn)
            if Book.objects.filter(isbn=isbn).exists():
                book = get_object_or_404(Book, isbn=isbn)
            else:
                book = form.save(commit=False)
                book.isbn = isbn
                book.save()
            BookUpload.objects.create(book=book, added_by=request.user, status='approved')
            book.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))



class BookDetail(BaseMixin, DetailView):
    model = Book
    template_name = 'dashboard/book_details.html'
    queryset = Book.objects.all()


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
    model = Category
    template_name = 'dashboard/create_category.html'
    queryset = Category.objects.none()
    form_class = ''


class CategoryList(BaseMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    paginate_by = 30
    queryset = Category.objects.all().order_by('-id')


class CategoryDetail(BaseMixin, DetailView):
    model = Category
    template_name = 'dashboard/category_details.html'
    queryset = Category.objects.all()


class CategoryUpdate(BaseMixin, UpdateView):
    model = Category
    template_name = 'dashboard/categroy_update.html'
    queryset = Category.objects.all()


class DepositList(BaseMixin, ListView):
    model = Deposit
    template_name = 'dashboard/deposit_list.html'
    paginate_by = 30
    queryset = Deposit.objects.all().order_by('-id')


class DepositDetail(BaseMixin, DetailView):
    model = Deposit
    template_name = 'dashboard/deposit_detail.html'
    queryset = Deposit.objects.all()

