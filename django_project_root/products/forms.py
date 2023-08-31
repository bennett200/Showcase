from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import HiddenInput

from store.models import Order
from .models import Product, Categories

#FORMS
class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'
        
   
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "Sorry, a product with this title already exists inside selected category."
            }
        }
        widgets = {'id_hidden': HiddenInput(),}
   

    def clean(self):
        cleaned_data = super().clean()
        stock_amount = self.cleaned_data.get('stock')
        display_value = self.cleaned_data.get('display_product')
        
        if stock_amount <= 0 and display_value == True:
            raise forms.ValidationError(('If you wish to display this value in your shop, it must be in stock.'), code='invalid')
        return cleaned_data    


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['complete', ]
       
