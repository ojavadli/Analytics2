import uuid
import secrets
import qrcode
from io import BytesIO
from decimal import Decimal
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

class User(AbstractUser):
    """Enhanced User model with role-based access"""
    ROLE_CHOICES = [
        ('influencer', 'Influencer'),
        ('venue', 'Venue'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='influencer')
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class InfluencerProfile(models.Model):
    """Complete influencer profile with gamification"""
    TIER_CHOICES = [
        ('bronze', 'Bronze Member'),
        ('silver', 'Silver Member'), 
        ('gold', 'Gold Member'),
        ('elite', 'Elite SF Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    instagram_username = models.CharField(max_length=100, unique=True)
    follower_count = models.IntegerField(default=0)
    
    # Gamification System
    xp_points = models.IntegerField(default=0)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default='bronze')
    streak_days = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    total_redemptions = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Credit System
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    monthly_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    last_allowance_reset = models.DateTimeField(default=timezone.now)
    
    # QR Code System
    qr_code_token = models.CharField(max_length=255, unique=True, blank=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True)
    qr_code_active = models.BooleanField(default=True)
    
    # Analytics
    rocket_api_data = models.JSONField(default=dict, blank=True)
    verification_status = models.CharField(max_length=20, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.qr_code_token:
            self.qr_code_token = self.generate_qr_token()
        
        super().save(*args, **kwargs)
        
        if not self.qr_code_image:
            self.generate_qr_code()
    
    def generate_qr_token(self):
        """Generate secure unique QR token"""
        return f"haip_{self.user.id}_{secrets.token_urlsafe(32)}"
    
    def generate_qr_code(self):
        """Generate QR code image"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr_data = {
            'token': self.qr_code_token,
            'influencer_id': str(self.user.id),
            'tier': self.tier,
            'balance': str(self.current_balance)
        }
        qr.add_data(str(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        filename = f'qr_{self.user.username}_{self.user.id}.png'
        self.qr_code_image.save(filename, File(buffer), save=False)
    
    def add_xp(self, points, reason=""):
        """Add XP points and check for tier upgrades"""
        self.xp_points += points
        old_tier = self.tier
        
        # Tier progression logic
        if self.xp_points >= 10000:
            self.tier = 'elite'
        elif self.xp_points >= 5000:
            self.tier = 'gold'
        elif self.xp_points >= 1000:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'
        
        self.save()
        
        # Create achievement if tier upgraded
        if old_tier != self.tier:
            Achievement.objects.create(
                influencer=self,
                badge_type='tier_upgrade',
                title=f"Upgraded to {self.get_tier_display()}",
                description=f"Congratulations! You've reached {self.get_tier_display()} status.",
                xp_reward=500
            )
    
    def deduct_balance(self, amount):
        """Deduct amount from balance"""
        if self.current_balance >= amount:
            self.current_balance -= amount
            self.total_spent += amount
            self.save()
            return True
        return False
    
    def reset_monthly_allowance(self):
        """Reset monthly allowance"""
        self.current_balance = self.monthly_allowance
        self.last_allowance_reset = timezone.now()
        self.save()
    
    def get_tier_color(self):
        """Get tier color for UI"""
        colors = {
            'bronze': '#CD7F32',
            'silver': '#C0C0C0', 
            'gold': '#FFD700',
            'elite': '#FF6B35'
        }
        return colors.get(self.tier, '#CD7F32')
    
    def __str__(self):
        return f"@{self.instagram_username} - {self.get_tier_display()}"

class VenueProfile(models.Model):
    """Venue profile for partner restaurants"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='venue_profile')
    venue_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    cuisine_type = models.CharField(max_length=100, blank=True)
    average_bill = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Venue Settings
    max_redemption_amount = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    is_active = models.BooleanField(default=True)
    
    # Analytics
    total_redemptions = models.IntegerField(default=0)
    total_redeemed_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.venue_name

class Achievement(models.Model):
    """Gamification achievements and badges"""
    BADGE_TYPES = [
        ('first_signup', 'First Sign-up'),
        ('first_redemption', 'First Redemption'),
        ('tier_upgrade', 'Tier Upgrade'),
        ('streak_7', '7-Day Streak'),
        ('streak_30', '30-Day Streak'),
        ('top_monthly', 'Top 10 Monthly'),
        ('big_spender', 'Big Spender'),
        ('venue_explorer', 'Venue Explorer'),
        ('social_star', 'Social Media Star'),
    ]
    
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='achievements')
    badge_type = models.CharField(max_length=30, choices=BADGE_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    xp_reward = models.IntegerField(default=0)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['influencer', 'badge_type']
    
    def __str__(self):
        return f"{self.influencer.user.username} - {self.title}"

class Redemption(models.Model):
    """Transaction records for venue redemptions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='redemptions')
    venue = models.ForeignKey(VenueProfile, on_delete=models.CASCADE, related_name='redemptions')
    
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Transaction Details
    qr_token_used = models.CharField(max_length=255)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional Data
    notes = models.TextField(blank=True)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True)
    
    def save(self, *args, **kwargs):
        if self.status == 'confirmed' and not self.confirmed_at:
            self.confirmed_at = timezone.now()
            
            # Award XP for redemption
            self.influencer.add_xp(50, f"Redemption at {self.venue.venue_name}")
            
            # Update venue stats
            self.venue.total_redemptions += 1
            self.venue.total_redeemed_amount += self.amount
            self.venue.save()
            
            # Check for first redemption achievement
            if self.influencer.total_redemptions == 0:
                Achievement.objects.get_or_create(
                    influencer=self.influencer,
                    badge_type='first_redemption',
                    defaults={
                        'title': 'First Redemption!',
                        'description': 'Congratulations on your first redemption at a partner venue!',
                        'xp_reward': 100
                    }
                )
            
            self.influencer.total_redemptions += 1
            self.influencer.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.influencer.user.username} - ${self.amount} at {self.venue.venue_name}"

class ActivityLog(models.Model):
    """Comprehensive activity logging"""
    ACTION_TYPES = [
        ('signup', 'Sign Up'),
        ('redemption', 'Redemption'),
        ('qr_scan', 'QR Code Scan'),
        ('achievement', 'Achievement Earned'),
        ('tier_upgrade', 'Tier Upgrade'),
        ('balance_reset', 'Balance Reset'),
        ('admin_action', 'Admin Action'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_type_display()}"

class SystemSettings(models.Model):
    """Global system settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"

# Signal handlers for automatic achievements
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile based on user role"""
    if created:
        if instance.role == 'influencer':
            profile = InfluencerProfile.objects.create(user=instance)
            # Award signup achievement
            Achievement.objects.create(
                influencer=profile,
                badge_type='first_signup',
                title='Welcome to hAIpClub!',
                description='Welcome to the elite SF influencer network!',
                xp_reward=100
            )
            profile.add_xp(100, "Welcome bonus")
            
        elif instance.role == 'venue':
            VenueProfile.objects.create(user=instance)
        
        # Log signup activity
        ActivityLog.objects.create(
            user=instance,
            action_type='signup',
            description=f'New {instance.role} account created'
        )
