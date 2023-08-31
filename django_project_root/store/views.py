from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, FormView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import Product, Categories
from .models import OrderItem, Order
from django.core.mail import send_mail
from django.db.models import Q

from accounts.models import User
from .forms import *
from django import forms
from django.db.models import F, Sum

# Create your views here.

class StoreFrontView(ListView):
    template_name = 'store/storefront.html'
    model = Product
    def get_context_data(self, **kwargs):
        context = super(StoreFrontView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(display_product=True).order_by('-created_at')[:6]
        return context
    

class StoreAllProductsView(ListView):
    template_name = 'store/all_products.html'
    model = Product
    def get_context_data(self, **kwargs):
        context = super(StoreAllProductsView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(display_product=True).order_by('title')
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('profile')
    template_name = 'store/product_detail.html'
    model = OrderItem
    form_class = OrderItemForm
    # quantity_form_class = OrderItemTrackerForm
    def get_success_url(self):
        return self.request.path
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # quantity_form = self.quantity_form_class(prefix='quantity_form')

        # context['quantity_form'] = quantity_form
        context['OrderItem'] = OrderItem.objects.all()
        context['product'] = Product.objects.get(id=self.kwargs['product_id'])
        context['amount_requested'] = OrderItem.objects.filter(product = self.kwargs['product_id'], customer=self.request.user, added_to_order=False).first()
        
        return context
    
    # def form_valid(self, form):
    #     form.instance.product_id = self.kwargs['product_id']
    #     # form.instance.user = self.request.user
    #     return super().form_valid(form)    
    
    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(**self.get_form_kwargs())
    #     quantity_form = self.quantity_form_class(prefix='quantity_form')
    #     return render(request, self.template_name, {'form': form, 'quantity_form': quantity_form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # quantity_form = self.quantity_form_class(request.POST, prefix='quantity_form')
        form.instance.product_id = self.kwargs['product_id']
       
        if form.is_valid():
            if OrderItem.objects.filter(product = self.kwargs['product_id'], customer=request.user, added_to_order=False).exists():
                orderitem = OrderItem.objects.get(product = self.kwargs['product_id'], customer=request.user, added_to_order=False)

                # myitem = OrderItem.objects.get(product = self.kwargs['product_id'], customer=request.user, id=orderitem.id)
                # raise forms.ValidationError(('This crap dont work'), code='invalid')
                # thetracker = OrderItemTracker.objects.get(order_item = myitem)
                # orderitem = OrderItemTracker.objects.get(order_item=myitem, user=request.user)
                cleaned_quantity = form.instance.quantity
                if cleaned_quantity > orderitem.product.stock:
                    messages.error(request, 'Sorry, please select an amount within the available stock')
                    
                elif (cleaned_quantity + orderitem.quantity) > orderitem.product.stock: 
                    messages.error(request, 'Sorry, you have already requested the maximum amount available')
                
                elif cleaned_quantity <= 0:
                    messages.error(request, f'Sorry, please select a quantity greater than 0')
                    
                else:
                    OrderItem.objects.filter(product = orderitem.product, customer=request.user, added_to_order=False).update(quantity=F('quantity')+cleaned_quantity)
                # quantity_form.instance.order_item = OrderItem.objects.get(id=myitem.pk)
                # quantity_form.save()   
            else:
                myitem = Product.objects.get(id=self.kwargs['product_id'])
                cleaned_quantity = form.instance.quantity
                
                if cleaned_quantity > myitem.stock: 
                    messages.error(request, 'Sorry, that exceeds the current stock of this item')
                elif cleaned_quantity <= 0:
                    messages.error(request, f'Sorry, please select a quantity greater than 0')
                else:
                    form.instance.product = Product.objects.get(id=myitem.id)
                    form.instance.customer = request.user
                    
                    form.save()   

            return redirect(self.request.path)

# class CartView(ListView):
#     template_name = 'store/cart.html' 
#     model = OrderItemTracker
#     context_object_name = 'Items'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['Items'] = OrderItemTracker.objects.all()
#         return context

class CartView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('profile')
    template_name = 'store/cart.html' 
    model = OrderItem
    context_object_name = 'Items'
    form_class = OrderItemForm
    
    #Queries and stuff
   
    
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderItemTrackObject = OrderItem.objects.filter(customer=self.request.user, added_to_order=False)
        context['Items'] = OrderItemTrackObject
        context['form'] = OrderItemForm
        cart_total = 0
        for item in OrderItemTrackObject:
            cart_total += item.order_item_price
            
        context['cart_total'] = cart_total   
        
        return context
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
       
        if form.is_valid():
            
            filteritem = form.cleaned_data['filter_item'] 
            cleaned_quantity = form.instance.quantity
            
            amount = OrderItem.objects.get(id=filteritem, customer=request.user)
            
            if cleaned_quantity > amount.product.stock:
                messages.error(request, 'Sorry, that exceeds the current stock of this item')
            elif (cleaned_quantity) > amount.product.stock:
                messages.error(request, 'Sorry, you have already requested the maximum amount available')
            elif cleaned_quantity <= 0:
                messages.error(request, 'Sorry, please select a quantity greater than 0')
            else:
                OrderItem.objects.filter(id=filteritem, customer=request.user).update(quantity=cleaned_quantity)

           
        return redirect(self.request.path)
    
    
class DeleteCartItemView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('profile')
    template_name = 'store/delete_cart_item.html'
    model = OrderItem
    success_url = reverse_lazy('cart')
    
   
class CheckoutView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('profile')
    template_name = 'store/checkout.html'
    model = Order
    form_class = OrderCheckoutForm
    
    def get_success_url(self):
        return self.request.path
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Order'] = Order.objects.filter(customer=self.request.user)
        context['order_trackers'] = OrderItem.objects.filter(customer=self.request.user, added_to_order=False)

        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)        
        if form.is_valid():
            form.instance.customer = request.user

            n = form.save()
            
            myitems = OrderItem.objects.filter(customer=request.user, added_to_order=False)
            order = Order.objects.get(id=n.pk)
            for item in myitems:
                item.order = order
                item.added_to_order = True
                item.product.stock = (item.product.stock - item.quantity)
                item.product.save()
                item.save()
            send_mail(
                'Order Success',
                f'You have successfully placed your order with the id number {order.id}',
                'Store@example.net',
               [order.customer],
               fail_silently = False,
            )
        return redirect(request.path)
    
class CheckoutSuccess(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('profile')
    template_name = 'store/checkout_success.html'
    
    
class CustomerProfileView(TemplateView):
    template_name = 'store/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['Orders'] = Order.objects.filter(customer=self.request.user).count()

        return context
   
    
    
class CustomerOrderHistoryView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('profile')
    template_name = 'store/customer_order_history.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Orders = Order.objects.filter(customer=self.request.user).order_by('-date_ordered')
        context['Orders'] = Orders
        
        return context
    
class CustomerOrderHistoryDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('profile')
    template_name = 'store/customer_order_history_detail.html'
    model = Order
    context_object_name = 'order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Orders = OrderItem.objects.filter(customer=self.request.user, order=self.kwargs['pk'])
        context['order_items'] = Orders
        cart_total = 0
        for item in Orders:
            cart_total += item.order_item_price
            
        context['cart_total'] = cart_total   
        return context

class ProductsSearchResults(ListView):
    model = Product
    template_name = 'store/products_search_results.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
class CategoriesListView(ListView):
    model = Categories
    template_name = 'store/categories_list.html'
    context_object_name = 'categories'
    
class ProductsByCategoryView(ListView):
    model = Product
    template_name = 'store/products_by_category.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(product_category=self.kwargs['pk'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Category'] = Categories.objects.get(id=self.kwargs['pk'])
        return context

class ContactStoreView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('profile')

    template_name = 'store/contact.html'
    form_class = ContactStoreForm
    
    success_url = reverse_lazy('contact_success')    

    def get_form_kwargs(self):
  
        kwargs = super(ContactStoreView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user

        return kwargs

    
    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
    
class ContactStoreSuccessView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('profile')

    template_name = 'store/contact_success.html'