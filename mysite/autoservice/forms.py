from django import forms
from .models import OrderReview, CustomUser, Order
from django.contrib.auth.forms import UserCreationForm


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class OrderCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'car_return', 'user', 'status']
        widgets = {'car_return': forms.DateInput(attrs={'type': 'date'})}