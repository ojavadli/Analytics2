from django.contrib import admin
from django.utils.html import format_html
from .models import InfluencerProfile, BrandProfile

@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    """Legacy influencer profile admin - use core.InfluencerProfile instead"""
    list_display = ('user', 'instagram_username', 'follower_count', 'engagement_rate', 'is_verified')
    list_filter = ('is_verified', 'content_categories', 'created_at')
    search_fields = ('user__username', 'instagram_username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'instagram_username', 'bio', 'follower_count', 'engagement_rate')
        }),
        ('Settings', {
            'fields': ('content_categories', 'weekly_allowance', 'current_allowance', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    """Legacy brand profile admin - use core.VenueProfile instead"""
    list_display = ('business_name', 'user', 'business_category', 'is_verified')
    list_filter = ('business_category', 'is_verified', 'created_at')
    search_fields = ('business_name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'business_name', 'business_category', 'description')
        }),
        ('Contact', {
            'fields': ('website', 'address', 'phone')
        }),
        ('Settings', {
            'fields': ('is_verified',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
