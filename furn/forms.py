from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Address




class SignupForm(UserCreationForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User 
        fields = ['full_name', 'username', 'email', 'password1', 'password2']


    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']= 'form-control'
        self.fields['password1'].widget.attrs['class']= 'form-control'
        self.fields['password2'].widget.attrs['class']= 'form-control'
        

class ProfileForm(ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
   
    class Meta:
        model = User 
        fields = ['username', 'email']

class AddressForm(ModelForm):

    class Meta:
        model = Address 
        exclude = ['user']

    def __init__(self, *args, **kwargs):
            super(AddressForm, self).__init__(*args, **kwargs)

            self.fields['country'].widget.attrs['class']= 'form-control'
            self.fields['state'].widget.attrs['class']= 'form-control'
            self.fields['address'].widget.attrs['class']= 'form-control'
            self.fields['zip'].widget.attrs['class']= 'form-control'
            self.fields['phone_number'].widget.attrs['class']= 'form-control'
            self.fields['email'].widget.attrs['class']= 'form-control'

