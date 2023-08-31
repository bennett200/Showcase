from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpRequest
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class HomePageView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_staff
    template_name = '_base.html'
    
    
# class Register(CreateView):
#     template_name = 'registration/signup.html'
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('account_login')
    
# class MyLoginView(LoginView):
    
#     def get_success_url(self):
#         return reverse_lazy('home') 
    
#     def form_invalid(self, form):
#         messages.error(self.request,'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))

class SignoutConfirmView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('account_login')
    template_name = 'accounts/confirm_signout.html'

class SignedOutView(TemplateView):
    template_name = 'accounts/signed_out.html'
    
    def get(self, request:HttpRequest):
        logout(request)
        return render(request, self.template_name)
    
    
class AboutView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_staff
    template_name = 'accounts/about.html'
        


    
 