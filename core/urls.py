from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main application views
    path('influencer/signup/', views.InfluencerSignUpView.as_view(), name='influencer_signup'),
    path('venue/signup/', views.VenueSignUpView.as_view(), name='venue_signup'),
    path('influencer/dashboard/', views.InfluencerDashboardView.as_view(), name='influencer_dashboard'),
    path('venue/dashboard/', views.VenueDashboardView.as_view(), name='venue_dashboard'),
    
    # QR Code system
    path('qr/scanner/', views.QRScannerView.as_view(), name='qr_scanner'),
    path('api/scan-qr/', views.scan_qr_code, name='scan_qr_code'),
    path('api/process-redemption/', views.process_redemption, name='process_redemption'),
    path('api/regenerate-qr/', views.regenerate_qr_code, name='regenerate_qr_code'),
    
    # Gamification
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    
    # Legacy URLs for backward compatibility
    path('influencer-waitlist/', views.InfluencerWaitlistView.as_view(), name='influencer_waitlist'),
    path('waitlist-success/', views.WaitlistSuccessView.as_view(), name='waitlist_success'),
    
    # Admin waitlist management URLs
    path('admin/waitlist/', views.AdminWaitlistView.as_view(), name='admin_waitlist'),
    path('admin/waitlist/<int:pk>/', views.AdminWaitlistDetailView.as_view(), name='admin_waitlist_detail'),
    path('admin/waitlist/<int:pk>/approve/', views.approve_waitlist, name='approve_waitlist'),
    path('admin/waitlist/<int:pk>/reject/', views.reject_waitlist, name='reject_waitlist'),
] 