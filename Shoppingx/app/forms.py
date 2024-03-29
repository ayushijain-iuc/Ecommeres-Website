from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from . models import Customer
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


# class CustomRegistrationForm(UserCreationForm):
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
#     class Meta:
#         model=User
#         fields=['username','email','password1','password2']
#         labels={'email':'Email', 'password1':'Password','password2':'Cofirm Password(again)'}
#         widgets={'username':forms.TextInput(attrs={'class':'form-control'})}


class CustomRegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email', 'password1': 'Password', 'password2': 'Confirm Password(again)'}
        widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}
    def clean_email(self):
        email = self.cleaned_data.get('email')    
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already associated with an account.")
        return email
        
class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password=forms.CharField(label=("password"), strip='False', widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordchangeField(PasswordChangeForm):
    old_password=forms.CharField(label=("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1=forms.CharField(label=("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class MyPasswordResetForm(PasswordResetForm): 
    email = forms.EmailField(label=("Email"),max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label=("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2=forms.CharField(label=("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields=['id','name','locality','city','zipcode','state']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}),
                   'city':forms.TextInput(attrs={'class':'form-control'}),'state':forms.Select(attrs={'class':'form-control'}),
                   'zipcode':forms.NumberInput(attrs={'class':'form-control'})}
             
