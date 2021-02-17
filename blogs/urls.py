from django.urls import path


from .views import BlogList, BlogDetail, AddComment


urlpatterns  = [
    path('blog/', BlogList.as_view(), name='blog_list' ),
    path('blog/<str:slug>/', BlogDetail.as_view(), name='blog_detail' ),
    path('blog/<str:slug>/comment/', AddComment.as_view(), name='add_comment'),

]