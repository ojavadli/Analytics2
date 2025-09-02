from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    User, InfluencerProfile, VenueProfile, Achievement, 
    Redemption, ActivityLog, SystemSettings
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin with role-based functionality"""
    list_display = ('username', 'email', 'role', 'is_verified', 'date_joined', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('hAIpClub Info', {
            'fields': ('role', 'phone', 'profile_image', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('hAIpClub Info', {
            'fields': ('role', 'phone', 'is_verified')
        }),
    )

@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    """Comprehensive influencer profile management"""
    list_display = (
        'user', 'instagram_username', 'tier', 'xp_points', 
        'current_balance', 'total_redemptions', 'verification_status'
    )
    list_filter = ('tier', 'verification_status', 'created_at')
    search_fields = ('user__username', 'instagram_username')
    readonly_fields = (
        'qr_code_token', 'qr_code_preview', 'total_redemptions', 
        'total_spent', 'created_at', 'updated_at'
    )
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'instagram_username', 'follower_count')
        }),
        ('Gamification', {
            'fields': ('xp_points', 'tier', 'streak_days', 'total_redemptions')
        }),
        ('Credit System', {
            'fields': ('current_balance', 'monthly_allowance', 'total_spent', 'last_allowance_reset')
        }),
        ('QR Code System', {
            'fields': ('qr_code_token', 'qr_code_preview', 'qr_code_active')
        }),
        ('Analytics', {
            'fields': ('rocket_api_data', 'verification_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['reset_monthly_allowance', 'upgrade_to_elite', 'regenerate_qr_codes']
    
    def qr_code_preview(self, obj):
        if obj.qr_code_image:
            return format_html(
                '<img src="{}" width="100" height="100" />',
                obj.qr_code_image.url
            )
        return "No QR Code"
    qr_code_preview.short_description = "QR Code"
    
    def reset_monthly_allowance(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.reset_monthly_allowance()
            count += 1
        self.message_user(request, f'Reset allowance for {count} influencers.')
    reset_monthly_allowance.short_description = "Reset monthly allowance"
    
    def upgrade_to_elite(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.tier = 'elite'
            profile.add_xp(1000, "Admin upgrade to Elite")
            count += 1
        self.message_user(request, f'Upgraded {count} influencers to Elite tier.')
    upgrade_to_elite.short_description = "Upgrade to Elite tier"
    
    def regenerate_qr_codes(self, request, queryset):
        count = 0
        for profile in queryset:
            profile.qr_code_token = profile.generate_qr_token()
            profile.generate_qr_code()
            profile.save()
            count += 1
        self.message_user(request, f'Regenerated QR codes for {count} influencers.')
    regenerate_qr_codes.short_description = "Regenerate QR codes"

@admin.register(VenueProfile)
class VenueProfileAdmin(admin.ModelAdmin):
    """Venue profile management"""
    list_display = (
        'venue_name', 'user', 'cuisine_type', 'total_redemptions', 
        'total_redeemed_amount', 'is_active'
    )
    list_filter = ('cuisine_type', 'is_active', 'created_at')
    search_fields = ('venue_name', 'user__username', 'address')
    readonly_fields = ('total_redemptions', 'total_redeemed_amount', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'venue_name', 'address', 'phone', 'cuisine_type')
        }),
        ('Settings', {
            'fields': ('max_redemption_amount', 'is_active', 'average_bill')
        }),
        ('Analytics', {
            'fields': ('total_redemptions', 'total_redeemed_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Achievement and badge management"""
    list_display = ('influencer', 'badge_type', 'title', 'xp_reward', 'earned_at')
    list_filter = ('badge_type', 'earned_at')
    search_fields = ('influencer__user__username', 'title')
    readonly_fields = ('earned_at',)
    
    fieldsets = (
        ('Achievement Info', {
            'fields': ('influencer', 'badge_type', 'title', 'description', 'xp_reward')
        }),
        ('Timestamp', {
            'fields': ('earned_at',)
        })
    )

@admin.register(Redemption)
class RedemptionAdmin(admin.ModelAdmin):
    """Transaction and redemption management"""
    list_display = (
        'influencer', 'venue', 'amount', 'status', 'created_at', 'confirmed_at'
    )
    list_filter = ('status', 'created_at', 'confirmed_at')
    search_fields = (
        'influencer__user__username', 'venue__venue_name', 
        'qr_token_used'
    )
    readonly_fields = (
        'id', 'qr_token_used', 'balance_before', 'balance_after',
        'created_at', 'confirmed_at'
    )
    
    fieldsets = (
        ('Transaction Info', {
            'fields': ('influencer', 'venue', 'amount', 'status')
        }),
        ('QR Details', {
            'fields': ('qr_token_used', 'balance_before', 'balance_after')
        }),
        ('Additional Info', {
            'fields': ('notes', 'receipt_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'confirmed_at')
        })
    )
    
    actions = ['confirm_redemptions', 'refund_redemptions']
    
    def confirm_redemptions(self, request, queryset):
        count = 0
        for redemption in queryset.filter(status='pending'):
            redemption.status = 'confirmed'
            redemption.save()
            count += 1
        self.message_user(request, f'Confirmed {count} redemptions.')
    confirm_redemptions.short_description = "Confirm selected redemptions"
    
    def refund_redemptions(self, request, queryset):
        count = 0
        for redemption in queryset.filter(status='confirmed'):
            # Refund the amount to influencer
            redemption.influencer.current_balance += redemption.amount
            redemption.influencer.save()
            redemption.status = 'refunded'
            redemption.save()
            count += 1
        self.message_user(request, f'Refunded {count} redemptions.')
    refund_redemptions.short_description = "Refund selected redemptions"

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Activity logging and audit trail"""
    list_display = ('user', 'action_type', 'description', 'ip_address', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action_type', 'description', 'metadata', 'ip_address', 'user_agent', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """Global system settings management"""
    list_display = ('key', 'value', 'description', 'updated_at')
    search_fields = ('key', 'value', 'description')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ('Setting Info', {
            'fields': ('key', 'value', 'description')
        }),
        ('Timestamp', {
            'fields': ('updated_at',)
        })
    )

# Admin site customization
admin.site.site_header = 'hAIpClub Administration'
admin.site.site_title = 'hAIpClub Admin'
admin.site.index_title = 'Welcome to hAIpClub Admin Panel'
