from django import forms #type: ignore
from .models import Product, Category, Review, Newsletter
from django.contrib.auth.models import User #type: ignore
from django.contrib.auth.forms import UserCreationForm #type: ignore

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name', 'category_description', 'category_image']  # Add other fields as necessary

class ProductForm(forms.ModelForm):
    product_category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label="category_name")

    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_details', 'product_image', 'product_category']  # Add other fields as necessary


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Your Email'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 
        'rows': 8, 
        'placeholder': 'Message'
    }))

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'rating-select'
        })
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Write your review here...'
        }),
        label='Review'
    )
    
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email Address',
            'required': True
        }),
        label=''
    )
    
    class Meta:
        model = Newsletter
        fields = ['email']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("This email is already subscribed to our newsletter.")
        return email
