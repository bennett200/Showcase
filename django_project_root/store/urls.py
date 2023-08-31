from django.urls import path
from allauth.account.views import SignupView, LoginView, LogoutView
from .views import *

urlpatterns = [
    path('', StoreFrontView.as_view(), name='storefront'),
    path('product/<slug:product_id>/', ProductCreateView.as_view(), name='product_detail_store'),
    path('products/', StoreAllProductsView.as_view(), name='all_products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/delete/<slug:pk>/', DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/checkout/success', CheckoutSuccess.as_view(), name='checkout_success'),
    path('customer/signup/', SignupView.as_view(template_name='store/account/signup.html'), name='store_signup'),
    path('customer/login/', LoginView.as_view(template_name='store/account/login.html'), name='store_login'),
    path('customer/logout/', LogoutView.as_view(template_name='store/account/logout.html'), {'next_page': 'profile', }, name='store_logout'),
    path('profile/', CustomerProfileView.as_view(), name='profile'),
    path('profile/order/history/', CustomerOrderHistoryView.as_view(), name='customer_order_history'),
    path('profile/order/history/<slug:pk>/', CustomerOrderHistoryDetailView.as_view(), name='order_history_detail'),
    path('search/', ProductsSearchResults.as_view(), name='store_search_results'),
    path('categories/', CategoriesListView.as_view(), name='store_categories_list'),
    path('categories/<slug:pk>/', ProductsByCategoryView.as_view(), name='products_by_category'),
    path('contact/', ContactStoreView.as_view(), name='store_contact'),
    path('contact/success/', ContactStoreSuccessView.as_view(), name='contact_success'),

]