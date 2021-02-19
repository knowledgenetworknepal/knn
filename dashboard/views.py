from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView
 
from .permissions import IsAdminMixin

from django.contrib.auth import get_user_model
from django.db.models import Q
from books.models import Book, Category, BookUpload, Order
from userapp.models import Request, Deposit
from books.forms import BookForm, CategoryForm, AdminBookForm

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

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.get_object()
        context_data['books'] = BookUpload.objects.select_related('book').filter(added_by=user)
        context_data['deposits'] = Deposit.objects.filter(user=user)
        return context_data

    def get_object(self, **kwargs):
        return get_object_or_404(User, username=self.kwargs.get('username'))


class ApproveUser(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        req =  Request.objects.filter(user=user, status=False).order_by('-id')
        if req.exists():    
            req.update(status=True)
        user.approved = True
        user.save()
        uploads = BookUpload.objects.filter(added_by=user)
        uploads.update(status='approved')
        books_id = uploads.values_list('books_id', flat=True)
        books = Book.objects.filter(id__in=books_id)
        books.update()
        return redirect(request.META.get("HTTP_REFERER"))


class RejectUser(View):
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
    template_name = 'dashboard/category_create.html'
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
            return redirect(reverse_lazy('book_list'))
        else:
            print(form.errors)
        return redirect(request.META.get('HTTP_REFERER'))


class BookDetail(BaseMixin, DetailView):
    model = Book
    template_name = 'dashboard/book_details.html'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['book_owners'] = BookUpload.objects.select_related('added_by').filter(book=self.get_object())
        return context_data


class UpdateBook(BaseMixin, UpdateView):
    model = Book
    template_name = 'dashboard/category_update.html'
    queryset = Book.objects.all()
    form_class = AdminBookForm

    def get_success_url(self):
        return reverse('dashboard:book_details',kwargs={'slug':self.get_object().slug})
    

class RequestList(BaseMixin, ListView):
    model = Request
    template_name = 'dashboard/request_list.html'
    paginate_by = 30
    queryset = Request.objects.select_related('user').filter(status=False).order_by('-id')


class Notification(BaseMixin):
    pass


class UserNotificationList(BaseMixin):
    pass


class CreateNotification(BaseMixin):
    pass


class AddCategory(BaseMixin, CreateView):
    model = Category
    template_name = 'dashboard/category_create.html'
    queryset = Category.objects.none()
    form_class = CategoryForm
    success_url = reverse_lazy('dashboard:category_list')


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
    template_name = 'dashboard/category_update.html'
    queryset = Category.objects.all()
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('dashboard:category_detail',kwargs={'slug':self.get_object().slug})
    

class DepositList(BaseMixin, ListView):
    model = Deposit
    template_name = 'dashboard/deposit_list.html'
    paginate_by = 30
    queryset = Deposit.objects.select_related('user').all().order_by('-id')


class DepositDetail(BaseMixin, DetailView):
    model = Deposit
    template_name = 'dashboard/deposit_detail.html'
    queryset = Deposit.objects.all()


class VerifyDeposit(View):
    def get(self, request, *args, **kwargs):
        deposit = get_object_or_404(Deposit, pk=self.kwargs.get('pk'))
        deposit.verified = True
        deposit.save()
        return redirect(request.META.get("HTTP_REFERER"))


class RejectDeposit(View):
    def get(self, request, *args, **kwargs):
        deposit = get_object_or_404(Deposit, pk=self.kwargs.get('pk'))
        deposit.verified = False
        deposit.save()
        return redirect(request.META.get("HTTP_REFERER"))



class OrderMixin(BaseMixin, ListView):
    model = Order
    template_name = 'dashboard/order_list.html'
    paginate_by = 30


class OrderList(OrderMixin):
    queryset = Order.objects.select_related('user').select_related('address').prefetch_related('books').filter(Q(delivery_status='none') | Q(dispatched=True, delivery_status='none' )).order_by('-id')


class CompletedOrderList(OrderMixin):
    queryset = Order.objects.select_related('user').select_related('address').prefetch_related('books').filter(delivery_status='delivered').order_by('-id')


class DispatchedOrderList(OrderMixin):
    queryset = Order.objects.select_related('user').select_related('address').prefetch_related('books').filter(dispatched=True, delivery_status='none').order_by('-id')


class CanceledOrderList(OrderMixin):
    queryset = Order.objects.select_related('user').select_related('address').prefetch_related('books').filter(delivery_status='canceled').order_by('-id')


class DispatchOrder(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.dispatched = True
        order.save()
        return redirect(request.META.get("HTTP_REFERER"))

class DelivereOrder(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.delivery_status = 'delivered'
        order.save()
        return redirect(request.META.get("HTTP_REFERER"))


class CanceleOrder(View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.delivery_status = 'canceled'
        order.save()
        return redirect(request.META.get("HTTP_REFERER"))