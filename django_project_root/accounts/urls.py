from django.urls import path

from .views import HomePageView, SignedOutView, SignoutConfirmView, AboutView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # path('register/', Register.as_view(), name='register'),
    path('confirm-signout/', SignoutConfirmView.as_view(), name='confirm_signout'),
    path('signed-out/', SignedOutView.as_view(), name='signed_out'),
    path('about/', AboutView.as_view(), name='about')
]