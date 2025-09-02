from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.db import transaction
from django.conf import settings
import json
import secrets
from decimal import Decimal

from .models import (
    User, InfluencerProfile, VenueProfile, Achievement, 
    Redemption, ActivityLog, SystemSettings
)

class HomeView(TemplateView):
    """Beautiful homepage with OTH Network styling"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_influencers': InfluencerProfile.objects.count(),
            'total_venues': VenueProfile.objects.count(),
            'total_redemptions': Redemption.objects.filter(status='confirmed').count(),
            'elite_members': InfluencerProfile.objects.filter(tier='elite').count(),
        })
        return context

class InfluencerSignUpView(CreateView):
    """Mobile-first influencer sign-up with instant QR code generation"""
    model = User
    template_name = 'core/influencer_signup.html'
    fields = ['username', 'email', 'password', 'first_name', 'last_name']
    success_url = reverse_lazy('core:influencer_dashboard')
    
    def form_valid(self, form):
        # Create user with influencer role
        user = form.save(commit=False)
        user.role = 'influencer'
        user.set_password(form.cleaned_data['password'])
        user.save()
        
        # Create influencer profile with Instagram username
        instagram_username = self.request.POST.get('instagram_username', '')
        if instagram_username:
            profile = InfluencerProfile.objects.create(
                user=user,
                instagram_username=instagram_username
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action_type='signup',
                description=f'New influencer signed up: @{instagram_username}',
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
        
        # Auto-login the user
        login(self.request, user)
        messages.success(self.request, 'Welcome to hAIpClub Elite SF! Your QR code is ready.')
        
        return redirect('core:influencer_dashboard')
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class VenueSignUpView(CreateView):
    """Venue registration for partner restaurants"""
    model = User
    template_name = 'core/venue_signup.html'
    fields = ['username', 'email', 'password']
    success_url = reverse_lazy('core:venue_dashboard')
    
    def form_valid(self, form):
        # Create user with venue role
        user = form.save(commit=False)
        user.role = 'venue'
        user.set_password(form.cleaned_data['password'])
        user.save()
        
        # Create venue profile
        venue_name = self.request.POST.get('venue_name', '')
        address = self.request.POST.get('address', '')
        phone = self.request.POST.get('phone', '')
        
        if venue_name:
            VenueProfile.objects.create(
                user=user,
                venue_name=venue_name,
                address=address,
                phone=phone
            )
        
        # Auto-login the user
        login(self.request, user)
        messages.success(self.request, 'Welcome to hAIpClub Partner Network!')
        
        return redirect('core:venue_dashboard')

class InfluencerDashboardView(LoginRequiredMixin, TemplateView):
    """Mobile-first influencer dashboard with QR code and gamification"""
    template_name = 'core/influencer_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'influencer_profile'):
            messages.error(request, 'Influencer profile not found.')
            return redirect('core:influencer_signup')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.influencer_profile
        
        # Recent redemptions
        recent_redemptions = profile.redemptions.filter(
            status='confirmed'
        ).order_by('-created_at')[:5]
        
        # Recent achievements
        recent_achievements = profile.achievements.order_by('-earned_at')[:5]
        
        # Progress to next tier
        tier_thresholds = settings.HAIPCLUB_SETTINGS['TIER_THRESHOLDS']
        current_xp = profile.xp_points
        
        if profile.tier == 'elite':
            next_tier_xp = None
            progress_percentage = 100
        else:
            tier_order = ['bronze', 'silver', 'gold', 'elite']
            current_index = tier_order.index(profile.tier)
            next_tier = tier_order[current_index + 1]
            next_tier_xp = tier_thresholds[next_tier.upper()]
            progress_percentage = (current_xp / next_tier_xp) * 100 if next_tier_xp > 0 else 0
        
        context.update({
            'profile': profile,
            'recent_redemptions': recent_redemptions,
            'recent_achievements': recent_achievements,
            'next_tier_xp': next_tier_xp,
            'progress_percentage': min(progress_percentage, 100),
            'tier_color': profile.get_tier_color(),
        })
        return context

class VenueDashboardView(LoginRequiredMixin, TemplateView):
    """Venue dashboard for QR scanning and redemption management"""
    template_name = 'core/venue_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'venue_profile'):
            messages.error(request, 'Venue profile not found.')
            return redirect('core:venue_signup')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venue = self.request.user.venue_profile
        
        # Recent redemptions
        recent_redemptions = venue.redemptions.filter(
            status='confirmed'
        ).order_by('-created_at')[:10]
        
        # Today's stats
        today = timezone.now().date()
        today_redemptions = venue.redemptions.filter(
            created_at__date=today,
            status='confirmed'
        )
        
        context.update({
            'venue': venue,
            'recent_redemptions': recent_redemptions,
            'today_redemptions_count': today_redemptions.count(),
            'today_total_amount': sum(r.amount for r in today_redemptions),
        })
        return context

class QRScannerView(LoginRequiredMixin, TemplateView):
    """QR code scanner interface for venues"""
    template_name = 'core/qr_scanner.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'venue':
            return HttpResponseForbidden("Only venues can access QR scanner")
        return super().dispatch(request, *args, **kwargs)

def scan_qr_code(request):
    """API endpoint for processing QR code scans"""
    if request.method != 'POST' or request.user.role != 'venue':
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    try:
        data = json.loads(request.body)
        qr_token = data.get('qr_token', '')
        
        # Find influencer by QR token
        try:
            profile = InfluencerProfile.objects.get(
                qr_code_token=qr_token,
                qr_code_active=True
            )
        except InfluencerProfile.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Invalid or expired QR code'
            })
        
        # Return influencer info for venue to review
        return JsonResponse({
            'success': True,
            'influencer': {
                'id': str(profile.user.id),
                'username': profile.user.username,
                'instagram_username': profile.instagram_username,
                'tier': profile.get_tier_display(),
                'tier_color': profile.get_tier_color(),
                'current_balance': float(profile.current_balance),
                'total_redemptions': profile.total_redemptions,
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'QR code processing failed'
        })

def process_redemption(request):
    """API endpoint for processing venue redemptions"""
    if request.method != 'POST' or request.user.role != 'venue':
        return JsonResponse({'success': False, 'error': 'Invalid request'})
    
    try:
        data = json.loads(request.body)
        influencer_id = data.get('influencer_id', '')
        amount = Decimal(str(data.get('amount', 0)))
        qr_token = data.get('qr_token', '')
        
        if amount <= 0:
            return JsonResponse({
                'success': False,
                'error': 'Invalid amount'
            })
        
        # Get influencer and venue profiles
        try:
            influencer = InfluencerProfile.objects.get(
                user__id=influencer_id,
                qr_code_token=qr_token,
                qr_code_active=True
            )
            venue = request.user.venue_profile
        except (InfluencerProfile.DoesNotExist, AttributeError):
            return JsonResponse({
                'success': False,
                'error': 'Invalid influencer or venue'
            })
        
        # Check if amount exceeds balance
        if amount > influencer.current_balance:
            return JsonResponse({
                'success': False,
                'error': f'Insufficient balance. Available: ${influencer.current_balance}'
            })
        
        # Check venue max redemption limit
        if amount > venue.max_redemption_amount:
            return JsonResponse({
                'success': False,
                'error': f'Amount exceeds venue limit of ${venue.max_redemption_amount}'
            })
        
        # Process the redemption
        with transaction.atomic():
            balance_before = influencer.current_balance
            
            # Deduct from influencer balance
            if not influencer.deduct_balance(amount):
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to deduct balance'
                })
            
            # Create redemption record
            redemption = Redemption.objects.create(
                influencer=influencer,
                venue=venue,
                amount=amount,
                status='confirmed',
                qr_token_used=qr_token,
                balance_before=balance_before,
                balance_after=influencer.current_balance,
                notes=data.get('notes', '')
            )
            
            # Log activity
            ActivityLog.objects.create(
                user=influencer.user,
                action_type='redemption',
                description=f'Redeemed ${amount} at {venue.venue_name}',
                metadata={
                    'venue_name': venue.venue_name,
                    'amount': float(amount),
                    'redemption_id': str(redemption.id)
                },
                ip_address=get_client_ip(request)
            )
        
        return JsonResponse({
            'success': True,
            'message': f'${amount} redeemed successfully!',
            'redemption_id': str(redemption.id),
            'new_balance': float(influencer.current_balance)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'Redemption processing failed'
        })

class AchievementsView(LoginRequiredMixin, ListView):
    """View all achievements and badges"""
    model = Achievement
    template_name = 'core/achievements.html'
    context_object_name = 'achievements'
    
    def get_queryset(self):
        if hasattr(self.request.user, 'influencer_profile'):
            return self.request.user.influencer_profile.achievements.order_by('-earned_at')
        return Achievement.objects.none()

class LeaderboardView(TemplateView):
    """Gamification leaderboard"""
    template_name = 'core/leaderboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Top influencers by XP
        top_xp = InfluencerProfile.objects.filter(
            user__is_active=True
        ).order_by('-xp_points')[:10]
        
        # Top spenders this month
        current_month = timezone.now().replace(day=1)
        top_spenders = InfluencerProfile.objects.filter(
            user__is_active=True,
            redemptions__created_at__gte=current_month,
            redemptions__status='confirmed'
        ).order_by('-total_spent')[:10]
        
        # Elite members
        elite_members = InfluencerProfile.objects.filter(
            tier='elite',
            user__is_active=True
        ).order_by('-xp_points')[:20]
        
        context.update({
            'top_xp': top_xp,
            'top_spenders': top_spenders,
            'elite_members': elite_members,
        })
        return context

def regenerate_qr_code(request):
    """API endpoint to regenerate user's QR code"""
    if not request.user.is_authenticated or request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    if not hasattr(request.user, 'influencer_profile'):
        return JsonResponse({'success': False, 'error': 'No influencer profile'})
    
    try:
        profile = request.user.influencer_profile
        
        # Generate new QR token and image
        profile.qr_code_token = profile.generate_qr_token()
        profile.generate_qr_code()
        profile.save()
        
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action_type='qr_scan',
            description='QR code regenerated',
            ip_address=get_client_ip(request)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'QR code regenerated successfully',
            'qr_code_url': profile.qr_code_image.url if profile.qr_code_image else None
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Failed to regenerate QR code'})

# Utility functions
def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Legacy views for backward compatibility (simplified)
class InfluencerWaitlistView(TemplateView):
    """Legacy waitlist view - redirects to new signup"""
    template_name = 'core/influencer_waitlist.html'
    
    def get(self, request):
        # For now, show the waitlist form instead of redirecting
        return super().get(request)
    
    def post(self, request):
        # Handle waitlist form submission
        # For now, just redirect to success page
        return redirect('core:waitlist_success')

class WaitlistSuccessView(TemplateView):
    """Legacy success view"""
    template_name = 'core/waitlist_success.html'

# Admin waitlist management views
class AdminWaitlistView(LoginRequiredMixin, TemplateView):
    """Admin view for managing waitlist applications"""
    template_name = 'core/admin_waitlist.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access denied. Admin privileges required.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Mock data for now - in a real implementation, this would query actual waitlist applications
        context.update({
            'applications': [],
            'stats': {
                'total': 0,
                'pending': 0,
                'approved': 0,
                'rejected': 0,
                'analyzing': 0,
                'analysis_failed': 0,
            },
            'status_choices': [
                ('pending', 'Pending Review'),
                ('approved', 'Approved'),
                ('rejected', 'Rejected'),
                ('analyzing', 'Analyzing'),
                ('analysis_failed', 'Analysis Failed'),
            ],
            'current_status': self.request.GET.get('status', ''),
            'current_search': self.request.GET.get('search', ''),
        })
        return context

class AdminWaitlistDetailView(LoginRequiredMixin, TemplateView):
    """Admin view for detailed waitlist application"""
    template_name = 'core/admin_waitlist_detail.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access denied. Admin privileges required.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs.get('pk')
        
        # Mock application data - in real implementation, would fetch from database
        context['application'] = {
            'id': pk,
            'instagram_username': 'example_user',
            'full_name': 'Example User',
            'email': 'user@example.com',
            'status': 'pending',
            'description': 'Sample bio description',
            'admin_notes': None,
            'reviewed_at': None,
        }
        return context

@login_required
def approve_waitlist(request, pk):
    """Approve a waitlist application"""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        # In real implementation, would update the application status
        messages.success(request, f'Application #{pk} has been approved.')
        return redirect('core:admin_waitlist')
    
    return redirect('core:admin_waitlist_detail', pk=pk)

@login_required 
def reject_waitlist(request, pk):
    """Reject a waitlist application"""
    if not request.user.is_superuser:
        return HttpResponseForbidden("Access denied.")
    
    if request.method == 'POST':
        admin_notes = request.POST.get('admin_notes', '')
        # In real implementation, would update the application status
        messages.success(request, f'Application #{pk} has been rejected.')
        return redirect('core:admin_waitlist')
    
    return redirect('core:admin_waitlist_detail', pk=pk)
