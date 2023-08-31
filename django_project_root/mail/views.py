from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from accounts.models import User
from .forms import EmailBaseForm
from .models import Email
# Create your views here.

class EmailListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/emails_list.html'
    context_object_name = 'emails'

class EmailUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/email_update.html'
    form_class = EmailBaseForm
    context_object_name = 'email'
    def get_success_url(self):
        return reverse_lazy('email_update', kwargs={'pk': self.kwargs['pk']})
    
    def get_form(self, *args, **kwargs):
        form = super().get_form(self.form_class)
        if form.instance.all_users == True:
            form.fields.pop('message_recipients')
        return form
    
class EmailCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/email_create.html'
    form_class = EmailBaseForm
    success_url = reverse_lazy('email_list')
    

class EmailDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/email_detail.html'
    context_object_name = 'email'
    
    
    
class EmailConfirmSendView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/email_send_confirm.html'
    context_object_name = 'email'
    
    def post(self, request, *args, **kwargs):
        email = Email.objects.get(id=self.kwargs['pk'])
        allusers = User.objects.all()
        emails = []
        for users in allusers:
            emails.append(users.email)
        if request.method == 'POST':
            if request.POST['action'] == 'Send Email':
                if email.all_users == True:
                    send_mail(
                        email.subject,
                        email.body,
                        email.message_sender,
                        emails,
                    fail_silently = False,
                    )
                else:
                    send_mail(
                        email.subject,
                        email.body,
                        email.message_sender,
                        email.message_receivers,
                    fail_silently = False,
                    )
        return redirect('email_details', pk=self.kwargs['pk'])
    
class EmailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account_login')
    def test_func(self):
        return self.request.user.is_staff
    model = Email
    template_name = 'mail/email_delete.html'
    success_url = 'email_list'