# hAIpClub - Social Currency Platform

A comprehensive Django-based influencer marketing platform that connects Silicon Valley brands with top-tier influencers, enabling authentic content creation in exchange for premium experiences.

## 🌟 Features

### For Influencers
- **Exclusive Membership**: Curated network with 10k+ follower requirement
- **AI-Powered Vetting**: Automated fake follower detection and engagement analysis
- **Weekly Allowances**: Dynamic credit limits based on follower count ($500-$4000/week)
- **Premium Experiences**: Access to exclusive offers from Silicon Valley's top brands
- **Real-time Instagram Integration**: Automatic profile data fetching via RocketAPI

### For Brands
- **Offer Management**: Create and manage collaboration campaigns
- **AI Content Analysis**: Automated content quality and brand safety checks
- **Influencer Matching**: Smart recommendations based on content categories
- **Performance Tracking**: Monitor campaign success and engagement
- **Secure Redemption System**: Digital codes for in-person reward redemption

### Platform Features
- **Dark Premium UI**: Modern, responsive design with gold accents
- **Real-time Notifications**: Keep users informed of important updates
- **Comprehensive Admin Panel**: Full management capabilities
- **Mobile-Optimized**: Seamless experience across all devices
- **Silicon Valley Focus**: Targeted to Bay Area businesses and creators

## 🛠 Technology Stack

- **Backend**: Django 4.2.7 with Python 3.9+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5 with custom CSS/JavaScript
- **APIs**: RocketAPI (Instagram), OpenAI (Content Analysis)
- **Authentication**: Django Allauth with custom user profiles
- **File Handling**: Django media management with Pillow

## 🚀 Quick Setup

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hAIpClub
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ROCKET_API_KEY=sFoVmRvvwtkOnfleh8xIqw
   OPENAI_API_KEY=your-openai-api-key-here
   ```

4. **Database Setup**
   ```bash
   python manage.py migrate
   ```

5. **Create Sample Data**
   ```bash
   python manage.py seed_data --clear
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000` to access the platform.

## 👥 Sample Accounts

After running the seed command, you can log in with these sample accounts:

### Influencers
- **Username**: `alice_sf_foodie` | **Password**: `testpass123`
  - Food influencer with 85k followers in San Francisco
- **Username**: `bob_tech_guru` | **Password**: `testpass123`
  - Tech influencer with 150k followers in Palo Alto
- **Username**: `sarah_wellness` | **Password**: `testpass123`
  - Wellness influencer with 95k followers in Mountain View

### Brands
- **Username**: `tasty_bites_sf` | **Password**: `testpass123`
  - Restaurant in San Francisco
- **Username**: `luxe_spa_palo_alto` | **Password**: `testpass123`
  - Spa in Palo Alto
- **Username**: `fit_zone_mv` | **Password**: `testpass123`
  - Fitness center in Mountain View

## 🏗 Project Structure

```
hAIpClub/
├── core/                   # Main app with offers, claims, content
│   ├── models.py          # Offer, OfferClaim, ContentSubmission
│   ├── views.py           # Dashboard and workflow views
│   ├── forms.py           # Offer and content forms
│   ├── services.py        # Instagram and OpenAI integrations
│   └── management/        # Custom management commands
├── users/                 # User management app
│   ├── models.py          # User profiles (Influencer, Brand)
│   ├── views.py           # Registration and profile views
│   └── forms.py           # Registration forms
├── templates/             # HTML templates
│   ├── core/             # Core app templates
│   ├── users/            # User app templates
│   └── base.html         # Base template
├── static/               # Static assets
│   ├── css/              # Custom stylesheets
│   ├── js/               # Custom JavaScript
│   └── images/           # Static images
└── media/                # User uploads
```

## 🔧 Configuration

### API Keys

1. **RocketAPI (Instagram Data)**
   - Sign up at [RocketAPI](https://rapidapi.com/Prasadbro/api/instagram-scraper-api2)
   - Add your API key to the `.env` file as `ROCKET_API_KEY`

2. **OpenAI (Content Analysis)**
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)
   - Add your API key to the `.env` file as `OPENAI_API_KEY`

### Silicon Valley Cities
The platform is pre-configured for these Silicon Valley locations:
- San Francisco
- Palo Alto
- San Jose
- Mountain View
- Menlo Park
- Cupertino
- Sunnyvale
- Fremont
- Santa Clara
- Redwood City

### Weekly Allowance Tiers
Influencer allowances are automatically calculated based on follower count:
- 500,000+ followers: $4,000/week
- 100,000+ followers: $2,500/week
- 50,000+ followers: $1,500/week
- 10,000+ followers: $1,000/week
- Under 10,000: $500/week

## 📱 User Workflows

### Influencer Journey
1. **Registration**: Apply with Instagram username and basic info
2. **AI Verification**: System fetches Instagram data and checks authenticity
3. **Approval**: Auto-approved if meeting criteria (10k+ followers)
4. **Browse Offers**: View available brand collaborations
5. **Claim Offers**: Select and claim desired collaborations
6. **Create Content**: Produce required social media content
7. **Submit for Review**: Upload content for brand approval
8. **AI Analysis**: System analyzes content quality and brand safety
9. **Brand Approval**: Brand reviews and approves content
10. **Redemption**: Use generated code to redeem reward in-person

### Brand Journey
1. **Registration**: Sign up with business details
2. **Profile Setup**: Complete business information and verification
3. **Create Offers**: Post collaboration opportunities
4. **Influencer Matching**: Receive applications from qualified creators
5. **Content Review**: Evaluate submitted content with AI assistance
6. **Approval Process**: Approve or request revisions
7. **Redemption Management**: Confirm in-person reward redemptions
8. **Performance Tracking**: Monitor campaign success and engagement

## 🤖 AI Features

### Instagram Analysis
- Automatic follower count and engagement rate calculation
- Fake follower detection using engagement patterns
- Content category classification
- Profile authenticity verification

### Content Quality Assurance
- Sentiment analysis of captions and content
- Brand mention verification
- Content quality scoring (1-10)
- Brand safety compliance checking
- Automated feedback generation

## 🔒 Security Features

- User role-based access control
- Secure API key management
- CSRF protection on all forms
- File upload validation and restrictions
- Unique redemption codes for offers
- Rate limiting on API endpoints

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False` in production
2. Configure PostgreSQL database
3. Set up static file serving (WhiteNoise or CDN)
4. Configure media file storage (AWS S3 recommended)
5. Set up SSL/HTTPS
6. Configure email backend for notifications
7. Set up monitoring and logging
8. Configure backup strategy

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:port/dbname
ROCKET_API_KEY=your-rocket-api-key
OPENAI_API_KEY=your-openai-api-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Check code coverage:
```bash
coverage run manage.py test
coverage report
```

## 📊 Admin Interface

Access the admin panel at `/admin/` to:
- Manage user accounts and profiles
- Approve/reject influencer applications
- Monitor offers and campaigns
- Review content submissions
- Generate platform analytics
- Manage notifications and system messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 🆘 Support

For support and questions:
- Check the documentation in this README
- Review the code comments for implementation details
- Test with the provided sample data
- Use the Django admin interface for debugging

## 🏆 Key Features Showcase

### Exclusive Membership Model
- Minimum 10,000 followers requirement
- AI-powered authenticity verification
- Curated creator network
- Premium brand partnerships

### Social Currency System
- Weekly spending allowances
- Dynamic credit allocation
- Secure redemption process
- Real-time balance tracking

### AI-Powered Platform
- Automated content analysis
- Brand safety verification
- Influencer-brand matching
- Performance optimization

### Silicon Valley Focus
- Targeted geographic scope
- Premium local businesses
- Tech-savvy user base
- High-value collaborations

---

**hAIpClub** - Revolutionizing collaborations with AI & social currency in Silicon Valley's premier influencer ecosystem. 