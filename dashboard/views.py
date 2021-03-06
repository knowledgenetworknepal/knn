from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView
 
from .permissions import IsAdminMixin
from django.http import JsonResponse


from django.contrib.auth import get_user_model
from django.db.models import Q,F
from books.models import Book, Category, BookUpload, Order
from userapp.models import Request, Deposit, Notification as Notice
from books.forms import BookForm, CategoryForm, AdminBookForm
from base.models import Ads, Contact
from base.forms import AdForm
from blogs.models import Blog
from discussion.models import Quesiton
from events.models import Event
from blogs.forms import Blogform
from events.forms import Eventform

User = get_user_model()

class BaseMixin(IsAdminMixin):
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['notificaitons'] = Notice.objects.all().order_by('-id')
        return context_data


class DashboardView(BaseMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        context_data['total_users'] = User.objects.all().count()
        context_data['total_books'] = Book.objects.all().count()
        context_data['new_request'] = Request.objects.filter(status=False).count()
        context_data['new_order'] = Order.objects.filter(delivery_status='none').count()

        return context_data


class UserMixin(BaseMixin, ListView):
    model = User
    template_name = 'dashboard/userlist.html'
    paginate_by = 30


class UserListView(UserMixin):
    queryset = User.objects.all().order_by('-id')


class ApprovedUserList(UserMixin):
    queryset = User.objects.filter(approved=True).order_by('-id')


class UnapprovedUserList(UserMixin):
    queryset = User.objects.filter(approved=False).order_by('-id')


class UserSearch(UserMixin):
    def get_queryset(self):
        data = str(self.request.GET.get("q"))
        return User.objects.filter(Q(username__icontains=data) | Q(contact__icontains=data) | Q(email__icontains=data)).order_by('-id')        


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


class ApproveUser(BaseMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        req =  Request.objects.filter(user=user, status=False).order_by('-id')
        if req.exists():    
            req.update(status=True)
        user.approved = True
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))


class ReceiveBook(BaseMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        uploads = BookUpload.objects.filter(added_by=user)
        uploads.update(status='approved')
        books_id = uploads.values_list('book_id', flat=True)
        books = Book.objects.filter(id__in=books_id)
        books.update(available=F('available')+1)
        user.books_received = True
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))


class RejectUser(BaseMixin, View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        user.approved = False
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))


class AddEvents(BaseMixin):
    pass


class BookMixin(BaseMixin, ListView):
    model = Book
    template_name = 'dashboard/booklist.html'
    paginate_by = 30


class BookList(BookMixin):
    queryset = Book.objects.filter(status=True).order_by('-id')


class AvailabelBookList(BookMixin):
    queryset = Book.objects.filter(available__gt=0, status=True).order_by('-id')


class UnavailabelBookList(BookMixin):
    queryset = Book.objects.filter(available__lte=0, status=True).order_by('-id')


class BookSearch(BookMixin):
    def get_queryset(self):
        return Book.objects.filter(Q(book_name__icontains=self.request.GET.get("q")) | Q(isbn__icontains=self.request.GET.get("q"))).order_by('-id')


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
            return redirect(reverse_lazy('dashboard:book_list'))
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
        print('success')
        return reverse('dashboard:book_details',kwargs={'slug':self.get_object().slug})


class DeleteBook(BaseMixin, View):
    def get(self, request):
        id = request.GET.get("pk", None)
        Book.objects.get(id=id).delete()
        data = {"deleted": True}
        return JsonResponse(data)


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


class CategoryDelete(BaseMixin, View):
    def get(self, request):
        id = request.GET.get("pk", None)
        Category.objects.get(id=id).delete()
        data = {"deleted": True}
        return JsonResponse(data)


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


class OrderSearch(OrderMixin):
    def get_queryset(self):
        return Order.objects.select_related('user').select_related('address').prefetch_related('books').filter(Q(user__username__icontains=self.request.GET.get("q")) | Q(user__contact__icontains=self.request.GET.get("q"))).order_by('-id')


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


class AdsView(BaseMixin, ListView):
    model = Ads
    template_name = 'dashboard/ads_list.html'
    queryset = Ads.objects.all().order_by('-id')
    paginate_by = 30


class AdsDetailView(BaseMixin, DetailView):
    model = Ads
    template_name = 'dashboard/ad_detail.html'
    queryset = Ads.objects.all()


class CreateAd(BaseMixin, CreateView):
    model = Ads
    template_name = 'dashboard/category_create.html'
    queryset = Ads.objects.none()
    form_class = AdForm
    success_url = reverse_lazy('dashboard:ads')


class UpdateAd(BaseMixin, UpdateView):
    model = Ads
    template_name = 'dashboard/category_update.html'
    queryset = Ads.objects.all()
    form_class = AdForm

    def get_success_url(self):
        return reverse('dashboard:ad_details',kwargs={'pk':self.get_object().pk})


class DeleteAd(BaseMixin, View):
    def get(self, request):
        id = request.GET.get("pk", None)
        Ads.objects.get(id=id).delete()
        data = {"deleted": True}
        return JsonResponse(data)


class ContactView(BaseMixin, ListView):
    model = Contact
    template_name = 'dashboard/contact.html'
    queryset = Contact.objects.all().order_by('-id')


class BlogListView(BaseMixin, ListView):
    model = Blog
    template_name = 'dashboard/blog_list.html'
    queryset = Blog.objects.all().order_by('-id')
    paginate_by = 30


class BlogDetailView(BaseMixin, DetailView):
    model = Blog
    template_name = 'dashboard/blog_detail.html'
    queryset = Blog.objects.prefetch_related('category').all()


class CreateBlog(BaseMixin, CreateView):
    model = Blog
    template_name = 'dashboard/category_create.html'
    queryset = Blog.objects.none()
    form_class = Blogform
    success_url = reverse_lazy('dashboard:blog_list')


class UpdateBlog(BaseMixin, UpdateView):
    model = Blog
    template_name = 'dashboard/category_update.html'
    queryset = Blog.objects.all()
    form_class = Blogform

    def get_success_url(self):
        return reverse('dashboard:blog_details',kwargs={'pk':self.get_object().pk})


class DeleteBlog(BaseMixin, View):
    def get(self, request):
        id = request.GET.get("pk", None)
        Blog.objects.get(id=id).delete()
        data = {"deleted": True}
        return JsonResponse(data)


class EventListView(BaseMixin, ListView):
    model = Event
    template_name = 'dashboard/event_list.html'
    queryset = Event.objects.prefetch_related('event_of').all().order_by('-id')
    paginate_by = 30


class EventDetailView(BaseMixin, DetailView):
    model = Event
    template_name = 'dashboard/event_detail.html'
    queryset = Event.objects.prefetch_related('event_of').prefetch_related('event_of__user').all()


class CreateEvent(BaseMixin, CreateView):
    model = Event
    template_name = 'dashboard/category_create.html'
    queryset = Event.objects.none()
    form_class = Eventform
    success_url = reverse_lazy('dashboard:event_list')


class UpdateEvent(BaseMixin, UpdateView):
    model = Event
    template_name = 'dashboard/category_update.html'
    queryset = Event.objects.all()
    form_class = Eventform

    def get_success_url(self):
        return reverse('dashboard:event_detail',kwargs={'pk':self.get_object().pk})


class DeleteEvent(BaseMixin, View):
    def get(self, request):
        id = request.GET.get("pk", None)
        Event.objects.get(id=id).delete()
        data = {"deleted": True}
        return JsonResponse(data)


