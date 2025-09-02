from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.conf import settings

from .models import InfluencerProfile, BrandProfile

class InfluencerRegisterView(CreateView):
    """Legacy influencer registration - redirects to new signup"""
    def get(self, request):
        return redirect('core:influencer_signup')

class BrandRegisterView(CreateView):
    """Legacy brand registration - redirects to new venue signup"""
    def get(self, request):
        return redirect('core:venue_signup')
