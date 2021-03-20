from django.urls import path
from .views import *

urlpatterns  = [
    path('discussion/', AllQuestionsView.as_view(), name='discussion_list' ),
    path('discussion/<str:slug>/', DiscussionDetail.as_view(), name='discussion_detail' ),
    path('discussion/cateogory/<str:slug>/', CategoryDiscussioView.as_view(), name='category_discussion' ),

    path('discussion/<str:slug>/comment/', AddComment.as_view(), name='discussion_comment'),
    path('discussion/new/add/', AddDiscussion.as_view(), name='add_discussion'),

]