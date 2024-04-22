from django import forms
from .models import Customer
from django.contrib.auth.models import User


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}))
    Confirm_Password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Enter Email"}))
    class Meta:
        model = Customer
        fields = ['full_name','address','email','username','password']
    
    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Full Name'
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Address'
        })
        
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken")
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        cpassword = cleaned_data.get("Confirm_Password")
        
        if password != cpassword:
            raise forms.ValidationError("Password does not match")
        return cleaned_data
    
class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter Password"}))
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid Username")
        
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError("Invalid Password")
        
        return cleaned_data
