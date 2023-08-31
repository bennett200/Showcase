from django.urls import path

from .views import *

urlpatterns = [
    #PRODUCT MODEL VIEWS
    path('', ProductView.as_view(), name='products_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('update/<slug:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('delete/<slug:pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('product/detail/<slug:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/search/', ProductSearchView.as_view(), name='product_search_results'),
    #CATEGORIES MODEL VIEWS
    path('categories/', CategoriesListView.as_view(), name='category_list'),
    path('categories/create/', CategoriesCreateView.as_view(), name='category_create'),
    path('categories/update/<slug:pk>/', CategoriesUpdateView.as_view(), name='category_update'),
    path('categories/delete/<slug:pk>/', CategoriesDeleteView.as_view(),  name='category_delete'),
    #PRODUCTS BY CATEGORY
    path('categories/by_product/<str:category>/', ProductsByCategoryView.as_view(), name='product_by_category'),
    path('categories/products/update/<slug:pk>', ProductUpdateView.as_view(), name='products_by_cat_up'),
    #ORDERS MODEL VIEWS
    path('orders/', OrdersIncompleteListView.as_view(), name='orders_incomplete_list'),
    path('orders/history/', OrdersCompleteListView.as_view(), name='order_complete_list'),
    path('orders/order_items/<slug:pk>/', OrderItemsView.as_view(), name='order_items'),
    path('order/update/<slug:pk>/', OrderStatusChange.as_view(), name='order_update'),
    path('order/user/<slug:pk>/', OrderUserDetailView.as_view(), name='order_user_detail'),
    path('order/user/order-history/<slug:pk>/', CustomerOrderHistory.as_view(), name='user_order_history'),
    path('orders/search/', OrderSearchView.as_view(), name='order_search_results'),

    
]