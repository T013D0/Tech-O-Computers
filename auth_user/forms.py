from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from store.models import Product

class RegisterForm(UserCreationForm):
    rut = forms.CharField(max_length=12, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['rut', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')
        
        if password != confirm_password:
            raise forms.ValidationError('The passwords do not match')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.rut = self.cleaned_data['rut']
        user.is_active = False

        if commit:
            user.save()
        
        return user
    
class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('The email does not exist')
        
        user = User.objects.get(email=email)
        
        if not user.check_password(password):
            raise forms.ValidationError('The password is incorrect')
        
        return cleaned_data
    
