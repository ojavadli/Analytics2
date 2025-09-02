from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import InfluencerProfile, BrandProfile
import re

class InfluencerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    
    instagram_username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Instagram Username (without @)'
        }),
        help_text="Your Instagram username without the @ symbol"
    )
    
    category = forms.ChoiceField(
        choices=settings.CONTENT_CATEGORIES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Primary category of your content"
    )
    
    city = forms.ChoiceField(
        choices=settings.SILICON_VALLEY_CITIES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Your primary location in Silicon Valley"
    )
    
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Tell us about yourself and your content...'
        }),
        help_text="Brief description of yourself and your content style (optional)"
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
        
        # Update help texts
        self.fields['username'].help_text = "Choose a unique username for your hAIpClub account"
        self.fields['email'].help_text = "We'll use this to send you important updates"
        
        # Make fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    
    def clean_instagram_username(self):
        username = self.cleaned_data['instagram_username']
        
        # Remove @ if present
        username = username.replace('@', '')
        
        # Validate Instagram username format
        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            raise ValidationError("Instagram username can only contain letters, numbers, dots, and underscores")
        
        if len(username) < 1 or len(username) > 30:
            raise ValidationError("Instagram username must be between 1 and 30 characters")
        
        # Check if username is already taken
        if InfluencerProfile.objects.filter(instagram_username=username).exists():
            raise ValidationError("This Instagram username is already registered")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered")
        
        return email

class BrandRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact First Name'
        }),
        help_text="First name of the primary contact person"
    )
    
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contact Last Name'
        }),
        help_text="Last name of the primary contact person"
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Email Address'
        }),
        help_text="Business email address for communications"
    )
    
    business_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Business Name'
        }),
        help_text="Official name of your business"
    )
    
    category = forms.ChoiceField(
        choices=settings.BUSINESS_CATEGORIES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="Primary category of your business"
    )
    
    address = forms.CharField(
        max_length=300,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Business Address'
        }),
        help_text="Full business address"
    )
    
    city = forms.ChoiceField(
        choices=settings.SILICON_VALLEY_CITIES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text="City where your business is located"
    )
    
    description = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Tell us about your business...'
        }),
        help_text="Brief description of your business and what you offer (optional)"
    )
    
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://yourbusiness.com'
        }),
        help_text="Your business website (optional)"
    )
    
    instagram_handle = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Instagram Handle (without @)'
        }),
        help_text="Your business Instagram handle (optional)"
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(555) 123-4567'
        }),
        help_text="Business phone number (optional)"
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
        
        # Update help texts
        self.fields['username'].help_text = "Choose a unique username for your hAIpClub account"
        
        # Make fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    
    def clean_business_name(self):
        name = self.cleaned_data['business_name']
        
        # Check if business name is already taken
        if BrandProfile.objects.filter(business_name__iexact=name).exists():
            raise ValidationError("A business with this name is already registered")
        
        return name
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered")
        
        return email
    
    def clean_instagram_handle(self):
        handle = self.cleaned_data.get('instagram_handle', '')
        
        if handle:
            # Remove @ if present
            handle = handle.replace('@', '')
            
            # Validate Instagram handle format
            if not re.match(r'^[a-zA-Z0-9._]+$', handle):
                raise ValidationError("Instagram handle can only contain letters, numbers, dots, and underscores")
        
        return handle

class InfluencerProfileForm(forms.ModelForm):
    class Meta:
        model = InfluencerProfile
        fields = [
            'instagram_username', 'category', 'city', 'bio',
            'follower_count', 'following_count', 'post_count', 'engagement_rate'
        ]
        
        widgets = {
            'instagram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram Username'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'follower_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'following_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'post_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
            'engagement_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'step': '0.01'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].choices = settings.CONTENT_CATEGORIES
        self.fields['city'].choices = settings.SILICON_VALLEY_CITIES
        
        # Set help texts
        self.fields['instagram_username'].help_text = "Your Instagram username (will fetch updated data)"
        self.fields['bio'].help_text = "Brief description of yourself and your content"
        self.fields['follower_count'].help_text = "Automatically updated from Instagram"
        self.fields['engagement_rate'].help_text = "Calculated from your recent posts"

class BrandProfileForm(forms.ModelForm):
    class Meta:
        model = BrandProfile
        fields = [
            'business_name', 'category', 'address', 'city', 'description',
            'website', 'instagram_handle', 'phone_number'
        ]
        
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Business Name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Business Address'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your business...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourbusiness.com'
            }),
            'instagram_handle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Instagram Handle'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(555) 123-4567'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].choices = settings.BUSINESS_CATEGORIES
        self.fields['city'].choices = settings.SILICON_VALLEY_CITIES
        
        # Set help texts
        self.fields['business_name'].help_text = "Official name of your business"
        self.fields['description'].help_text = "Brief description of your business and services"
        self.fields['website'].help_text = "Your business website (optional)"
        self.fields['instagram_handle'].help_text = "Your business Instagram handle (optional)"
        self.fields['phone_number'].help_text = "Business phone number (optional)"

class UserBasicInfoForm(forms.ModelForm):
    """Form for updating basic user information"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all fields required
        for field in self.fields.values():
            field.required = True 