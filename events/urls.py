from django.urls import path


from .views import EventList, EventDetail, event_regiseter


urlpatterns  = [
    path('event/', EventList.as_view(), name='event_list' ),
    path('event/<str:slug>/', EventDetail.as_view(), name='event_detail' ),
    path('event/<str:slug>/register/', event_regiseter, name='event_register' ),

]