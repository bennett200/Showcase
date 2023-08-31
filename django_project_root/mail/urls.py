from django.urls import path

from .views import *

urlpatterns = [
    path('', EmailListView.as_view(), name='email_list'),
    path('update/<slug:pk>/', EmailUpdateView.as_view(), name='email_update'),
    path('create/', EmailCreateView.as_view(), name='create_email'),
    path('details/<slug:pk>/', EmailDetailView.as_view(), name='email_details'),
    path('email/confirm/send/<slug:pk>/', EmailConfirmSendView.as_view(), name='email_send_confirm'),
    path('email/delete/<slug:pk>/', EmailDeleteView.as_view(), name='delete_email'),
]