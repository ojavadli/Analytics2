from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Legacy URLs - redirect to new signup flows
    path('influencer/register/', views.InfluencerRegisterView.as_view(), name='influencer_register'),
    path('brand/register/', views.BrandRegisterView.as_view(), name='brand_register'),
] 