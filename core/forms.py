from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Offer, ContentSubmission, InfluencerWaitlist
import json
import re

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            'title', 'description', 'reward_value', 'required_posts',
            'city', 'specific_location', 'max_influencers', 'min_followers',
            'target_categories', 'terms_conditions', 'expires_at'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Free Dinner for Instagram Post'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe what you are offering and any special instructions...'
            }),
            'reward_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': '200'
            }),
            'required_posts': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., 2 Instagram Stories and 1 Feed Post within one week'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'specific_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 123 Main St, Downtown location'
            }),
            'max_influencers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'value': 1
            }),
            'min_followers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'value': 10000
            }),
            'terms_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional terms or conditions...'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    target_categories = forms.MultipleChoiceField(
        choices=settings.CONTENT_CATEGORIES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        help_text="Select preferred influencer categories (optional)"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].choices = settings.SILICON_VALLEY_CITIES
        
        # Set labels and help texts
        self.fields['title'].help_text = "Clear, descriptive title for your offer"
        self.fields['reward_value'].help_text = "Dollar value of the reward/service"
        self.fields['required_posts'].help_text = "Specify exactly what content you expect"
        self.fields['max_influencers'].help_text = "How many influencers can claim this offer"
        self.fields['min_followers'].help_text = "Minimum follower count required"
        self.fields['expires_at'].help_text = "When does this offer expire? (optional)"
    
    def clean_reward_value(self):
        value = self.cleaned_data['reward_value']
        if value <= 0:
            raise ValidationError("Reward value must be positive")
        if value > 5000:
            raise ValidationError("Reward value cannot exceed $5000")
        return value
    
    def clean_min_followers(self):
        followers = self.cleaned_data['min_followers']
        if followers < 1000:
            raise ValidationError("Minimum follower count should be at least 1000")
        return followers
    
    def save(self, commit=True):
        offer = super().save(commit=False)
        
        # Convert target_categories list to JSON
        if self.cleaned_data['target_categories']:
            offer.target_categories = list(self.cleaned_data['target_categories'])
        else:
            offer.target_categories = []
        
        if commit:
            offer.save()
        return offer

class ContentSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContentSubmission
        fields = ['content_type', 'caption_text', 'media_file', 'instagram_url']
        
        widgets = {
            'content_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'caption_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Paste your Instagram caption here...'
            }),
            'media_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/p/...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set labels and help texts
        self.fields['content_type'].help_text = "Type of content you're submitting"
        self.fields['caption_text'].help_text = "The caption you used or plan to use"
        self.fields['media_file'].help_text = "Upload your content file (image or video)"
        self.fields['instagram_url'].help_text = "Link to your live Instagram post (optional)"
        
        # Make caption_text required
        self.fields['caption_text'].required = True
    
    def clean_media_file(self):
        file = self.cleaned_data.get('media_file')
        
        if file:
            # Check file size (max 50MB)
            if file.size > 50 * 1024 * 1024:
                raise ValidationError("File size cannot exceed 50MB")
            
            # Check file type
            allowed_types = [
                'image/jpeg', 'image/png', 'image/gif', 'image/webp',
                'video/mp4', 'video/quicktime', 'video/x-msvideo'
            ]
            
            if file.content_type not in allowed_types:
                raise ValidationError("File type not supported. Please upload an image or video.")
        
        return file
    
    def clean_instagram_url(self):
        url = self.cleaned_data.get('instagram_url')
        
        if url and not ('instagram.com' in url or 'instagr.am' in url):
            raise ValidationError("Please provide a valid Instagram URL")
        
        return url
    
    def clean(self):
        cleaned_data = super().clean()
        media_file = cleaned_data.get('media_file')
        instagram_url = cleaned_data.get('instagram_url')
        
        # Require either media file or Instagram URL
        if not media_file and not instagram_url:
            raise ValidationError("Please either upload a media file or provide an Instagram URL")
        
        return cleaned_data

class OfferFilterForm(forms.Form):
    """Form for filtering offers on the offer list page"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search offers, brands...'
        })
    )
    
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + settings.BUSINESS_CATEGORIES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    city = forms.ChoiceField(
        choices=[('', 'All Cities')] + settings.SILICON_VALLEY_CITIES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('-reward_value', 'Highest Value'),
            ('reward_value', 'Lowest Value'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    min_value = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min $'
        })
    )
    
    max_value = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max $'
        })
    )

class ContentApprovalForm(forms.Form):
    """Form for brand to approve or reject content"""
    
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Request Revision'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    feedback = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional feedback for the influencer...'
        }),
        help_text="Provide feedback if requesting revisions"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        feedback = cleaned_data.get('feedback')
        
        if action == 'reject' and not feedback:
            raise ValidationError("Please provide feedback when requesting revisions")
        
        return cleaned_data

class RedeemForm(forms.Form):
    """Form for redeeming offers"""
    
    redeem_code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter redeem code',
            'style': 'letter-spacing: 2px; font-family: monospace;'
        })
    )
    
    def clean_redeem_code(self):
        code = self.cleaned_data['redeem_code'].upper().strip()
        
        if len(code) != 8:
            raise ValidationError("Redeem code must be 8 characters")
        
        return code 

class InfluencerWaitlistForm(forms.ModelForm):
    class Meta:
        model = InfluencerWaitlist
        fields = ['instagram_username', 'email']
        widgets = {
            'instagram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Instagram username (without @)',
                'help_text': 'We will analyze your profile and followers'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com (optional)',
                'help_text': 'We will notify you when your application is reviewed'
            })
        }
    
    def clean_instagram_username(self):
        username = self.cleaned_data['instagram_username']
        
        # Remove @ symbol if present
        username = username.replace('@', '').strip()
        
        # Validate Instagram username format
        if not re.match(r'^[a-zA-Z0-9._]+$', username):
            raise ValidationError(
                "Instagram username can only contain letters, numbers, dots, and underscores"
            )
        
        if len(username) < 1:
            raise ValidationError("Instagram username is required")
        
        if len(username) > 30:
            raise ValidationError("Instagram username cannot be longer than 30 characters")
        
        # Check if already in waitlist
        if InfluencerWaitlist.objects.filter(instagram_username=username).exists():
            raise ValidationError(
                "This Instagram username is already in our waitlist. "
                "Please contact us if you need to update your application."
            )
        
        return username 