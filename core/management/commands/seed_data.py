from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from users.models import InfluencerProfile, BrandProfile, UserProfile
from core.models import Offer, OfferClaim, ContentSubmission, Notification

class Command(BaseCommand):
    help = 'Populate database with sample data for hAIpClub'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()

        self.stdout.write('Creating sample data...')
        
        # Create sample influencers
        influencers = self.create_influencers()
        self.stdout.write(f'Created {len(influencers)} influencers')
        
        # Create sample brands
        brands = self.create_brands()
        self.stdout.write(f'Created {len(brands)} brands')
        
        # Create sample offers
        offers = self.create_offers(brands)
        self.stdout.write(f'Created {len(offers)} offers')
        
        # Create sample claims and interactions
        self.create_sample_interactions(influencers, offers)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

    def clear_data(self):
        """Clear existing data"""
        ContentSubmission.objects.all().delete()
        OfferClaim.objects.all().delete()
        Offer.objects.all().delete()
        Notification.objects.all().delete()
        InfluencerProfile.objects.all().delete()
        BrandProfile.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    def create_influencers(self):
        """Create sample influencer accounts"""
        influencers_data = [
            {
                'username': 'alice_sf_foodie',
                'first_name': 'Alice',
                'last_name': 'Chen',
                'email': 'alice@example.com',
                'instagram_username': 'alice_in_sf',
                'follower_count': 85000,
                'engagement_rate': 3.2,
                'category': 'food',
                'city': 'san_francisco',
                'bio': 'SF foodie exploring the best restaurants in Silicon Valley 🍽️'
            },
            {
                'username': 'bob_tech_guru',
                'first_name': 'Bob',
                'last_name': 'Martinez',
                'email': 'bob@example.com',
                'instagram_username': 'bob_tech_guru',
                'follower_count': 150000,
                'engagement_rate': 2.8,
                'category': 'tech',
                'city': 'palo_alto',
                'bio': 'Tech enthusiast sharing the latest innovations from Silicon Valley 📱'
            },
            {
                'username': 'sarah_wellness',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah@example.com',
                'instagram_username': 'sarah_wellness_sv',
                'follower_count': 95000,
                'engagement_rate': 4.1,
                'category': 'fitness',
                'city': 'mountain_view',
                'bio': 'Wellness coach promoting healthy living in the Bay Area 🧘‍♀️'
            },
            {
                'username': 'david_lifestyle',
                'first_name': 'David',
                'last_name': 'Kim',
                'email': 'david@example.com',
                'instagram_username': 'david_sv_life',
                'follower_count': 120000,
                'engagement_rate': 3.5,
                'category': 'lifestyle',
                'city': 'san_jose',
                'bio': 'Lifestyle content creator showcasing Silicon Valley culture ✨'
            },
            {
                'username': 'emma_beauty',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'email': 'emma@example.com',
                'instagram_username': 'emma_beauty_bay',
                'follower_count': 75000,
                'engagement_rate': 5.2,
                'category': 'beauty',
                'city': 'menlo_park',
                'bio': 'Beauty influencer sharing the latest trends and tips 💄'
            }
        ]

        influencers = []
        for data in influencers_data:
            # Create user
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password='testpass123'
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='influencer'
            )
            
            # Create influencer profile
            from django.conf import settings
            # Calculate weekly allowance based on follower count
            follower_count = data['follower_count']
            if follower_count >= 500000:
                weekly_allowance = 4000
            elif follower_count >= 100000:
                weekly_allowance = 2500
            elif follower_count >= 50000:
                weekly_allowance = 1500
            elif follower_count >= 10000:
                weekly_allowance = 1000
            else:
                weekly_allowance = 500
            
            influencer = InfluencerProfile.objects.create(
                user=user,
                instagram_username=data['instagram_username'],
                follower_count=data['follower_count'],
                following_count=random.randint(500, 2000),
                post_count=random.randint(100, 500),
                engagement_rate=data['engagement_rate'],
                category=data['category'],
                city=data['city'],
                bio=data['bio'],
                is_approved=True,
                allowance_weekly=weekly_allowance,
                allowance_remaining=weekly_allowance
            )
            influencers.append(influencer)

        return influencers

    def create_brands(self):
        """Create sample brand accounts"""
        brands_data = [
            {
                'username': 'tasty_bites_sf',
                'first_name': 'Michael',
                'last_name': 'Chang',
                'email': 'michael@tastybites.com',
                'business_name': 'Tasty Bites SF',
                'category': 'restaurant',
                'city': 'san_francisco',
                'address': '123 Union Square, San Francisco, CA 94108',
                'description': 'Award-winning restaurant serving modern American cuisine with a focus on local ingredients.',
                'website': 'https://tastybitessf.com',
                'instagram_handle': 'tastybites_sf',
                'phone_number': '(415) 555-0123'
            },
            {
                'username': 'luxe_spa_palo_alto',
                'first_name': 'Jennifer',
                'last_name': 'Smith',
                'email': 'jennifer@luxespa.com',
                'business_name': 'LuxeSpa Palo Alto',
                'category': 'spa',
                'city': 'palo_alto',
                'address': '456 University Ave, Palo Alto, CA 94301',
                'description': 'Premium spa offering relaxation and wellness treatments in the heart of Palo Alto.',
                'website': 'https://luxespa.com',
                'instagram_handle': 'luxe_spa_pa',
                'phone_number': '(650) 555-0456'
            },
            {
                'username': 'fit_zone_mv',
                'first_name': 'Carlos',
                'last_name': 'Rodriguez',
                'email': 'carlos@fitzone.com',
                'business_name': 'FitZone Mountain View',
                'category': 'fitness',
                'city': 'mountain_view',
                'address': '789 Castro St, Mountain View, CA 94041',
                'description': 'State-of-the-art fitness center with personal training and group classes.',
                'website': 'https://fitzonemv.com',
                'instagram_handle': 'fitzone_mv',
                'phone_number': '(650) 555-0789'
            },
            {
                'username': 'tech_boutique_sj',
                'first_name': 'Lisa',
                'last_name': 'Wang',
                'email': 'lisa@techboutique.com',
                'business_name': 'Tech Boutique San Jose',
                'category': 'retail',
                'city': 'san_jose',
                'address': '321 Santana Row, San Jose, CA 95128',
                'description': 'Curated selection of the latest tech gadgets and accessories.',
                'website': 'https://techboutique.com',
                'instagram_handle': 'tech_boutique_sj',
                'phone_number': '(408) 555-0321'
            },
            {
                'username': 'beauty_bar_mp',
                'first_name': 'Amanda',
                'last_name': 'Taylor',
                'email': 'amanda@beautybar.com',
                'business_name': 'Beauty Bar Menlo Park',
                'category': 'beauty',
                'city': 'menlo_park',
                'address': '654 Santa Cruz Ave, Menlo Park, CA 94025',
                'description': 'Full-service beauty salon offering cuts, color, and styling services.',
                'website': 'https://beautybarmp.com',
                'instagram_handle': 'beauty_bar_mp',
                'phone_number': '(650) 555-0654'
            }
        ]

        brands = []
        for data in brands_data:
            # Create user
            user = User.objects.create_user(
                username=data['username'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                password='testpass123'
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role='brand'
            )
            
            # Create brand profile
            brand = BrandProfile.objects.create(
                user=user,
                business_name=data['business_name'],
                category=data['category'],
                address=data['address'],
                city=data['city'],
                description=data['description'],
                website=data['website'],
                instagram_handle=data['instagram_handle'],
                phone_number=data['phone_number'],
                is_verified=True
            )
            brands.append(brand)

        return brands

    def create_offers(self, brands):
        """Create sample offers from brands"""
        offers_data = [
            {
                'brand': 'Tasty Bites SF',
                'title': 'Free Dinner for Two',
                'description': 'Enjoy a complimentary dinner for two at our award-winning restaurant. Experience our signature tasting menu featuring locally sourced ingredients.',
                'reward_value': 250,
                'required_posts': '2 Instagram Stories and 1 Feed Post featuring your dining experience',
                'min_followers': 50000,
                'expires_days': 30
            },
            {
                'brand': 'LuxeSpa Palo Alto',
                'title': 'Luxury Spa Package',
                'description': 'Indulge in our premium spa package including massage, facial, and access to all facilities.',
                'reward_value': 300,
                'required_posts': '3 Instagram Stories showcasing your spa experience',
                'min_followers': 25000,
                'expires_days': 45
            },
            {
                'brand': 'FitZone Mountain View',
                'title': '1-Month Premium Membership',
                'description': 'Complete access to our state-of-the-art facility including personal training sessions and group classes.',
                'reward_value': 200,
                'required_posts': '1 Instagram Reel and 2 Stories about your fitness journey',
                'min_followers': 30000,
                'expires_days': 60
            },
            {
                'brand': 'Tech Boutique San Jose',
                'title': 'Latest Tech Gadget Bundle',
                'description': 'Take home the newest tech accessories worth $180 including wireless earbuds and phone accessories.',
                'reward_value': 180,
                'required_posts': '1 Instagram Post and 1 Story unboxing and reviewing the products',
                'min_followers': 40000,
                'expires_days': 21
            },
            {
                'brand': 'Beauty Bar Menlo Park',
                'title': 'Complete Makeover Experience',
                'description': 'Full hair styling and makeup session with our top stylists. Perfect for special events or photo shoots.',
                'reward_value': 220,
                'required_posts': '2 Instagram Posts showing before/after transformation',
                'min_followers': 35000,
                'expires_days': 30
            },
            {
                'brand': 'Tasty Bites SF',
                'title': 'Weekend Brunch Special',
                'description': 'Complimentary weekend brunch for two including bottomless mimosas and our chef\'s special dishes.',
                'reward_value': 120,
                'required_posts': '1 Instagram Story and 1 Post about your brunch experience',
                'min_followers': 20000,
                'expires_days': 14
            }
        ]

        offers = []
        for data in offers_data:
            # Find the brand
            brand = next(b for b in brands if b.business_name == data['brand'])
            
            offer = Offer.objects.create(
                title=data['title'],
                brand=brand,
                description=data['description'],
                reward_value=data['reward_value'],
                required_posts=data['required_posts'],
                city=brand.city,
                specific_location=brand.address,
                min_followers=data['min_followers'],
                expires_at=timezone.now() + timedelta(days=data['expires_days']),
                status='open'
            )
            offers.append(offer)

        return offers

    def create_sample_interactions(self, influencers, offers):
        """Create sample claims and interactions"""
        # Create some claims with different statuses
        for i, offer in enumerate(offers[:3]):  # First 3 offers
            influencer = influencers[i % len(influencers)]
            
            # Create claim
            claim = OfferClaim.objects.create(
                offer=offer,
                influencer=influencer,
                status='content_submitted' if i == 0 else 'content_approved' if i == 1 else 'completed_redeemed',
                claimed_at=timezone.now() - timedelta(days=random.randint(1, 7))
            )
            
            if claim.status in ['content_submitted', 'content_approved', 'completed_redeemed']:
                claim.content_submitted_at = claim.claimed_at + timedelta(hours=random.randint(2, 48))
                
                # Create content submission
                ContentSubmission.objects.create(
                    offer_claim=claim,
                    content_type='story',
                    caption_text=f"Amazing experience at {offer.brand.business_name}! Highly recommend their {offer.title.lower()}. #sponsored #haipclub",
                    submitted_at=claim.content_submitted_at
                )
            
            if claim.status in ['content_approved', 'completed_redeemed']:
                claim.content_approved_at = claim.content_submitted_at + timedelta(hours=random.randint(1, 24))
                claim.generate_redeem_code()
            
            if claim.status == 'completed_redeemed':
                claim.redeemed_at = claim.content_approved_at + timedelta(days=random.randint(1, 5))
            
            claim.save()
            
            # Create notifications
            if claim.status == 'content_submitted':
                Notification.objects.create(
                    user=offer.brand.user,
                    notification_type='content_submitted',
                    title=f'Content Submitted: {offer.title}',
                    message=f'{influencer.instagram_username} submitted content for review'
                )
            elif claim.status in ['content_approved', 'completed_redeemed']:
                Notification.objects.create(
                    user=influencer.user,
                    notification_type='content_approved',
                    title=f'Content Approved: {offer.title}',
                    message=f'Your content has been approved! Redeem code: {claim.redeem_code}'
                )

        self.stdout.write('Created sample interactions and notifications') 