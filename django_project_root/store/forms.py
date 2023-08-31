from django import forms
from django.forms import HiddenInput, NumberInput
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .models import OrderItem, Order
from accounts.models import User
from django.contrib import messages


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['useless', 'quantity', 'filter_item']
        widgets = {'useless': HiddenInput(), 'filter_item': HiddenInput(), 'quantity': NumberInput(attrs={'class': 'numberinput',})}
        
    
class OrderItemDeleteForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'


# class OrderItemTrackerForm(forms.ModelForm):
#     class Meta:
#         model = OrderItemTracker
#         fields = ['quantity',]
     
        
# class OrderItemTrackerUpdateForm(forms.ModelForm):
#     class Meta:
#         model = OrderItemTracker
#         fields = ['quantity', 'filter_item']
#         widgets = {'filter_item': HiddenInput(),}
        

class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'notes']
      
        
# class CheckoutOrderTracker(forms.ModelForm):
#     class Meta:
#         model = OrderItemTracker
#         fields = ['complete', ]
#         widgets = {'complete': HiddenInput(),}
   
class UserImageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_img', ]
        
        
class ContactStoreForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'body-in'}))
    
    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.user = kwargs.pop('user', None)
        super(ContactStoreForm, self).__init__(*args,**kwargs)
        
    def send_email(self):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['body']
        from_email = self.user.email
        admin = User.objects.filter(is_superuser=True).first()
        if subject and message and from_email:
            send_mail(subject, message, from_email, [admin])
          
