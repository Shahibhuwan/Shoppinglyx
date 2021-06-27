
from app.models import Customer
from django import forms
from django.contrib.auth import password_validation

from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import fields, widgets

from django.utils.translation import gettext, gettext_lazy as _
class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password' , widget =forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password' , widget =forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required =True , widget =forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email':'Email'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'),strip=False ,widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class': 'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False , widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label = _("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label = _("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))

class MyPasswordResetForm(PasswordChangeForm):
    email = forms.EmailField(label= ("Email"), max_length=254,widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm ):
     new_password1 = forms.CharField(label = _("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
     new_password2 = forms.CharField(label = _("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))
 
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}), 'locality':forms.TextInput(attrs={'class':'forms-control'}),'city':forms.TextInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),'zipcode':forms.NumberInput(attrs={'class':'form-control'})}


class BillingForm(forms.Form):
    name = forms.CharField(label='Name' , widget =forms.TextInput(attrs={'class': 'form-control'}))  
    state = forms.CharField(label='State' , widget =forms.TextInput(attrs={'class': 'form-control'}))
    locality =forms.CharField(label='' , widget =forms.TextInput(attrs={'class': 'form-control'}))
    totalamount = forms.CharField(label='Totalamount' , widget =forms.TextInput(attrs={'class': 'form-control'}))
    totalitems=forms.CharField(label='Quantity' , widget =forms.TextInput(attrs={'class': 'form-control'}))
    date= forms.DateTimeField(label='Date' , widget =forms.TextInput(attrs={'class': 'form-control'}))
      

#widget are used to use bootstrap class
#usercreationform is just a form which is inherited and thier field is customized which are which in meta class for our customize form creation