#!/usr/bin/env python3
"""
Dual Location Analysis: San Jose + Hayward followers for influencers from influencer_list.txt
Using the proven rocketapi library approach
"""

import time
import csv
from datetime import datetime
from rocketapi import InstagramAPI, exceptions

# Configuration
API_TOKEN = "sFoVmRvvwtkOnfleh8xIqw"
SAMPLE_SIZE = 300

# San Jose identification criteria
SAN_JOSE_ZIP_CODES = [
    # User specified zip codes for San Jose
    "95101", "95103", "95106", "95108", "95109", "95110", "95111", "95112", "95113", 
    "95114", "95115", "95116", "95117", "95118", "95119", "95120", "95121", "95122", 
    "95123", "95124", "95125", "95126", "95127", "95128", "95129", "95130", "95131", 
    "95132", "95133", "95134", "95135", "95136", "95137", "95138", "95139", "95140", 
    "95141", "95148", "95150", "95151", "95152", "95153", "95154", "95155", "95156", 
    "95157", "95160", "95161", "95164", "95170", "95172", "95173", "95190", "95191", 
    "95192", "95193", "95194", "95195", "95196"
]

SAN_JOSE_LOCATION_IDS = [
    "213063126", "213987654", "213123456", "213070948", "212999109"
]

SAN_JOSE_KEYWORDS = [
    "san jose", "sj", "sjsu", "silicon valley", "408", "bay area", "south bay",
    "santa clara", "santa clara county", "san jose state", "downtown san jose",
    "santana row", "campbell", "cupertino", "sunnyvale", "milpitas", "morgan hill",
    "gilroy", "saratoga", "los gatos", "willow glen", "almaden", "evergreen",
    "berryessa", "cambrian", "rose garden", "japantown", "sap center", "sharks",
    "san jose sharks", "tech", "tech worker", "engineer", "startup", "adobe",
    "cisco", "google", "apple", "meta", "facebook", "netflix", "nvidia",
    "stanford", "cal state", "mission college", "de anza", "foothill college"
]

# Palo Alto identification criteria
PALO_ALTO_ZIP_CODES = [
    "94301", "94302", "94303", "94304", "94306", "94309"
]

PALO_ALTO_LOCATION_IDS = [
    "213070949", "213987655", "214123457"  # Placeholder IDs - to be updated with actual
]

PALO_ALTO_KEYWORDS = [
    "palo alto", "pa", "stanford", "stanford university", "sand hill", "university avenue",
    "downtown palo alto", "midtown palo alto", "professorville", "crescent park",
    "old palo alto", "southgate", "adobe", "tesla", "facebook", "meta", "palantir",
    "vmware", "hp", "hewlett packard", "venture capital", "vc", "menlo park adjacent"
]

# Sunnyvale identification criteria  
SUNNYVALE_ZIP_CODES = [
    "94085", "94086", "94087", "94088", "94089"
]

SUNNYVALE_LOCATION_IDS = [
    "213070950", "213987656", "214123458"  # Placeholder IDs - to be updated with actual
]

SUNNYVALE_KEYWORDS = [
    "sunnyvale", "yahoo", "linkedin", "amd", "juniper", "netapp", "fortinet",
    "cherry avenue", "mathilda avenue", "lawrence expressway", "el camino sunnyvale",
    "downtown sunnyvale", "south sunnyvale", "cherry orchard"
]

# Mountain View identification criteria
MOUNTAIN_VIEW_ZIP_CODES = [
    "94035", "94039", "94040", "94041", "94042", "94043"
]

MOUNTAIN_VIEW_LOCATION_IDS = [
    "213070951", "213987657", "214123459"  # Placeholder IDs - to be updated with actual
]

MOUNTAIN_VIEW_KEYWORDS = [
    "mountain view", "mv", "googleplex", "google", "mozilla", "symantec", "microsoft", 
    "downtown mountain view", "castro street", "shoreline amphitheatre", "computer history museum",
    "shoreline park", "rengstorff park", "whisman", "graham", "bubb road"
]

# Cupertino identification criteria
CUPERTINO_ZIP_CODES = [
    "95014", "95015"
]

CUPERTINO_LOCATION_IDS = [
    "213070952", "213987658", "214123460"  # Placeholder IDs - to be updated with actual
]

CUPERTINO_KEYWORDS = [
    "cupertino", "apple", "apple park", "infinite loop", "de anza college", "flint center",
    "vallco", "rancho rinconada", "monta vista", "stevens creek", "bandley drive",
    "tantau avenue", "wolfe road", "homestead road"
]

# Milpitas identification criteria
MILPITAS_ZIP_CODES = [
    "95035", "95036"
]

MILPITAS_LOCATION_IDS = [
    "213070953", "213987659", "214123461"  # Placeholder IDs - to be updated with actual
]

MILPITAS_KEYWORDS = [
    "milpitas", "great mall", "cisco", "kla tencor", "solectron", "lam research",
    "downtown milpitas", "calaveras blvd", "dixon landing", "montague expressway",
    "warm springs", "alviso"
]

# Menlo Park identification criteria
MENLO_PARK_ZIP_CODES = [
    "94025", "94026"
]

MENLO_PARK_LOCATION_IDS = [
    "213070954", "213987660", "214123462"  # Placeholder IDs - to be updated with actual
]

MENLO_PARK_KEYWORDS = [
    "menlo park", "facebook", "meta", "sand hill road", "venture capital", "vc",
    "downtown menlo park", "santa cruz avenue", "middlefield road", "atherton border",
    "belle haven", "sharon heights", "allied arts guild"
]

# Los Gatos identification criteria
LOS_GATOS_ZIP_CODES = [
    "95030", "95031", "95032", "95033"
]

LOS_GATOS_LOCATION_IDS = [
    "213070955", "213987661", "214123463"  # Placeholder IDs - to be updated with actual
]

LOS_GATOS_KEYWORDS = [
    "los gatos", "monte sereno", "netflix", "downtown los gatos", "los gatos creek",
    "vasona park", "oak meadow", "blossom hill", "los gatos blvd", "saratoga adjacent",
    "almaden valley", "cats", "town of los gatos"
]

# Santa Clara identification criteria
SANTA_CLARA_ZIP_CODES = [
    "95050", "95051", "95052", "95053", "95054", "95055", "95056"
]

SANTA_CLARA_LOCATION_IDS = [
    "213070956", "213987662", "214123464"  # Placeholder IDs - to be updated with actual
]

SANTA_CLARA_KEYWORDS = [
    "santa clara", "intel", "nvidia", "applied materials", "santa clara university", "scu",
    "great america", "california's great america", "49ers", "levi's stadium", "triton museum",
    "central park santa clara", "el camino santa clara", "lawrence expressway"
]

# Redwood City identification criteria
REDWOOD_CITY_ZIP_CODES = [
    "94061", "94062", "94063", "94064", "94065"
]

REDWOOD_CITY_LOCATION_IDS = [
    "213070957", "213987663", "214123465"  # Placeholder IDs - to be updated with actual
]

REDWOOD_CITY_KEYWORDS = [
    "redwood city", "redwood shores", "oracle", "electronic arts", "ea", "downtown redwood city",
    "courthouse square", "centennial district", "woodside road", "whipple avenue",
    "canyon road", "farm hill", "emerald hills"
]

# San Mateo identification criteria
SAN_MATEO_ZIP_CODES = [
    "94401", "94402", "94403", "94404"
]

SAN_MATEO_LOCATION_IDS = [
    "213070958", "213987664", "214123466"  # Placeholder IDs - to be updated with actual
]

SAN_MATEO_KEYWORDS = [
    "san mateo", "hillsdale", "downtown san mateo", "caltrain san mateo", "101 san mateo",
    "bay meadows", "laurel creek", "borel", "bunker hill", "college of san mateo"
]

# Los Altos identification criteria
LOS_ALTOS_ZIP_CODES = [
    "94022", "94023", "94024"
]

LOS_ALTOS_LOCATION_IDS = [
    "213070959", "213987665", "214123467"  # Placeholder IDs - to be updated with actual
]

LOS_ALTOS_KEYWORDS = [
    "los altos", "los altos hills", "downtown los altos", "state street los altos",
    "main street los altos", "rancho shopping center", "loyola corners", "almond avenue"
]

# Campbell identification criteria
CAMPBELL_ZIP_CODES = [
    "95008", "95009", "95011"
]

CAMPBELL_LOCATION_IDS = [
    "213070960", "213987666", "214123468"  # Placeholder IDs - to be updated with actual
]

CAMPBELL_KEYWORDS = [
    "campbell", "downtown campbell", "campbell avenue", "pruneyard", "orchard city",
    "bascom avenue", "hamilton avenue", "winchester mystery house adjacent"
]

# Saratoga identification criteria
SARATOGA_ZIP_CODES = [
    "95070", "95071"
]

SARATOGA_LOCATION_IDS = [
    "213070961", "213987667", "214123469"  # Placeholder IDs - to be updated with actual
]

SARATOGA_KEYWORDS = [
    "saratoga", "villa montalvo", "hakone gardens", "saratoga village", "big basin way",
    "prospect road", "quito road", "congress springs"
]

# Fremont identification criteria
FREMONT_ZIP_CODES = [
    "94536", "94537", "94538", "94539", "94555"
]

FREMONT_LOCATION_IDS = [
    "213070962", "213987668", "214123470"  # Placeholder IDs - to be updated with actual
]

FREMONT_KEYWORDS = [
    "fremont", "tesla factory", "newby island", "ardenwood", "central park fremont",
    "pacific commons", "warm springs", "mission san jose", "niles"
]

# Morgan Hill identification criteria
MORGAN_HILL_ZIP_CODES = [
    "95037", "95038"
]

MORGAN_HILL_LOCATION_IDS = [
    "213070963", "213987669", "214123471"  # Placeholder IDs - to be updated with actual
]

MORGAN_HILL_KEYWORDS = [
    "morgan hill", "downtown morgan hill", "monterey road morgan hill", "cochrane plaza",
    "live oak high school", "burnett elementary"
]

# Atherton identification criteria
ATHERTON_ZIP_CODES = [
    "94027"
]

ATHERTON_LOCATION_IDS = [
    "213070964", "213987670", "214123472"  # Placeholder IDs - to be updated with actual
]

ATHERTON_KEYWORDS = [
    "atherton", "town of atherton", "holbrook palmer park", "middlefield road atherton",
    "marsh road", "fair oaks lane"
]

# San Carlos identification criteria
SAN_CARLOS_ZIP_CODES = [
    "94070", "94071"
]

SAN_CARLOS_LOCATION_IDS = [
    "213070965", "213987671", "214123473"  # Placeholder IDs - to be updated with actual
]

SAN_CARLOS_KEYWORDS = [
    "san carlos", "laurel street san carlos", "downtown san carlos", "caltrain san carlos",
    "hiller aviation museum", "pulgas water temple"
]

# East Palo Alto identification criteria
EAST_PALO_ALTO_ZIP_CODES = [
    "94303"  # Note: Same as some Palo Alto ZIP codes
]

EAST_PALO_ALTO_LOCATION_IDS = [
    "213070966", "213987672", "214123474"  # Placeholder IDs - to be updated with actual
]

EAST_PALO_ALTO_KEYWORDS = [
    "east palo alto", "epa", "university avenue epa", "bay road", "cooley landing",
    "ravenswood", "east palo alto academy"
]

# Foster City identification criteria
FOSTER_CITY_ZIP_CODES = [
    "94404"  # Note: Same as some San Mateo ZIP codes
]

FOSTER_CITY_LOCATION_IDS = [
    "213070967", "213987673", "214123475"  # Placeholder IDs - to be updated with actual
]

FOSTER_CITY_KEYWORDS = [
    "foster city", "leo ryan park", "foster city boulevard", "shell boulevard",
    "bay meadows", "visa headquarters"
]

# Newark identification criteria
NEWARK_ZIP_CODES = [
    "94560"
]

NEWARK_LOCATION_IDS = [
    "213070968", "213987674", "214123476"  # Placeholder IDs - to be updated with actual
]

NEWARK_KEYWORDS = [
    "newark", "newark community center", "newark pavilion", "mowry avenue", "cherry street"
]

# Woodside identification criteria
WOODSIDE_ZIP_CODES = [
    "94062"  # Note: Same as some Redwood City ZIP codes
]

WOODSIDE_LOCATION_IDS = [
    "213070969", "213987675", "214123477"  # Placeholder IDs - to be updated with actual
]

WOODSIDE_KEYWORDS = [
    "woodside", "town of woodside", "woodside road", "canada road", "roberts market",
    "folger stable", "filoli"
]

# San Francisco identification criteria
SAN_FRANCISCO_ZIP_CODES = [
    "94102", "94103", "94104", "94105", "94107", "94108", "94109", "94110", "94111", 
    "94112", "94114", "94115", "94116", "94117", "94118", "94119", "94120", "94121", 
    "94122", "94123", "94124", "94125", "94126", "94127", "94129", "94130", "94131", 
    "94132", "94133", "94134", "94137", "94139", "94140", "94141", "94142", "94143", 
    "94144", "94145", "94146", "94147", "94151", "94158", "94159", "94160", "94161", 
    "94163", "94164", "94172", "94177", "94188"
]

SAN_FRANCISCO_LOCATION_IDS = [
    "213070970", "213987676", "214123478"  # Placeholder IDs - to be updated with actual
]

SAN_FRANCISCO_KEYWORDS = [
    "san francisco", "sf", "the city", "bay area", "golden gate", "lombard street",
    "fisherman's wharf", "pier 39", "union square", "chinatown", "north beach", "soma",
    "mission district", "castro", "haight", "richmond", "sunset", "nob hill", "pac heights",
    "financial district", "embarcadero", "coit tower", "alcatraz", "presidio", "marina",
    "fillmore", "hayes valley", "potrero hill", "bernal heights", "outer sunset",
    "muni", "bart", "caltrain", "giants", "warriors", "49ers"
]

# Hayward identification criteria
HAYWARD_ZIP_CODES = [
    "94540", "94541", "94542", "94543", "94544", "94545", "94557"
]

HAYWARD_LOCATION_IDS = [
    "215651420"  # Known Hayward location ID
]

HAYWARD_KEYWORDS = [
    "hayward", "east bay", "alameda county", "510", "cal state east bay", "csueb", 
    "chabot college", "hayward hills", "castro valley", "san lorenzo", "union city",
    "fremont", "newark", "alameda", "berkeley", "oakland", "san leandro",
    "hayward bart", "south hayward", "hayward regional", "garin park",
    "hayward shoreline", "sulphur creek", "downtown hayward", "mission blvd hayward"
]

# Initialize API
api = InstagramAPI(token=API_TOKEN)

def check_location_match(user_data, zip_codes, keywords, location_ids):
    """Generic function to check if user matches location criteria"""
    # Get all user profile fields
    bio = user_data.get("biography", "").lower()
    full_name = user_data.get("full_name", "").lower() 
    username = user_data.get("username", "").lower()
    
    # Get location field if available
    location_info = ""
    if "location" in user_data and user_data["location"]:
        location_info = str(user_data["location"]).lower()
    
    # Check location IDs if available
    location_id = str(user_data.get('location_id', ''))
    if location_id in location_ids:
        return True
    
    # Combine all text fields for comprehensive search
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

def is_san_jose_user(user_data):
    """Check if user is from San Jose based on profile information"""
    return check_location_match(user_data, SAN_JOSE_ZIP_CODES, SAN_JOSE_KEYWORDS, SAN_JOSE_LOCATION_IDS)

def is_palo_alto_user(user_data):
    """Check if user is from Palo Alto based on profile information"""
    return check_location_match(user_data, PALO_ALTO_ZIP_CODES, PALO_ALTO_KEYWORDS, PALO_ALTO_LOCATION_IDS)

def is_sunnyvale_user(user_data):
    """Check if user is from Sunnyvale based on profile information"""
    return check_location_match(user_data, SUNNYVALE_ZIP_CODES, SUNNYVALE_KEYWORDS, SUNNYVALE_LOCATION_IDS)

def is_mountain_view_user(user_data):
    """Check if user is from Mountain View based on profile information"""
    return check_location_match(user_data, MOUNTAIN_VIEW_ZIP_CODES, MOUNTAIN_VIEW_KEYWORDS, MOUNTAIN_VIEW_LOCATION_IDS)

def is_cupertino_user(user_data):
    """Check if user is from Cupertino based on profile information"""
    return check_location_match(user_data, CUPERTINO_ZIP_CODES, CUPERTINO_KEYWORDS, CUPERTINO_LOCATION_IDS)

def is_milpitas_user(user_data):
    """Check if user is from Milpitas based on profile information"""
    return check_location_match(user_data, MILPITAS_ZIP_CODES, MILPITAS_KEYWORDS, MILPITAS_LOCATION_IDS)

def is_menlo_park_user(user_data):
    """Check if user is from Menlo Park based on profile information"""
    return check_location_match(user_data, MENLO_PARK_ZIP_CODES, MENLO_PARK_KEYWORDS, MENLO_PARK_LOCATION_IDS)

def is_los_gatos_user(user_data):
    """Check if user is from Los Gatos based on profile information"""
    return check_location_match(user_data, LOS_GATOS_ZIP_CODES, LOS_GATOS_KEYWORDS, LOS_GATOS_LOCATION_IDS)

def is_santa_clara_user(user_data):
    """Check if user is from Santa Clara based on profile information"""
    return check_location_match(user_data, SANTA_CLARA_ZIP_CODES, SANTA_CLARA_KEYWORDS, SANTA_CLARA_LOCATION_IDS)

def is_redwood_city_user(user_data):
    """Check if user is from Redwood City based on profile information"""
    return check_location_match(user_data, REDWOOD_CITY_ZIP_CODES, REDWOOD_CITY_KEYWORDS, REDWOOD_CITY_LOCATION_IDS)

def is_san_mateo_user(user_data):
    """Check if user is from San Mateo based on profile information"""
    return check_location_match(user_data, SAN_MATEO_ZIP_CODES, SAN_MATEO_KEYWORDS, SAN_MATEO_LOCATION_IDS)

def is_los_altos_user(user_data):
    """Check if user is from Los Altos based on profile information"""
    return check_location_match(user_data, LOS_ALTOS_ZIP_CODES, LOS_ALTOS_KEYWORDS, LOS_ALTOS_LOCATION_IDS)

def is_campbell_user(user_data):
    """Check if user is from Campbell based on profile information"""
    return check_location_match(user_data, CAMPBELL_ZIP_CODES, CAMPBELL_KEYWORDS, CAMPBELL_LOCATION_IDS)

def is_saratoga_user(user_data):
    """Check if user is from Saratoga based on profile information"""
    return check_location_match(user_data, SARATOGA_ZIP_CODES, SARATOGA_KEYWORDS, SARATOGA_LOCATION_IDS)

def is_fremont_user(user_data):
    """Check if user is from Fremont based on profile information"""
    return check_location_match(user_data, FREMONT_ZIP_CODES, FREMONT_KEYWORDS, FREMONT_LOCATION_IDS)

def is_morgan_hill_user(user_data):
    """Check if user is from Morgan Hill based on profile information"""
    return check_location_match(user_data, MORGAN_HILL_ZIP_CODES, MORGAN_HILL_KEYWORDS, MORGAN_HILL_LOCATION_IDS)

def is_atherton_user(user_data):
    """Check if user is from Atherton based on profile information"""
    return check_location_match(user_data, ATHERTON_ZIP_CODES, ATHERTON_KEYWORDS, ATHERTON_LOCATION_IDS)

def is_san_carlos_user(user_data):
    """Check if user is from San Carlos based on profile information"""
    return check_location_match(user_data, SAN_CARLOS_ZIP_CODES, SAN_CARLOS_KEYWORDS, SAN_CARLOS_LOCATION_IDS)

def is_east_palo_alto_user(user_data):
    """Check if user is from East Palo Alto based on profile information"""
    return check_location_match(user_data, EAST_PALO_ALTO_ZIP_CODES, EAST_PALO_ALTO_KEYWORDS, EAST_PALO_ALTO_LOCATION_IDS)

def is_foster_city_user(user_data):
    """Check if user is from Foster City based on profile information"""
    return check_location_match(user_data, FOSTER_CITY_ZIP_CODES, FOSTER_CITY_KEYWORDS, FOSTER_CITY_LOCATION_IDS)

def is_newark_user(user_data):
    """Check if user is from Newark based on profile information"""
    return check_location_match(user_data, NEWARK_ZIP_CODES, NEWARK_KEYWORDS, NEWARK_LOCATION_IDS)

def is_woodside_user(user_data):
    """Check if user is from Woodside based on profile information"""
    return check_location_match(user_data, WOODSIDE_ZIP_CODES, WOODSIDE_KEYWORDS, WOODSIDE_LOCATION_IDS)

def is_san_francisco_user(user_data):
    """Check if user is from San Francisco based on profile information"""
    return check_location_match(user_data, SAN_FRANCISCO_ZIP_CODES, SAN_FRANCISCO_KEYWORDS, SAN_FRANCISCO_LOCATION_IDS)

def is_hayward_user(user_data):
    """Check if user is from Hayward based on profile information"""
    return check_location_match(user_data, HAYWARD_ZIP_CODES, HAYWARD_KEYWORDS, HAYWARD_LOCATION_IDS)

def is_fake_follower(user_data):
    """Detect if a follower appears to be fake using balanced scoring system"""
    # Get profile data
    username = user_data.get("username", "").lower()
    full_name = user_data.get("full_name", "")
    biography = user_data.get("biography", "")
    follower_count = user_data.get("edge_followed_by", {}).get("count", 0)
    following_count = user_data.get("edge_follow", {}).get("count", 0)
    media_count = user_data.get("edge_owner_to_timeline_media", {}).get("count", 0)
    has_profile_pic = user_data.get("profile_pic_url", "") != ""
    is_verified = user_data.get("is_verified", False)
    is_private = user_data.get("is_private", False)
    
    # Verified accounts are never fake
    if is_verified:
        return False
    
    fake_score = 0
    
    # MAJOR RED FLAGS (High Weight)
    
    # 1. Extreme following/follower ratio (bots follow many, have few followers)
    if follower_count > 0 and following_count > 0:
        ratio = following_count / follower_count
        if ratio > 4:  # Following 4x more than followers
            fake_score += 3
        elif ratio > 2.5:
            fake_score += 2
        elif ratio > 1.5:
            fake_score += 1
    
    # 2. High following count with very low followers (classic bot pattern)
    if following_count > 1000 and follower_count < 100:
        fake_score += 3
    elif following_count > 500 and follower_count < 50:
        fake_score += 2
    
    # 3. No profile picture (major indicator)
    if not has_profile_pic:
        fake_score += 2
    
    # 4. No posts but high activity (following many)
    if media_count == 0 and following_count > 200:
        fake_score += 2
    elif media_count == 0 and following_count > 50:
        fake_score += 1
    
    # MODERATE RED FLAGS (Medium Weight)
    
    # 5. Suspicious username patterns
    bot_patterns = ["user", "account", "real", "official", "follow", "insta"]
    number_heavy = sum(1 for c in username if c.isdigit()) > len(username) * 0.4
    
    if any(pattern in username for pattern in bot_patterns):
        fake_score += 2
    elif number_heavy or username.count("_") > 2:
        fake_score += 1
    
    # 6. Empty or generic bio
    if not biography.strip():
        fake_score += 1
    elif len(biography.strip()) < 10:
        fake_score += 1
    
    # 7. Generic or empty display name
    if not full_name.strip():
        fake_score += 1
    elif full_name.lower() in ["user", "account", "real", "official", "follow"]:
        fake_score += 2
    
    # 8. Very few posts for account age (assuming older accounts should have more posts)
    if media_count <= 5 and following_count > 150:
        fake_score += 1
    
    # MINOR RED FLAGS (Low Weight)
    
    # 9. High following count (bots tend to follow many accounts)
    if following_count > 1500:
        fake_score += 1
    
    # 10. Very low engagement indicators
    if follower_count < 20 and following_count > 500:
        fake_score += 1
    
    # THRESHOLD: Score >= 2.0 indicates likely fake follower
    # This should catch ~14-15% as fake, which aligns with sjfoodies baseline
    return fake_score >= 2.0

def count_location_followers_and_analyze_gender(user_pk: int, target_sample: int = SAMPLE_SIZE) -> dict:
    """Count followers for all Bay Area cities, fake followers, AND analyze gender using the SAME sample. Returns dict with counts, gender data, and sample_size"""
    
    # Initialize counters for all cities plus fake followers
    city_counts = {
        'san_jose': 0,
        'palo_alto': 0,
        'sunnyvale': 0,
        'mountain_view': 0,
        'cupertino': 0,
        'milpitas': 0,
        'menlo_park': 0,
        'los_gatos': 0,
        'santa_clara': 0,
        'redwood_city': 0,
        'san_mateo': 0,
        'los_altos': 0,
        'campbell': 0,
        'saratoga': 0,
        'fremont': 0,
        'morgan_hill': 0,
        'atherton': 0,
        'san_carlos': 0,
        'east_palo_alto': 0,
        'foster_city': 0,
        'newark': 0,
        'woodside': 0,
        'san_francisco': 0,
        'hayward': 0,
        'fake_followers': 0
    }
    
    # Initialize gender counters
    male_count = 0
    female_count = 0
    unknown_count = 0
    
    # Gender indicators
    male_indicators = [
        'john', 'mike', 'david', 'chris', 'alex', 'ryan', 'kevin', 'brian', 'jason', 'daniel',
        'matthew', 'andrew', 'joshua', 'james', 'robert', 'michael', 'william', 'richard',
        'joseph', 'thomas', 'charles', 'anthony', 'mark', 'donald', 'steven', 'paul',
        'kenneth', 'joshua', 'kevin', 'brian', 'george', 'edward', 'ronald', 'timothy',
        'boy', 'man', 'guy', 'dude', 'bro', 'mr'
    ]
    
    female_indicators = [
        'sarah', 'jennifer', 'lisa', 'karen', 'donna', 'carol', 'ruth', 'sharon', 'michelle',
        'laura', 'emily', 'kimberly', 'deborah', 'dorothy', 'amy', 'angela', 'ashley',
        'brenda', 'emma', 'olivia', 'sophia', 'isabella', 'charlotte', 'amelia', 'mia',
        'harper', 'evelyn', 'abigail', 'emily', 'ella', 'elizabeth', 'camila', 'luna',
        'sofia', 'avery', 'mila', 'aria', 'scarlett', 'penelope', 'layla', 'chloe',
        'victoria', 'madison', 'eleanor', 'grace', 'nora', 'riley', 'zoey', 'hannah',
        'hazel', 'lily', 'ellie', 'violet', 'lillian', 'zoe', 'stella', 'aurora',
        'natalie', 'emilia', 'everly', 'leah', 'aubrey', 'willow', 'addison', 'lucy',
        'girl', 'woman', 'lady', 'gal', 'miss', 'mrs', 'ms'
    ]
    
    # City check functions mapping
    city_checks = {
        'san_jose': is_san_jose_user,
        'palo_alto': is_palo_alto_user,
        'sunnyvale': is_sunnyvale_user,
        'mountain_view': is_mountain_view_user,
        'cupertino': is_cupertino_user,
        'milpitas': is_milpitas_user,
        'menlo_park': is_menlo_park_user,
        'los_gatos': is_los_gatos_user,
        'santa_clara': is_santa_clara_user,
        'redwood_city': is_redwood_city_user,
        'san_mateo': is_san_mateo_user,
        'los_altos': is_los_altos_user,
        'campbell': is_campbell_user,
        'saratoga': is_saratoga_user,
        'fremont': is_fremont_user,
        'morgan_hill': is_morgan_hill_user,
        'atherton': is_atherton_user,
        'san_carlos': is_san_carlos_user,
        'east_palo_alto': is_east_palo_alto_user,
        'foster_city': is_foster_city_user,
        'newark': is_newark_user,
        'woodside': is_woodside_user,
        'san_francisco': is_san_francisco_user,
        'hayward': is_hayward_user,
        'fake_followers': is_fake_follower
    }
    
    max_id = None
    total_checked = 0
    
    try:
        print(f"    🔍 Scanning {target_sample} followers for all Bay Area cities and fake followers...")
        
        while total_checked < target_sample:
            batch = api.get_user_followers(user_id=user_pk, count=25, max_id=max_id)
            if not batch or "users" not in batch:
                break
                
            users = batch["users"]
            batch_counts = {city: 0 for city in city_counts.keys()}
            
            for user in users:
                if total_checked >= target_sample:
                    break
                
                total_checked += 1
                
                # Check each city and fake followers for this user
                for city, check_func in city_checks.items():
                    if check_func(user):
                        batch_counts[city] += 1
                        city_counts[city] += 1
                
                # ALSO analyze gender for this same user
                full_name = user.get("full_name", "").lower()
                username = user.get("username", "").lower()
                biography = user.get("biography", "").lower()
                
                # Combine all text for gender analysis
                text_to_analyze = f"{full_name} {username} {biography}"
                
                # Check for gender indicators
                male_score = sum(1 for indicator in male_indicators if indicator in text_to_analyze)
                female_score = sum(1 for indicator in female_indicators if indicator in text_to_analyze)
                
                if male_score > female_score:
                    male_count += 1
                elif female_score > male_score:
                    female_count += 1
                else:
                    unknown_count += 1
                        

            
            # Show progress for cities and fake followers with matches in this batch
            active_cities = {city: count for city, count in batch_counts.items() if count > 0}
            if active_cities:
                city_summary = ", ".join([f"{city.replace('_', ' ').title()}: {count}" for city, count in active_cities.items()])
                print(f"       Found in batch: {city_summary}")
            
            # Stop if we've reached target sample
            if total_checked >= target_sample:
                print(f"       Sampled exactly {total_checked} followers")
                break
            
            max_id = batch.get("next_max_id")
            if not max_id:
                print(f"       Reached end of followers at {total_checked} sampled")
                break
                
            time.sleep(1.0)
            
    except Exception as e:
        print(f"       ⚠️  API limit reached after {total_checked} followers: {e}")
    
    # Calculate gender percentages
    if total_checked > 0:
        male_percentage = round((male_count / total_checked) * 100, 1)
        female_percentage = round((female_count / total_checked) * 100, 1)
        unknown_percentage = round((unknown_count / total_checked) * 100, 1)
    else:
        male_percentage = female_percentage = unknown_percentage = 0
    
    # Add sample size and gender data to the result
    city_counts['sample_size'] = total_checked
    city_counts['male_percentage'] = male_percentage
    city_counts['female_percentage'] = female_percentage
    city_counts['unknown_percentage'] = unknown_percentage
    city_counts['gender_sample_size'] = total_checked
    
    return city_counts

def calculate_engagement_metrics(user_pk: int, total_followers: int):
    """Calculate engagement rate, average likes, estimated reach, and posts per week"""
    try:
        # Get recent posts for engagement analysis
        posts_response = api.get_user_media(user_id=user_pk, count=12)  # Last 12 posts
        
        if not posts_response or "items" not in posts_response:
            return {
                'engagement_rate': 0,
                'average_likes': 0,
                'estimated_reach': 0,
                'average_posts_per_week': 0
            }
        
        posts = posts_response["items"]
        if not posts:
            return {
                'engagement_rate': 0,
                'average_likes': 0,
                'estimated_reach': 0,
                'average_posts_per_week': 0
            }
        
        # Calculate engagement metrics
        total_likes = 0
        total_comments = 0
        post_count = len(posts)
        
        # Get timestamps for posts per week calculation
        timestamps = []
        
        for post in posts:
            likes = post.get("like_count", 0)
            comments = post.get("comment_count", 0)
            timestamp = post.get("taken_at", 0)
            
            total_likes += likes
            total_comments += comments
            if timestamp:
                timestamps.append(timestamp)
        
        # Calculate average likes
        average_likes = total_likes / post_count if post_count > 0 else 0
        
        # Calculate engagement rate (likes + comments) / followers * 100
        total_engagement = total_likes + total_comments
        engagement_rate = (total_engagement / post_count / total_followers * 100) if total_followers > 0 and post_count > 0 else 0
        
        # Calculate estimated reach (typically 10-30% of followers for good engagement)
        estimated_reach = int(total_followers * (engagement_rate / 100) * 3) if engagement_rate > 0 else int(total_followers * 0.1)
        
        # Calculate posts per week
        if len(timestamps) >= 2:
            # Sort timestamps and calculate time span
            timestamps.sort(reverse=True)  # Most recent first
            time_span_seconds = timestamps[0] - timestamps[-1]
            time_span_weeks = time_span_seconds / (7 * 24 * 60 * 60)  # Convert to weeks
            
            if time_span_weeks > 0:
                average_posts_per_week = post_count / time_span_weeks
            else:
                average_posts_per_week = post_count  # If all posts in same day
        else:
            average_posts_per_week = 0
        
        return {
            'engagement_rate': round(engagement_rate, 2),
            'average_likes': int(average_likes),
            'estimated_reach': estimated_reach,
            'average_posts_per_week': round(average_posts_per_week, 1)
        }
        
    except Exception as e:
        print(f"       ⚠️  Error calculating engagement metrics: {e}")
        return {
            'engagement_rate': 0,
            'average_likes': 0,
            'estimated_reach': 0,
            'average_posts_per_week': 0
        }



def analyze_influencer(username: str):
    """Analyze a single influencer for all Bay Area city followers"""
    print(f"\n🔍 ANALYZING: @{username}")
    print("=" * 60)
    
    try:
        # Get user info
        response = api.get_user_info(username)
        
        if response and isinstance(response, dict):
            user_data = response.get("data", {}).get("user", {})
            
            if user_data:
                total_followers = user_data.get("edge_followed_by", {}).get("count", 0)
                full_name = user_data.get("full_name", "Unknown")
                biography = user_data.get("biography", "")
                is_verified = user_data.get("is_verified", False)
                user_pk = int(user_data.get("id", 0))
                
                print(f"📊 Profile: {full_name}")
                print(f"✅ Verified: {'Yes' if is_verified else 'No'}")
                print(f"👥 Total Followers: {total_followers:,}")
                
                if user_pk:
                    # Calculate engagement metrics
                    print(f"    📈 Calculating engagement metrics...")
                    engagement_metrics = calculate_engagement_metrics(user_pk, total_followers)
                    
                    # Analyze city followers AND gender using the SAME 300 sample
                    print(f"    🔍 Analyzing {SAMPLE_SIZE} followers for cities, fake followers, AND gender...")
                    city_results = count_location_followers_and_analyze_gender(user_pk, SAMPLE_SIZE)
                    sample_size = city_results.pop('sample_size')  # Remove sample_size from city_results
                    
                    # Extract gender data from the same results
                    male_percentage = city_results.pop('male_percentage')
                    female_percentage = city_results.pop('female_percentage') 
                    unknown_percentage = city_results.pop('unknown_percentage')
                    gender_sample_size = city_results.pop('gender_sample_size')
                    
                    # Calculate percentages and show summary for cities with followers
                    print(f"\n📍 City breakdown (sample: {sample_size}):")
                    active_cities = {city: count for city, count in city_results.items() if count > 0}
                    
                    if active_cities:
                        for city, count in active_cities.items():
                            pct = (count / sample_size * 100) if sample_size > 0 else 0
                            city_display = city.replace('_', ' ').title()
                            print(f"   {city_display}: {count} ({pct:.1f}%)")
                    else:
                        print("   No followers found in any tracked Bay Area cities")
                    
                    # Print gender analysis results
                    print(f"       Gender analysis: {male_percentage}% male, {female_percentage}% female, {unknown_percentage}% unknown")
                    
                    # Prepare result with all city data and new metrics
                    result = {
                        'username': username,
                        'full_name': full_name,
                        'description': biography,
                        'total_followers': total_followers,
                        'sample_size': sample_size,
                        'is_verified': is_verified,
                        'engagement_rate': engagement_metrics['engagement_rate'],
                        'average_likes': engagement_metrics['average_likes'],
                        'estimated_reach': engagement_metrics['estimated_reach'],
                        'average_posts_per_week': engagement_metrics['average_posts_per_week'],
                        'male_percentage': male_percentage,
                        'female_percentage': female_percentage,
                        'unknown_percentage': unknown_percentage,
                        'gender_sample_size': gender_sample_size,
                        'status': 'success'
                    }
                    
                    # Add all city follower counts
                    for city, count in city_results.items():
                        if city == 'fake_followers':
                            result['fake_followers'] = count  # Special case for fake followers
                        else:
                            result[f'{city}_followers'] = count
                    
                    return result
                else:
                    print("❌ Could not get user ID for follower analysis")
            else:
                print("❌ No user data found")
        else:
            print("❌ Failed to get user info")
            
    except Exception as e:
        print(f"❌ Error analyzing {username}: {e}")
    
    # Error result with all city counts as 0
    error_result = {
        'username': username,
        'full_name': 'Error',
        'description': '',
        'total_followers': 0,
        'sample_size': 0,
        'is_verified': False,
        'engagement_rate': 0,
        'average_likes': 0,
        'estimated_reach': 0,
        'average_posts_per_week': 0,
        'male_percentage': 0,
        'female_percentage': 0,
        'unknown_percentage': 0,
        'gender_sample_size': 0,
        'status': 'error'
    }
    
    # Add all city follower counts as 0
    city_names = ['san_jose', 'palo_alto', 'sunnyvale', 'mountain_view', 'cupertino', 'milpitas', 
                 'menlo_park', 'los_gatos', 'santa_clara', 'redwood_city', 'san_mateo', 'los_altos',
                 'campbell', 'saratoga', 'fremont', 'morgan_hill', 'atherton', 'san_carlos',
                 'east_palo_alto', 'foster_city', 'newark', 'woodside', 'san_francisco', 'hayward']
    
    for city in city_names:
        error_result[f'{city}_followers'] = 0
    
    # Special case for fake followers
    error_result['fake_followers'] = 0
    
    return error_result

def main():
    """Main execution function"""
    print("🚀 COMPREHENSIVE BAY AREA LOCATION ANALYSIS + FAKE FOLLOWER DETECTION")
    print(f"📊 Sample size: {SAMPLE_SIZE} followers per influencer")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏙️ Tracking 24 Bay Area cities with comprehensive ZIP codes and keywords")
    print(f"🤖 PLUS fake follower detection using advanced profile analysis")
    print(f"🔍 San Jose: {len(SAN_JOSE_ZIP_CODES)} ZIP codes, {len(SAN_JOSE_KEYWORDS)} keywords")
    print(f"🔍 San Francisco: {len(SAN_FRANCISCO_ZIP_CODES)} ZIP codes, {len(SAN_FRANCISCO_KEYWORDS)} keywords")
    print(f"🔍 Hayward: {len(HAYWARD_ZIP_CODES)} ZIP codes, {len(HAYWARD_KEYWORDS)} keywords")
    print(f"🔍 Plus 21 other Bay Area cities with full ZIP code coverage")
    print("=" * 80)
    
    # Read influencer list
    influencers = []
    try:
        with open("influencer_list.txt", "r", encoding="utf-8") as file:
            for line in file:
                username = line.strip()
                if username:  # Skip empty lines
                    influencers.append(username)
    except FileNotFoundError:
        print("❌ influencer_list.txt file not found")
        return
    
    print(f"📋 Found {len(influencers)} influencers to analyze: {', '.join(influencers)}")
    
    # Test API connection
    print("\n🔌 Testing API connection...")
    try:
        test = api.get_user_info("instagram")
        if test:
            print("✅ API connection successful")
        else:
            print("❌ API connection failed")
            return
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return
    
    results = []
    
    # Analyze each influencer
    for i, username in enumerate(influencers, 1):
        print(f"\n[{i:2d}/{len(influencers)}] Processing @{username}")
        print("-" * 70)
        
        result = analyze_influencer(username)
        results.append(result)
        
        # Show running totals for key cities
        successful = [r for r in results if r['status'] == 'success']
        if successful:
            total_sampled = sum(r['sample_size'] for r in successful)
            
            # Calculate totals for key cities and fake followers
            key_cities = ['san_jose', 'san_francisco', 'palo_alto', 'sunnyvale', 'mountain_view', 'hayward', 'fake_followers']
            running_totals = {}
            
            for city in key_cities:
                if city == 'fake_followers':
                    city_total = sum(r.get('fake_followers', 0) for r in successful)
                else:
                    city_total = sum(r.get(f'{city}_followers', 0) for r in successful)
                city_pct = (city_total / total_sampled * 100) if total_sampled > 0 else 0
                running_totals[city] = (city_total, city_pct)
            
            print(f"🏃 Running totals (top cities + fake followers):")
            for city, (total, pct) in running_totals.items():
                if total > 0:  # Only show cities with followers
                    city_display = city.replace('_', ' ').title()
                    print(f"   {city_display}: {total}/{total_sampled} = {pct:.1f}%")
        
        # Brief pause between accounts
        if i < len(influencers):
            time.sleep(2.0)
    
    # Save results to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"influencer_data/comprehensive_bay_area_analysis_{timestamp}.csv"
    
    # Define all city columns for CSV plus fake followers
    city_columns = [
        'san_jose_followers', 'palo_alto_followers', 'sunnyvale_followers', 'mountain_view_followers',
        'cupertino_followers', 'milpitas_followers', 'menlo_park_followers', 'los_gatos_followers',
        'santa_clara_followers', 'redwood_city_followers', 'san_mateo_followers', 'los_altos_followers',
        'campbell_followers', 'saratoga_followers', 'fremont_followers', 'morgan_hill_followers',
        'atherton_followers', 'san_carlos_followers', 'east_palo_alto_followers', 'foster_city_followers',
        'newark_followers', 'woodside_followers', 'san_francisco_followers', 'hayward_followers',
        'fake_followers'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'username', 'full_name', 'description', 'total_followers', 'sample_size',
            'engagement_rate', 'average_likes', 'estimated_reach', 'average_posts_per_week',
            'male_percentage', 'female_percentage', 'unknown_percentage', 'gender_sample_size'
        ] + city_columns
        
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            if result['status'] == 'success':
                csv_row = {
                    'username': result['username'],
                    'full_name': result['full_name'],
                    'description': result['description'][:200] + "..." if len(result['description']) > 200 else result['description'],
                    'total_followers': result['total_followers'],
                    'sample_size': result['sample_size'],
                    'engagement_rate': result['engagement_rate'],
                    'average_likes': result['average_likes'],
                    'estimated_reach': result['estimated_reach'],
                    'average_posts_per_week': result['average_posts_per_week'],
                    'male_percentage': result['male_percentage'],
                    'female_percentage': result['female_percentage'],
                    'unknown_percentage': result['unknown_percentage'],
                    'gender_sample_size': result['gender_sample_size']
                }
                
                # Add all city follower counts
                for city_col in city_columns:
                    csv_row[city_col] = result.get(city_col, 0)
                
                writer.writerow(csv_row)
    
    # Display summary
    successful = [r for r in results if r['status'] == 'success']
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"📁 Results saved to: {output_file}")
    print(f"✅ Successfully analyzed: {len(successful)}/{len(influencers)} influencers")
    
    if successful:
        total_followers = sum(r['total_followers'] for r in successful)
        total_sampled = sum(r['sample_size'] for r in successful)
        verified_count = sum(1 for r in successful if r['is_verified'])
        
        # Calculate totals for all cities and fake followers
        all_cities = ['san_jose', 'palo_alto', 'sunnyvale', 'mountain_view', 'cupertino', 'milpitas',
                     'menlo_park', 'los_gatos', 'santa_clara', 'redwood_city', 'san_mateo', 'los_altos',
                     'campbell', 'saratoga', 'fremont', 'morgan_hill', 'atherton', 'san_carlos',
                     'east_palo_alto', 'foster_city', 'newark', 'woodside', 'san_francisco', 'hayward',
                     'fake_followers']
        
        city_totals = {}
        for city in all_cities:
            if city == 'fake_followers':
                total = sum(r.get('fake_followers', 0) for r in successful)
            else:
                total = sum(r.get(f'{city}_followers', 0) for r in successful)
            pct = (total / total_sampled * 100) if total_sampled > 0 else 0
            if total > 0:  # Only track cities with followers
                city_totals[city] = (total, pct)
        
        print(f"\n📈 OVERALL RESULTS:")
        print(f"   • Total combined followers: {total_followers:,}")
        print(f"   • Total followers sampled: {total_sampled:,}")
        print(f"   • Verified accounts: {verified_count}")
        print(f"   • Cities with followers found: {len(city_totals)}")
        
        if city_totals:
            print(f"\n🏙️ CITY BREAKDOWN:")
            # Sort cities by follower count (descending)
            sorted_cities = sorted(city_totals.items(), key=lambda x: x[1][0], reverse=True)
            for city, (total, pct) in sorted_cities:
                city_display = city.replace('_', ' ').title()
                print(f"   • {city_display}: {total} followers ({pct:.1f}%)")
        
        print(f"\n📊 TOP INDIVIDUAL RESULTS:")
        # Show top results for cities with most followers
        top_cities = sorted(city_totals.items(), key=lambda x: x[1][0], reverse=True)[:5]
        for city, _ in top_cities:
            city_display = city.replace('_', ' ').title()
            print(f"\n   {city_display} leaders:")
            if city == 'fake_followers':
                city_results = [(r['username'], r.get('fake_followers', 0)) for r in successful]
            else:
                city_results = [(r['username'], r.get(f'{city}_followers', 0)) for r in successful]
            city_results = [(username, count) for username, count in city_results if count > 0]
            city_results.sort(key=lambda x: x[1], reverse=True)
            for username, count in city_results[:3]:  # Top 3 for each city
                print(f"     @{username}: {count} followers")

if __name__ == "__main__":
    main() 