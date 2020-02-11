from django import forms
from .models import Employee
from .models import *

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('fullname','mobile','emp_code','position')
        labels = {
            'fullname':'Full Name',
            'emp_code':'EMP. Code'
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = "Select"
        self.fields['emp_code'].required = False

class ProductsModelForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('product_code', 'product_name', 'sales_price')
        labels = {
            'product_code':'Product Code',
            'product_name':'Product Name',
            'sales_price':'Sales Price',
        }


class ProductsSalesModelForm(forms.ModelForm):
    product_name = forms.CharField(label='Product Name', initial="",)
    def __init__(self, *args, **kwargs):
        super(ProductsSalesModelForm, self).__init__(*args, **kwargs)
        self.fields['unit_price'].widget.attrs['readonly'] = True
        self.fields['total_price'].widget.attrs['readonly'] = True
        self.fields['product_name'].widget.attrs['readonly'] = True
        self.fields['product_name'].initial = "A"
        self.fields['product_name'].required = False

    class Meta:
        model = Products_Sales
        fields = ('unit_price', 'total_quantity', 'total_price', 'product_code')
        labels = {
            'product_code':'Product Code',
            'unit_price':'Sales Price',
            'total_price':'Total Price',
            'total_quantity':'Total Quantity',
        }

