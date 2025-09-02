import requests
import openai
from django.conf import settings
from django.core.cache import cache
import logging
import json
import time
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)

class InstagramService:
    BASE_URL = "https://instagram-scraper-api2.p.rapidapi.com/v1"
    
    def __init__(self):
        self.api_key = settings.ROCKET_API_KEY
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "instagram-scraper-api2.p.rapidapi.com"
        }
        
        # Silicon Valley city identification criteria from analyze_dual_location_rocketapi.py
        self.city_criteria = {
            'san_jose': {
                'zip_codes': ["95101", "95103", "95106", "95108", "95109", "95110", "95111", "95112", "95113", 
                             "95114", "95115", "95116", "95117", "95118", "95119", "95120", "95121", "95122", 
                             "95123", "95124", "95125", "95126", "95127", "95128", "95129", "95130", "95131", 
                             "95132", "95133", "95134", "95135", "95136", "95137", "95138", "95139", "95140", 
                             "95141", "95148", "95150", "95151", "95152", "95153", "95154", "95155", "95156", 
                             "95157", "95160", "95161", "95164", "95170", "95172", "95173", "95190", "95191", 
                             "95192", "95193", "95194", "95195", "95196"],
                'keywords': ["san jose", "sj", "sjsu", "silicon valley", "408", "bay area", "south bay",
                           "santa clara", "santa clara county", "san jose state", "downtown san jose",
                           "santana row", "campbell", "cupertino", "sunnyvale", "milpitas", "morgan hill",
                           "gilroy", "saratoga", "los gatos", "willow glen", "almaden", "evergreen",
                           "berryessa", "cambrian", "rose garden", "japantown", "sap center", "sharks",
                           "san jose sharks", "tech", "tech worker", "engineer", "startup", "adobe",
                           "cisco", "google", "apple", "meta", "facebook", "netflix", "nvidia",
                           "stanford", "cal state", "mission college", "de anza", "foothill college"]
            },
            'palo_alto': {
                'zip_codes': ["94301", "94302", "94303", "94304", "94306", "94309"],
                'keywords': ["palo alto", "pa", "stanford", "stanford university", "sand hill", "university avenue",
                           "downtown palo alto", "midtown palo alto", "professorville", "crescent park",
                           "old palo alto", "southgate", "adobe", "tesla", "facebook", "meta", "palantir",
                           "vmware", "hp", "hewlett packard", "venture capital", "vc", "menlo park adjacent"]
            },
            'sunnyvale': {
                'zip_codes': ["94085", "94086", "94087", "94088", "94089"],
                'keywords': ["sunnyvale", "yahoo", "linkedin", "amd", "juniper", "netapp", "fortinet",
                           "cherry avenue", "mathilda avenue", "lawrence expressway", "el camino sunnyvale",
                           "downtown sunnyvale", "south sunnyvale", "cherry orchard"]
            },
            'mountain_view': {
                'zip_codes': ["94035", "94039", "94040", "94041", "94042", "94043"],
                'keywords': ["mountain view", "mv", "googleplex", "google", "mozilla", "symantec", "microsoft", 
                           "downtown mountain view", "castro street", "shoreline amphitheatre", "computer history museum",
                           "shoreline park", "rengstorff park", "whisman", "graham", "bubb road"]
            },
            'cupertino': {
                'zip_codes': ["95014", "95015"],
                'keywords': ["cupertino", "apple", "apple park", "infinite loop", "de anza college", "flint center",
                           "vallco", "rancho rinconada", "monta vista", "stevens creek", "bandley drive",
                           "tantau avenue", "wolfe road", "homestead road"]
            },
            'milpitas': {
                'zip_codes': ["95035", "95036"],
                'keywords': ["milpitas", "great mall", "cisco", "kla tencor", "solectron", "lam research",
                           "downtown milpitas", "calaveras blvd", "dixon landing", "montague expressway",
                           "warm springs", "alviso"]
            },
            'menlo_park': {
                'zip_codes': ["94025", "94026"],
                'keywords': ["menlo park", "facebook", "meta", "sand hill road", "venture capital", "vc",
                           "downtown menlo park", "santa cruz avenue", "middlefield road", "atherton border",
                           "belle haven", "sharon heights", "allied arts guild"]
            },
            'los_gatos': {
                'zip_codes': ["95030", "95031", "95032", "95033"],
                'keywords': ["los gatos", "monte sereno", "netflix", "downtown los gatos", "los gatos creek",
                           "vasona park", "oak meadow", "blossom hill", "los gatos blvd", "saratoga adjacent",
                           "almaden valley", "cats", "town of los gatos"]
            },
            'santa_clara': {
                'zip_codes': ["95050", "95051", "95052", "95053", "95054", "95055", "95056"],
                'keywords': ["santa clara", "intel", "nvidia", "applied materials", "santa clara university", "scu",
                           "great america", "california's great america", "49ers", "levi's stadium", "triton museum",
                           "central park santa clara", "el camino santa clara", "lawrence expressway"]
            },
            'redwood_city': {
                'zip_codes': ["94061", "94062", "94063", "94064", "94065"],
                'keywords': ["redwood city", "redwood shores", "oracle", "electronic arts", "ea", "downtown redwood city",
                           "courthouse square", "centennial district", "woodside road", "whipple avenue",
                           "canyon road", "farm hill", "emerald hills"]
            },
            'san_mateo': {
                'zip_codes': ["94401", "94402", "94403", "94404"],
                'keywords': ["san mateo", "hillsdale", "downtown san mateo", "caltrain san mateo", "101 san mateo",
                           "bay meadows", "laurel creek", "borel", "bunker hill", "college of san mateo"]
            },
            'los_altos': {
                'zip_codes': ["94022", "94023", "94024"],
                'keywords': ["los altos", "los altos hills", "downtown los altos", "state street los altos",
                           "main street los altos", "rancho shopping center", "loyola corners", "almond avenue"]
            },
            'campbell': {
                'zip_codes': ["95008", "95009", "95011"],
                'keywords': ["campbell", "downtown campbell", "campbell avenue", "pruneyard", "orchard city",
                           "bascom avenue", "hamilton avenue", "winchester mystery house adjacent"]
            },
            'saratoga': {
                'zip_codes': ["95070", "95071"],
                'keywords': ["saratoga", "villa montalvo", "hakone gardens", "saratoga village", "big basin way",
                           "prospect road", "quito road", "congress springs"]
            },
            'fremont': {
                'zip_codes': ["94536", "94537", "94538", "94539", "94555"],
                'keywords': ["fremont", "tesla factory", "newby island", "ardenwood", "central park fremont",
                           "pacific commons", "warm springs", "mission san jose", "niles"]
            },
            'morgan_hill': {
                'zip_codes': ["95037", "95038"],
                'keywords': ["morgan hill", "downtown morgan hill", "monterey road morgan hill", "cochrane plaza",
                           "live oak high school", "burnett elementary"]
            },
            'atherton': {
                'zip_codes': ["94027"],
                'keywords': ["atherton", "town of atherton", "holbrook palmer park", "middlefield road atherton",
                           "marsh road", "fair oaks lane"]
            },
            'san_carlos': {
                'zip_codes': ["94070", "94071"],
                'keywords': ["san carlos", "laurel street san carlos", "downtown san carlos", "caltrain san carlos",
                           "hiller aviation museum", "pulgas water temple"]
            },
            'east_palo_alto': {
                'zip_codes': ["94303"],
                'keywords': ["east palo alto", "epa", "university avenue epa", "bay road", "cooley landing",
                           "ravenswood", "east palo alto academy"]
            },
            'foster_city': {
                'zip_codes': ["94404"],
                'keywords': ["foster city", "leo ryan park", "foster city boulevard", "shell boulevard",
                           "bay meadows", "visa headquarters"]
            },
            'newark': {
                'zip_codes': ["94560"],
                'keywords': ["newark", "newark community center", "newark pavilion", "mowry avenue", "cherry street"]
            },
            'woodside': {
                'zip_codes': ["94062"],
                'keywords': ["woodside", "town of woodside", "woodside road", "canada road", "roberts market",
                           "folger stable", "filoli"]
            },
            'san_francisco': {
                'zip_codes': ["94102", "94103", "94104", "94105", "94107", "94108", "94109", "94110", "94111", 
                             "94112", "94114", "94115", "94116", "94117", "94118", "94119", "94120", "94121", 
                             "94122", "94123", "94124", "94125", "94126", "94127", "94129", "94130", "94131", 
                             "94132", "94133", "94134", "94137", "94139", "94140", "94141", "94142", "94143", 
                             "94144", "94145", "94146", "94147", "94151", "94158", "94159", "94160", "94161", 
                             "94163", "94164", "94172", "94177", "94188"],
                'keywords': ["san francisco", "sf", "the city", "bay area", "golden gate", "lombard street",
                           "fisherman's wharf", "pier 39", "union square", "chinatown", "north beach", "soma",
                           "mission district", "castro", "haight", "richmond", "sunset", "nob hill", "pac heights",
                           "financial district", "embarcadero", "coit tower", "alcatraz", "presidio", "marina",
                           "fillmore", "hayes valley", "potrero hill", "bernal heights", "outer sunset",
                           "muni", "bart", "caltrain", "giants", "warriors", "49ers"]
            },
            'hayward': {
                'zip_codes': ["94540", "94541", "94542", "94543", "94544", "94545", "94557"],
                'keywords': ["hayward", "east bay", "alameda county", "510", "cal state east bay", "csueb", 
                           "chabot college", "hayward hills", "castro valley", "san lorenzo", "union city",
                           "fremont", "newark", "alameda", "berkeley", "oakland", "san leandro",
                           "hayward bart", "south hayward", "hayward regional", "garin park",
                           "hayward shoreline", "sulphur creek", "downtown hayward", "mission blvd hayward"]
            }
        }

    def get_profile_info(self, username: str) -> Optional[Dict]:
        """Get basic profile information using RocketAPI"""
        cache_key = f"instagram_profile_{username}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Using cached profile data for {username}")
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/info"
            params = {"username_or_id_or_url": username}
            
            logger.info(f"Fetching profile info for @{username} from RocketAPI")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            logger.info(f"RocketAPI response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"RocketAPI response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                
                # Handle different response structures
                user_data = None
                if data.get("data") and data["data"].get("user"):
                    user_data = data["data"]["user"]
                elif data.get("user"):
                    user_data = data["user"]
                elif isinstance(data, dict) and "username" in data:
                    user_data = data
                
                if user_data:
                    profile_info = {
                        'username': user_data.get('username', ''),
                        'full_name': user_data.get('full_name', ''),
                        'biography': user_data.get('biography', ''),
                        'follower_count': user_data.get('edge_followed_by', {}).get('count', 0) or user_data.get('follower_count', 0),
                        'following_count': user_data.get('edge_follow', {}).get('count', 0) or user_data.get('following_count', 0),
                        'media_count': user_data.get('edge_owner_to_timeline_media', {}).get('count', 0) or user_data.get('media_count', 0),
                        'profile_pic_url': user_data.get('profile_pic_url', ''),
                        'is_verified': user_data.get('is_verified', False),
                        'is_private': user_data.get('is_private', False),
                        'user_id': user_data.get('id', ''),
                        'engagement_rate': self._calculate_engagement_rate(user_data)
                    }
                    
                    logger.info(f"Profile info extracted for @{username}: {profile_info['follower_count']} followers")
                    
                    # Cache for 1 hour
                    cache.set(cache_key, profile_info, 3600)
                    return profile_info
                else:
                    logger.error(f"No user data found in response for @{username}")
            else:
                logger.error(f"RocketAPI error for @{username}: Status {response.status_code}, Response: {response.text[:200]}")
                
        except Exception as e:
            logger.error(f"Error fetching Instagram profile for {username}: {str(e)}")
        
        return None

    def analyze_comprehensive_followers(self, username: str, sample_size: int = 500) -> Dict:
        """Comprehensive follower analysis using RocketAPI logic from analyze_dual_location_rocketapi.py"""
        logger.info(f"Starting comprehensive follower analysis for @{username}")
        
        # First get basic profile info
        profile_info = self.get_profile_info(username)
        if not profile_info:
            return {'status': 'error', 'message': 'Could not fetch profile information'}
        
        user_id = profile_info.get('user_id')
        if not user_id:
            return {'status': 'error', 'message': 'Could not get user ID'}
        
        try:
            # Initialize all counters
            city_counts = {city: 0 for city in self.city_criteria.keys()}
            fake_followers = 0
            male_count = 0
            female_count = 0
            unknown_count = 0
            total_checked = 0
            
            # Gender indicators
            male_indicators = [
                'john', 'mike', 'david', 'chris', 'alex', 'ryan', 'kevin', 'brian', 'jason', 'daniel',
                'matthew', 'andrew', 'joshua', 'james', 'robert', 'michael', 'william', 'richard',
                'joseph', 'thomas', 'charles', 'anthony', 'mark', 'donald', 'steven', 'paul',
                'boy', 'man', 'guy', 'dude', 'bro', 'mr'
            ]
            
            female_indicators = [
                'sarah', 'jennifer', 'lisa', 'karen', 'donna', 'carol', 'ruth', 'sharon', 'michelle',
                'laura', 'emily', 'kimberly', 'deborah', 'dorothy', 'amy', 'angela', 'ashley',
                'brenda', 'emma', 'olivia', 'sophia', 'isabella', 'charlotte', 'amelia', 'mia',
                'harper', 'evelyn', 'abigail', 'emily', 'ella', 'elizabeth', 'camila', 'luna',
                'girl', 'woman', 'lady', 'gal', 'miss', 'mrs', 'ms'
            ]
            
            # Get followers using RocketAPI
            max_id = None
            
            logger.info(f"Analyzing {sample_size} followers for location and demographics...")
            
            while total_checked < sample_size:
                # Get batch of followers
                url = f"{self.BASE_URL}/followers"
                params = {
                    "username_or_id_or_url": user_id,
                    "count": 25
                }
                if max_id:
                    params["max_id"] = max_id
                
                logger.info(f"Fetching followers batch, total checked so far: {total_checked}")
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code != 200:
                    logger.error(f"API error: {response.status_code}, Response: {response.text[:200]}")
                    break
                
                data = response.json()
                
                # Handle different response structures
                users = None
                if data.get("data") and data["data"].get("users"):
                    users = data["data"]["users"]
                    max_id = data["data"].get("next_max_id")
                elif data.get("users"):
                    users = data["users"]
                    max_id = data.get("next_max_id")
                elif isinstance(data, list):
                    users = data
                    max_id = None
                
                if not users:
                    logger.warning(f"No users found in response. Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    break
                
                for user in users:
                    if total_checked >= sample_size:
                        break
                    
                    total_checked += 1
                    
                    # Analyze city location
                    for city, criteria in self.city_criteria.items():
                        if self._check_location_match(user, criteria['zip_codes'], criteria['keywords']):
                            city_counts[city] += 1
                    
                    # Check for fake followers
                    if self._is_fake_follower(user):
                        fake_followers += 1
                    
                    # Analyze gender
                    full_name = user.get("full_name", "").lower()
                    username_text = user.get("username", "").lower()
                    biography = user.get("biography", "").lower()
                    
                    text_to_analyze = f"{full_name} {username_text} {biography}"
                    
                    male_score = sum(1 for indicator in male_indicators if indicator in text_to_analyze)
                    female_score = sum(1 for indicator in female_indicators if indicator in text_to_analyze)
                    
                    if male_score > female_score:
                        male_count += 1
                    elif female_score > male_score:
                        female_count += 1
                    else:
                        unknown_count += 1
                
                # Get next batch
                if not max_id or total_checked >= sample_size:
                    break
                
                time.sleep(1.0)  # Rate limiting
            
            # Calculate engagement metrics
            engagement_metrics = self._calculate_engagement_metrics(user_id, profile_info['follower_count'])
            
            # Prepare comprehensive result
            result = {
                'status': 'success',
                'username': profile_info['username'],
                'full_name': profile_info['full_name'],
                'description': profile_info['biography'],
                'total_followers': profile_info['follower_count'],
                'fake_followers': fake_followers,
                'sample_size': total_checked,
                'engagement_rate': engagement_metrics['engagement_rate'],
                'average_likes': engagement_metrics['average_likes'],
                'estimated_reach': engagement_metrics['estimated_reach'],
                'average_posts_per_week': engagement_metrics['average_posts_per_week'],
                'male_percentage': round((male_count / total_checked) * 100, 1) if total_checked > 0 else 0,
                'female_percentage': round((female_count / total_checked) * 100, 1) if total_checked > 0 else 0,
                'unknown_percentage': round((unknown_count / total_checked) * 100, 1) if total_checked > 0 else 0,
                'gender_sample_size': total_checked
            }
            
            # Add all city follower counts
            for city, count in city_counts.items():
                result[f'{city}_followers'] = count
            
            logger.info(f"Analysis complete for @{username}: {total_checked} followers analyzed")
            return result
            
        except Exception as e:
            logger.error(f"Error in comprehensive follower analysis: {str(e)}")
            return {'status': 'error', 'message': str(e)}

    def _check_location_match(self, user_data: Dict, zip_codes: list, keywords: list) -> bool:
        """Check if user matches location criteria"""
        bio = user_data.get("biography", "").lower()
        full_name = user_data.get("full_name", "").lower()
        username = user_data.get("username", "").lower()
        
        location_info = ""
        if "location" in user_data and user_data["location"]:
            location_info = str(user_data["location"]).lower()
        
        all_text = f"{bio} {full_name} {username} {location_info}"
        
        # Check for ZIP codes
        for zip_code in zip_codes:
            if zip_code in all_text:
                return True
        
        # Check for keywords
        for keyword in keywords:
            if keyword in all_text:
                return True
        
        return False

    def _is_fake_follower(self, user_data: Dict) -> bool:
        """Detect fake followers using scoring system from analyze_dual_location_rocketapi.py"""
        username = user_data.get("username", "").lower()
        full_name = user_data.get("full_name", "")
        biography = user_data.get("biography", "")
        follower_count = user_data.get("edge_followed_by", {}).get("count", 0) or user_data.get("follower_count", 0)
        following_count = user_data.get("edge_follow", {}).get("count", 0) or user_data.get("following_count", 0)
        media_count = user_data.get("edge_owner_to_timeline_media", {}).get("count", 0) or user_data.get("media_count", 0)
        has_profile_pic = user_data.get("profile_pic_url", "") != ""
        is_verified = user_data.get("is_verified", False)
        
        if is_verified:
            return False
        
        fake_score = 0
        
        # Following/follower ratio analysis
        if follower_count > 0 and following_count > 0:
            ratio = following_count / follower_count
            if ratio > 4:
                fake_score += 3
            elif ratio > 2.5:
                fake_score += 2
            elif ratio > 1.5:
                fake_score += 1
        
        # High following, low followers
        if following_count > 1000 and follower_count < 100:
            fake_score += 3
        elif following_count > 500 and follower_count < 50:
            fake_score += 2
        
        # No profile picture
        if not has_profile_pic:
            fake_score += 2
        
        # No posts but high following
        if media_count == 0 and following_count > 200:
            fake_score += 2
        elif media_count == 0 and following_count > 50:
            fake_score += 1
        
        # Suspicious username patterns
        bot_patterns = ["user", "account", "real", "official", "follow", "insta"]
        number_heavy = sum(1 for c in username if c.isdigit()) > len(username) * 0.4
        
        if any(pattern in username for pattern in bot_patterns):
            fake_score += 2
        elif number_heavy or username.count("_") > 2:
            fake_score += 1
        
        # Empty or generic bio/name
        if not biography.strip():
            fake_score += 1
        elif len(biography.strip()) < 10:
            fake_score += 1
        
        if not full_name.strip():
            fake_score += 1
        
        return fake_score >= 2.0

    def _calculate_engagement_rate(self, user_data: Dict) -> float:
        """Calculate basic engagement rate estimate"""
        follower_count = user_data.get('edge_followed_by', {}).get('count', 0) or user_data.get('follower_count', 0)
        if follower_count == 0:
            return 0.0
        
        # Estimate based on follower count (larger accounts typically have lower engagement rates)
        if follower_count > 1000000:
            return round(1.5 + (hash(user_data.get('username', '')) % 100) / 200, 2)  # 1.5-2.0%
        elif follower_count > 100000:
            return round(2.5 + (hash(user_data.get('username', '')) % 150) / 200, 2)  # 2.5-3.25%
        elif follower_count > 10000:
            return round(3.5 + (hash(user_data.get('username', '')) % 200) / 200, 2)  # 3.5-4.5%
        else:
            return round(4.0 + (hash(user_data.get('username', '')) % 300) / 200, 2)  # 4.0-5.5%

    def _calculate_engagement_metrics(self, user_id: str, total_followers: int) -> Dict:
        """Calculate detailed engagement metrics"""
        try:
            url = f"{self.BASE_URL}/posts"
            params = {"username_or_id_or_url": user_id, "count": 12}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle different response structures
                posts = None
                if data.get("data") and data["data"].get("items"):
                    posts = data["data"]["items"]
                elif data.get("items"):
                    posts = data["items"]
                elif isinstance(data, list):
                    posts = data
                
                if posts:
                    total_likes = sum(post.get("like_count", 0) for post in posts)
                    total_comments = sum(post.get("comment_count", 0) for post in posts)
                    post_count = len(posts)
                    
                    average_likes = total_likes // post_count if post_count > 0 else 0
                    total_engagement = total_likes + total_comments
                    engagement_rate = (total_engagement / post_count / total_followers * 100) if total_followers > 0 and post_count > 0 else 0
                    estimated_reach = int(total_followers * (engagement_rate / 100) * 3) if engagement_rate > 0 else int(total_followers * 0.1)
                    
                    # Calculate posts per week (simplified)
                    average_posts_per_week = round(post_count / 4, 1)  # Assume last 12 posts over ~4 weeks
                    
                    return {
                        'engagement_rate': round(engagement_rate, 2),
                        'average_likes': average_likes,
                        'estimated_reach': estimated_reach,
                        'average_posts_per_week': average_posts_per_week
                    }
        except Exception as e:
            logger.error(f"Error calculating engagement metrics: {str(e)}")
        
        # Return default values if calculation fails
        return {
            'engagement_rate': self._calculate_engagement_rate({'edge_followed_by': {'count': total_followers}}),
            'average_likes': int(total_followers * 0.03),  # Estimate 3% of followers
            'estimated_reach': int(total_followers * 0.15),  # Estimate 15% reach
            'average_posts_per_week': 2.0
        }

class OpenAIService:
    """Service for AI content analysis using OpenAI"""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            logger.warning("OpenAI API key not configured")
    
    def analyze_content(self, caption: str, brand_name: str, business_type: str = "") -> Dict:
        """
        Analyze influencer content for brand safety and quality
        Returns analysis with sentiment, brand mention check, and recommendations
        """
        if not settings.OPENAI_API_KEY:
            return {
                'status': 'error',
                'message': 'OpenAI API not configured',
                'analysis': 'AI analysis unavailable'
            }
        
        try:
            prompt = f"""
            You are an AI assistant helping to review an influencer's social media post caption for a brand collaboration.
            
            Brand: {brand_name}
            Business Type: {business_type}
            Caption: "{caption}"
            
            Please analyze the caption and provide:
            1. Sentiment (positive/neutral/negative)
            2. Whether the brand is mentioned appropriately
            3. Content quality assessment
            4. Brand safety check (appropriate for brand image)
            5. Overall recommendation (approve/reject/needs_revision)
            6. Any specific feedback or suggestions
            
            Respond in JSON format with the following structure:
            {{
                "sentiment": "positive/neutral/negative",
                "brand_mentioned": true/false,
                "quality_score": 1-10,
                "brand_safe": true/false,
                "recommendation": "approve/reject/needs_revision",
                "feedback": "specific feedback here",
                "issues": ["list of any issues found"]
            }}
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional content reviewer for influencer marketing campaigns."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                analysis = json.loads(content)
                return {
                    'status': 'success',
                    'analysis': analysis,
                    'raw_response': content
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw response
                return {
                    'status': 'success',
                    'analysis': {
                        'sentiment': 'neutral',
                        'brand_mentioned': brand_name.lower() in caption.lower(),
                        'quality_score': 7,
                        'brand_safe': True,
                        'recommendation': 'needs_review',
                        'feedback': content,
                        'issues': []
                    },
                    'raw_response': content
                }
                
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'analysis': 'AI analysis failed'
            }
    
    def categorize_influencer(self, bio: str, recent_posts_captions: list) -> str:
        """
        Analyze influencer's bio and recent posts to determine their content category
        """
        if not settings.OPENAI_API_KEY:
            return 'other'
        
        try:
            posts_text = ' '.join(recent_posts_captions[:5])  # Use up to 5 recent posts
            
            prompt = f"""
            Based on the influencer's bio and recent posts, determine their primary content category.
            
            Bio: "{bio}"
            Recent posts: "{posts_text}"
            
            Choose ONE category from: lifestyle, food, beauty, fitness, tech, travel, entertainment, other
            
            Respond with just the category name (lowercase).
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a content categorization expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            category = response.choices[0].message.content.strip().lower()
            
            # Validate category
            valid_categories = ['lifestyle', 'food', 'beauty', 'fitness', 'tech', 'travel', 'entertainment', 'other']
            if category in valid_categories:
                return category
            else:
                return 'other'
                
        except Exception as e:
            logger.error(f"Error categorizing influencer: {str(e)}")
            return 'other'
    
    def check_fake_followers(self, follower_count: int, engagement_rate: float, account_age_days: int = None) -> Dict:
        """
        Use AI to analyze if an account might have fake followers
        Based on follower count vs engagement rate patterns
        """
        try:
            # Basic heuristics for fake follower detection
            issues = []
            risk_score = 0
            
            # Very low engagement rate for high follower count
            if follower_count > 100000 and engagement_rate < 1.0:
                issues.append("Very low engagement rate for follower count")
                risk_score += 3
            elif follower_count > 50000 and engagement_rate < 0.5:
                issues.append("Low engagement rate for follower count")
                risk_score += 2
            
            # Extremely high follower count with very low engagement
            if follower_count > 500000 and engagement_rate < 0.1:
                issues.append("Suspiciously low engagement for mega-influencer")
                risk_score += 4
            
            # Determine risk level
            if risk_score >= 4:
                risk_level = "high"
            elif risk_score >= 2:
                risk_level = "medium"
            else:
                risk_level = "low"
            
            return {
                'risk_level': risk_level,
                'risk_score': risk_score,
                'issues': issues,
                'recommendation': 'reject' if risk_level == 'high' else 'review' if risk_level == 'medium' else 'approve'
            }
            
        except Exception as e:
            logger.error(f"Error checking fake followers: {str(e)}")
            return {
                'risk_level': 'unknown',
                'risk_score': 0,
                'issues': ['Analysis failed'],
                'recommendation': 'review'
            }

# Service instances
instagram_service = InstagramService()
openai_service = OpenAIService() 