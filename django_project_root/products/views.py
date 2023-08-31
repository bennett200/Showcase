from typing import Any, Dict
from django.db.models.query import QuerySet
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.core.mail import send_mail
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, request
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from store.models import OrderItem, Order
from accounts.models import User
from .forms import ProductForm, CategoriesForm, OrderUpdateForm
from .models import Product, Categories
from django.contrib.auth.decorators import user_passes_test

from mail.models import Email

# Create your views here.



#PRODUCTS VIEWS
class ProductView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    ordering = ['title']
    
class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('products_list')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    template_name = 'products/product_update.html'
    form_class = ProductForm
    # success_url = reverse_lazy('products_list')
    context_object_name = 'products'
    object = Product.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_context'] = Categories.objects.all()
        return context
    
    def get_success_url(self):
        
        if 'categories/' in self.request.path:
            the_pk = self.request.POST.get('product_category')
            category = Categories.objects.get(pk=the_pk)

            return reverse_lazy('product_by_category', kwargs={'category': category})
        else:
            return reverse_lazy('products_list')
    
    
    def form_valid(self, form):
        cleaned_stock = form.cleaned_data['stock']
        cleaned_id = form.cleaned_data['id_hidden']
        order_items = OrderItem.objects.filter(product=cleaned_id)
        for items in order_items:
            if items.quantity > cleaned_stock:
                items.quantity = cleaned_stock
                items.save()
        return super().form_valid(form)

   
        
        
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    template_name = 'products/product_delete.html'
    success_url = reverse_lazy('products_list')

#CATEGORIES VIEWS

class CategoriesListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Categories
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    ordering = ['category_name']
    
    
class CategoriesCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Categories
    template_name = 'products/category_create.html'
    form_class = CategoriesForm
    context_object_name = 'categories'
    success_url = reverse_lazy('category_list')
    
class CategoriesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Categories
    template_name = 'products/category_update.html'
    form_class = CategoriesForm
    context_object_name = 'categories'
    success_url = reverse_lazy('category_list')
    
class CategoriesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Categories
    template_name = 'products/category_delete.html'
    context_object_name = 'categories'
    success_url = reverse_lazy('category_list')
   
# SORTED PRODUCTS BY CATEGORY
class ProductsByCategoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    template_name = 'products/products_by_category.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(product_category__category_name=self.kwargs['category'])
    

#ORDER MODELS
class OrdersIncompleteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Order
    template_name = 'products/orders_incomplete_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(complete=False).order_by('-date_ordered')
        context['orders_count'] = Order.objects.filter(complete=False).count()


        return context
    
class OrdersCompleteListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Order
    template_name = 'products/orders_complete_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(complete=True).order_by('-date_ordered')
        context['orders_count'] = Order.objects.filter(complete=True).count()


        return context

class OrderItemsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = OrderItem
    template_name = 'products/order_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs['pk'])
        context['Items'] = OrderItem.objects.filter(order=self.kwargs['pk'])
        return context

class ProductDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = OrderItem
    template_name = 'products/product_detail.html'
    context_object_name = 'order_item'


class OrderStatusChange(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Order
    template_name = 'products/order_update.html'
    form_class = OrderUpdateForm
    context_object_name = 'order'
    success_url = reverse_lazy('orders_incomplete_list')
    
    def form_valid(self, form):
        instance = form.instance
        order = Order.objects.get(id=self.kwargs['pk'])
        if instance.complete == True:
            send_mail(
                'Order Update',
                'Your order has been processed and is now on the way to you!',
                'store@example.net',
                [order.customer.email],
               fail_silently = False,
            )
            form.save()
            return redirect(reverse_lazy('orders_incomplete_list'))
        else:
            messages.error(self.request, 'Form is invalid')
            form.save()
            return redirect(reverse_lazy('order_complete_list'))

    
   
        

class OrderUserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = User
    template_name = 'products/order_user_detail.html'
    context_object_name = 'user'
    
    
class CustomerOrderHistory(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Order
    template_name = 'products/user_orders_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(customer=self.kwargs['pk'])
        return context
    

class ProductSearchView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Product
    template_name = 'products/product_search_results.html'
    context_object_name = 'products'
    def get_queryset(self): 
        query = self.request.GET.get('q')
        return Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
        )
        
        
class OrderSearchView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Order
    template_name = 'products/order_search_results.html'
    context_object_name = 'orders'
    def get_queryset(self): 
        query = self.request.GET.get('q')
        if query.isdigit():
            return Order.objects.filter(
        Q(id__exact=query)
        )
        else:
            return Order.objects.filter(
        Q(customer__email__icontains=query)
        )
    
    
    
    