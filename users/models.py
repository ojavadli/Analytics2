from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

# Note: User model is now in core.models as a custom User model
# These models are kept for backward compatibility but may be deprecated

class InfluencerProfile(models.Model):
    """Legacy influencer profile - use core.InfluencerProfile instead"""
    CONTENT_CATEGORIES = [
        ('lifestyle', 'Lifestyle'),
        ('food', 'Food & Dining'),
        ('beauty', 'Beauty & Fashion'),
        ('fitness', 'Fitness & Health'),
        ('tech', 'Technology'),
        ('travel', 'Travel'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    instagram_username = models.CharField(max_length=100, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    follower_count = models.IntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    content_categories = models.CharField(
        max_length=50,
        choices=CONTENT_CATEGORIES,
        default='lifestyle'
    )
    weekly_allowance = models.IntegerField(default=1000)
    current_allowance = models.IntegerField(default=1000)
    allowance_reset_date = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"@{self.instagram_username}"
    
    def can_spend(self, amount):
        """Check if influencer can spend the given amount"""
        return self.current_allowance >= amount
    
    def spend_allowance(self, amount):
        """Deduct amount from current allowance"""
        if self.can_spend(amount):
            self.current_allowance -= amount
            self.save()
            return True
        return False
    
    def reset_weekly_allowance(self):
        """Reset weekly allowance"""
        self.current_allowance = self.weekly_allowance
        self.allowance_reset_date = timezone.now()
        self.save()

class BrandProfile(models.Model):
    """Legacy brand profile - use core.VenueProfile instead"""
    BUSINESS_CATEGORIES = [
        ('restaurant', 'Restaurant'),
        ('spa', 'Spa & Wellness'),
        ('fitness', 'Fitness & Gym'),
        ('retail', 'Retail & Shopping'),
        ('beauty', 'Beauty & Salon'),
        ('entertainment', 'Entertainment'),
        ('tech', 'Technology'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    business_category = models.CharField(
        max_length=50,
        choices=BUSINESS_CATEGORIES,
        default='restaurant'
    )
    description = models.TextField(max_length=1000, blank=True)
    website = models.URLField(blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.business_name
