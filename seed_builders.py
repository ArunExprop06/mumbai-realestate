"""Seed realistic properties from top Mumbai builders."""
from extensions import db
from models import Property, Locality, User
from helpers import slugify


def seed_builder_properties():
    """Add properties from top Mumbai builders."""

    # Get or create a builder agent for each builder
    localities = db.session.query(Locality).all()
    loc_map = {}
    for l in localities:
        loc_map[l.name] = l.id

    builders = [
        {"name": "Lodha Group", "email": "sales@lodhagroup.com", "phone": "9820012345", "company": "Lodha Group", "rera": "P51900001234"},
        {"name": "Oberoi Realty", "email": "sales@oberoirealty.com", "phone": "9820023456", "company": "Oberoi Realty Ltd", "rera": "P51900002345"},
        {"name": "Godrej Properties", "email": "sales@godrejproperties.com", "phone": "9820034567", "company": "Godrej Properties Ltd", "rera": "P51900003456"},
        {"name": "Hiranandani Group", "email": "sales@hiranandani.com", "phone": "9820045678", "company": "Hiranandani Group", "rera": "P51900004567"},
        {"name": "Rustomjee Group", "email": "sales@rustomjee.com", "phone": "9820056789", "company": "Rustomjee Builders", "rera": "P51900005678"},
        {"name": "Runwal Group", "email": "sales@runwal.com", "phone": "9820067890", "company": "Runwal Developers", "rera": "P51900006789"},
        {"name": "Kalpataru Ltd", "email": "sales@kalpataru.com", "phone": "9820078901", "company": "Kalpataru Ltd", "rera": "P51900007890"},
        {"name": "Mahindra Lifespaces", "email": "sales@mahindralife.com", "phone": "9820089012", "company": "Mahindra Lifespace Developers", "rera": "P51900008901"},
        {"name": "Piramal Realty", "email": "sales@piramalrealty.com", "phone": "9820090123", "company": "Piramal Realty Pvt Ltd", "rera": "P51900009012"},
        {"name": "L&T Realty", "email": "sales@lntrealty.com", "phone": "9820001234", "company": "L&T Realty Ltd", "rera": "P51900010123"},
    ]

    builder_users = {}
    for b in builders:
        user = db.session.query(User).filter_by(email=b["email"]).first()
        if not user:
            user = User(
                name=b["name"], email=b["email"], phone=b["phone"],
                role="broker", company=b["company"], rera_number=b["rera"],
                is_approved=True
            )
            user.set_password("builder123")
            db.session.add(user)
            db.session.commit()
        builder_users[b["company"]] = user.id

    properties_data = [
        # ===== LODHA GROUP =====
        {
            "title": "Lodha Park - Ultra Luxury 4 BHK at Worli",
            "property_type": "flat", "listing_type": "buy",
            "price": 12.5, "price_unit": "crore", "bhk": 4,
            "area_sqft": 3200, "carpet_area": 2450,
            "floor_number": 45, "total_floors": 65, "age_years": 2,
            "furnished": "semi", "facing": "West",
            "description": "Lodha Park, Worli - an iconic ultra-luxury residential tower by Lodha Group. This magnificent 4 BHK features floor-to-ceiling windows with uninterrupted Arabian Sea views. Italian marble flooring, imported fixtures, private lift lobby. World-class amenities including infinity pool, spa, concierge service, and 5-tier security. One of Mumbai's most prestigious addresses.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Concierge","Spa","Jogging Track","CCTV","Intercom"]',
            "address": "Lodha Park, Dr Annie Besant Road, Worli",
            "locality": "Worli", "company": "Lodha Group",
            "is_featured": True, "views_count": 890
        },
        {
            "title": "Lodha Bellezza - Premium 3 BHK in Kuala Lumpur Junction, Goregaon",
            "property_type": "flat", "listing_type": "buy",
            "price": 2.85, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1650, "carpet_area": 1200,
            "floor_number": 18, "total_floors": 32, "age_years": 3,
            "furnished": "semi", "facing": "East",
            "description": "Premium 3 BHK in Lodha Bellezza, Goregaon West. Spacious living areas, modular kitchen with chimney and hob, vitrified tile flooring. Amenities include Olympic-size pool, gymnasium, badminton court, and landscaped gardens. Close to Western Express Highway and Goregaon station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track"]',
            "address": "Lodha Bellezza, New Link Road, Goregaon West",
            "locality": "Goregaon", "company": "Lodha Group",
            "is_featured": False, "views_count": 445
        },
        {
            "title": "Lodha Amara - Affordable 2 BHK in Thane",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.15, "price_unit": "crore", "bhk": 2,
            "area_sqft": 950, "carpet_area": 720,
            "floor_number": 12, "total_floors": 28, "age_years": 4,
            "furnished": "unfurnished", "facing": "North",
            "description": "Well-designed 2 BHK in Lodha Amara, Kolshet Road, Thane. Excellent township with 4000+ families. School, hospital, shopping centre within the complex. Beautiful landscaping, multiple play areas, and sports facilities. 10 minutes from Thane station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area","Jogging Track","Fire Safety"]',
            "address": "Lodha Amara, Kolshet Road, Thane West",
            "locality": "Thane West", "company": "Lodha Group",
            "is_featured": False, "views_count": 567
        },
        {
            "title": "Lodha Crown Taloja - Budget 1 BHK Near Panvel",
            "property_type": "flat", "listing_type": "buy",
            "price": 48, "price_unit": "lakh", "bhk": 1,
            "area_sqft": 480, "carpet_area": 370,
            "floor_number": 6, "total_floors": 20, "age_years": 1,
            "furnished": "unfurnished", "facing": "East",
            "description": "Affordable 1 BHK in Lodha Crown, Taloja near upcoming Navi Mumbai International Airport. Smart home features, modular kitchen, vitrified tiles. Part of integrated township with school, shopping, and healthcare. Excellent investment opportunity.",
            "amenities": '["Parking","Lift","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Lodha Crown, Taloja, Navi Mumbai",
            "locality": "Panvel", "company": "Lodha Group",
            "is_featured": False, "views_count": 723
        },

        # ===== OBEROI REALTY =====
        {
            "title": "Oberoi Sky City - Luxurious 3 BHK in Borivali East",
            "property_type": "flat", "listing_type": "buy",
            "price": 3.45, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1850, "carpet_area": 1380,
            "floor_number": 35, "total_floors": 50, "age_years": 1,
            "furnished": "semi", "facing": "West",
            "description": "Oberoi Sky City offers unmatched luxury in Borivali East. This 3 BHK on the 35th floor boasts breathtaking Sanjay Gandhi National Park views. Premium specifications include VRV air conditioning, smart home automation, imported marble, and Grohe fittings. 65,000 sqft clubhouse with every amenity imaginable.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Spa","Garden","Jogging Track","CCTV","Intercom","Vastu Compliant"]',
            "address": "Oberoi Sky City, Western Express Highway, Borivali East",
            "locality": "Borivali", "company": "Oberoi Realty Ltd",
            "is_featured": True, "views_count": 678
        },
        {
            "title": "Oberoi Splendor Grande - 4 BHK Duplex Andheri East",
            "property_type": "flat", "listing_type": "buy",
            "price": 5.8, "price_unit": "crore", "bhk": 4,
            "area_sqft": 2800, "carpet_area": 2100,
            "floor_number": 28, "total_floors": 30, "age_years": 5,
            "furnished": "fully", "facing": "South",
            "description": "Rare duplex penthouse in Oberoi Splendor Grande, JVLR Andheri East. Sprawling 4 BHK with private terrace garden. Italian marble, Bulthaup kitchen, Duravit bathrooms. Panoramic city views. Premium complex with golf putting green, squash court, and business centre. 5 minutes from airport.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Terrace","Garden","CCTV","Intercom","Visitor Parking"]',
            "address": "Oberoi Splendor Grande, JVLR, Andheri East",
            "locality": "Andheri", "company": "Oberoi Realty Ltd",
            "is_featured": True, "views_count": 534
        },
        {
            "title": "Oberoi Commerz - Premium Office Space Goregaon",
            "property_type": "office", "listing_type": "rent",
            "price": 250000, "price_unit": "month", "bhk": None,
            "area_sqft": 3500, "carpet_area": 2800,
            "floor_number": 20, "total_floors": 35, "age_years": 3,
            "furnished": "fully", "facing": "West",
            "description": "Grade A+ commercial office in Oberoi Commerz, Goregaon East. Fully fitted with 60 workstations, 4 cabins, 2 conference rooms, server room, and pantry. Building features include food court, ATMs, EV charging, and dedicated Metro connectivity. Ideal for IT companies and MNCs.",
            "amenities": '["Parking","Lift","Security","Power Backup","Fire Safety","Cafeteria","CCTV","Visitor Parking"]',
            "address": "Oberoi Commerz, Oberoi Garden City, Goregaon East",
            "locality": "Goregaon", "company": "Oberoi Realty Ltd",
            "is_featured": False, "views_count": 312
        },

        # ===== GODREJ PROPERTIES =====
        {
            "title": "Godrej Platinum - 3 BHK with Terrace in Vikhroli",
            "property_type": "flat", "listing_type": "buy",
            "price": 4.2, "price_unit": "crore", "bhk": 3,
            "area_sqft": 2100, "carpet_area": 1580,
            "floor_number": 22, "total_floors": 40, "age_years": 2,
            "furnished": "semi", "facing": "East",
            "description": "Godrej Platinum in the heart of Vikhroli offers premium living within Godrej's iconic campus. This 3 BHK features a private terrace, double-height living room, and creek views. Surrounded by 100 acres of greenery including mangroves. IGBC Platinum-rated green building. Walking distance to Vikhroli station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Terrace","Garden","Jogging Track","Rainwater Harvesting","Vastu Compliant"]',
            "address": "Godrej Platinum, Pirojshanagar, Vikhroli East",
            "locality": "Vikhroli", "company": "Godrej Properties Ltd",
            "is_featured": True, "views_count": 456
        },
        {
            "title": "Godrej Exquisite - 2 BHK in Thane West",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.35, "price_unit": "crore", "bhk": 2,
            "area_sqft": 1000, "carpet_area": 750,
            "floor_number": 14, "total_floors": 25, "age_years": 3,
            "furnished": "unfurnished", "facing": "North",
            "description": "Smartly designed 2 BHK in Godrej Exquisite, Kavesar, Thane. Part of a sprawling township with over 3000 apartments. Vastu-compliant layout with cross ventilation. Amenities include temperature-controlled pool, mini theatre, and yoga centre. Close to Viviana Mall and Thane station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","CCTV"]',
            "address": "Godrej Exquisite, Kavesar, Thane West",
            "locality": "Thane West", "company": "Godrej Properties Ltd",
            "is_featured": False, "views_count": 389
        },
        {
            "title": "Godrej RKS - Ready 1 BHK for Rent in Chembur",
            "property_type": "flat", "listing_type": "rent",
            "price": 28000, "price_unit": "month", "bhk": 1,
            "area_sqft": 580, "carpet_area": 440,
            "floor_number": 8, "total_floors": 18, "age_years": 4,
            "furnished": "fully", "facing": "West",
            "description": "Fully furnished 1 BHK for rent in Godrej RKS, Chembur. Includes AC, washing machine, fridge, double bed, and modular kitchen. Gated society with swimming pool and gymnasium. Walking distance to Chembur station and R City Mall.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden"]',
            "address": "Godrej RKS, EEH, Chembur",
            "locality": "Chembur", "company": "Godrej Properties Ltd",
            "is_featured": False, "views_count": 567
        },

        # ===== HIRANANDANI =====
        {
            "title": "Hiranandani Gardens - Luxury 3 BHK in Powai",
            "property_type": "flat", "listing_type": "buy",
            "price": 3.75, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1700, "carpet_area": 1280,
            "floor_number": 16, "total_floors": 22, "age_years": 8,
            "furnished": "semi", "facing": "South",
            "description": "Classic Hiranandani 3 BHK in the heart of Powai's Hiranandani Gardens. Lake-facing apartment with stunning Powai lake views. Well-maintained society with lush landscaping. Walk to Galleria Mall, schools, hospitals. Hiranandani's signature European-style architecture. Premium address in Powai.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track","CCTV"]',
            "address": "Hiranandani Gardens, Powai",
            "locality": "Powai", "company": "Hiranandani Group",
            "is_featured": True, "views_count": 892
        },
        {
            "title": "Hiranandani Fortune City - 2 BHK Panvel",
            "property_type": "flat", "listing_type": "buy",
            "price": 72, "price_unit": "lakh", "bhk": 2,
            "area_sqft": 850, "carpet_area": 640,
            "floor_number": 10, "total_floors": 20, "age_years": 2,
            "furnished": "unfurnished", "facing": "East",
            "description": "Affordable Hiranandani quality in Fortune City, Panvel. Spacious 2 BHK with balcony in a well-planned township. Clubhouse, swimming pool, and sports facilities. Near upcoming Navi Mumbai airport. Growing infrastructure with new metro and expressway connectivity.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Hiranandani Fortune City, Panvel",
            "locality": "Panvel", "company": "Hiranandani Group",
            "is_featured": False, "views_count": 445
        },

        # ===== RUSTOMJEE =====
        {
            "title": "Rustomjee Crown - Sea-View 3 BHK Prabhadevi",
            "property_type": "flat", "listing_type": "buy",
            "price": 7.5, "price_unit": "crore", "bhk": 3,
            "area_sqft": 2200, "carpet_area": 1680,
            "floor_number": 38, "total_floors": 55, "age_years": 1,
            "furnished": "semi", "facing": "West",
            "description": "Rustomjee Crown at Prabhadevi - South Mumbai's most sought-after new address. Unobstructed sea views from every room. Designed by world-renowned architects. Features include Italian marble, VRV AC, home automation, and private lift lobby. 80,000 sqft clubhouse designed by Armani Casa.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Concierge","Spa","Terrace","CCTV","Intercom","Vastu Compliant"]',
            "address": "Rustomjee Crown, Prabhadevi",
            "locality": "Prabhadevi", "company": "Rustomjee Builders",
            "is_featured": True, "views_count": 623
        },
        {
            "title": "Rustomjee Azziano - 2 BHK for Rent Thane",
            "property_type": "flat", "listing_type": "rent",
            "price": 25000, "price_unit": "month", "bhk": 2,
            "area_sqft": 980, "carpet_area": 740,
            "floor_number": 8, "total_floors": 22, "age_years": 5,
            "furnished": "semi", "facing": "North",
            "description": "Semi-furnished 2 BHK for rent in Rustomjee Azziano, Majiwada, Thane. Includes wardrobes, modular kitchen, and geyser. Well-maintained gated community with excellent amenities. Close to Eastern Express Highway, TMC school, and Jupiter Hospital.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Rustomjee Azziano, Majiwada, Thane West",
            "locality": "Thane West", "company": "Rustomjee Builders",
            "is_featured": False, "views_count": 345
        },

        # ===== RUNWAL =====
        {
            "title": "Runwal Bliss - Spacious 3 BHK Kanjurmarg",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.95, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1350, "carpet_area": 1020,
            "floor_number": 20, "total_floors": 35, "age_years": 2,
            "furnished": "unfurnished", "facing": "East",
            "description": "Runwal Bliss in Kanjurmarg East - excellent value for a 3 BHK near LBS Marg. Integrated township with R City Mall access. Cross-ventilated layout with mountain views. Proximity to upcoming Metro Line 4 station. Well-connected to BKC via SCLR.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track"]',
            "address": "Runwal Bliss, LBS Marg, Kanjurmarg East",
            "locality": "Kanjurmarg", "company": "Runwal Developers",
            "is_featured": False, "views_count": 412
        },
        {
            "title": "Runwal Forests - 2 BHK with Forest View Kanjurmarg",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.45, "price_unit": "crore", "bhk": 2,
            "area_sqft": 980, "carpet_area": 740,
            "floor_number": 15, "total_floors": 40, "age_years": 1,
            "furnished": "unfurnished", "facing": "North",
            "description": "Brand new 2 BHK in Runwal Forests overlooking the beautiful Aarey forest. Fresh air and green views. 75+ amenities in 35,000 sqft clubhouse. Connected to upcoming Metro stations. Part of a mega township with over 5000 apartments.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track","CCTV","Rainwater Harvesting"]',
            "address": "Runwal Forests, LBS Marg, Kanjurmarg West",
            "locality": "Kanjurmarg", "company": "Runwal Developers",
            "is_featured": False, "views_count": 334
        },

        # ===== KALPATARU =====
        {
            "title": "Kalpataru Magnus - 3 BHK Bandra East",
            "property_type": "flat", "listing_type": "buy",
            "price": 4.8, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1900, "carpet_area": 1420,
            "floor_number": 25, "total_floors": 38, "age_years": 3,
            "furnished": "semi", "facing": "West",
            "description": "Kalpataru Magnus at BKC Annexe, Bandra East. Premium 3 BHK with stunning Mahim Bay and sea link views. Italian marble flooring, designer modular kitchen, VRV AC. Located adjacent to BKC - Mumbai's business hub. 2 minutes from Bandra station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Terrace","Garden","Jogging Track","CCTV","Intercom"]',
            "address": "Kalpataru Magnus, BKC Annexe, Bandra East",
            "locality": "Bandra", "company": "Kalpataru Ltd",
            "is_featured": True, "views_count": 567
        },
        {
            "title": "Kalpataru Starlight - 2 BHK Malad West",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.65, "price_unit": "crore", "bhk": 2,
            "area_sqft": 900, "carpet_area": 680,
            "floor_number": 12, "total_floors": 25, "age_years": 4,
            "furnished": "unfurnished", "facing": "East",
            "description": "Compact 2 BHK in Kalpataru Starlight, Malad West. Efficient layout with good ventilation. Society amenities include rooftop pool, party hall, and gym. Walking distance to Malad station and Inorbit Mall. Surrounded by reputed schools and hospitals.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Kalpataru Starlight, SV Road, Malad West",
            "locality": "Malad", "company": "Kalpataru Ltd",
            "is_featured": False, "views_count": 289
        },

        # ===== MAHINDRA LIFESPACES =====
        {
            "title": "Mahindra Alcove - 3 BHK with Garden in Chandivali",
            "property_type": "flat", "listing_type": "buy",
            "price": 2.65, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1500, "carpet_area": 1130,
            "floor_number": 6, "total_floors": 18, "age_years": 5,
            "furnished": "semi", "facing": "South",
            "description": "Mahindra Alcove in Chandivali offers a unique garden-facing 3 BHK apartment. IGBC Gold-certified green building. Spacious bedrooms with wardrobes, servant quarter, and 2 parking spaces. Located in a serene environment away from the main road. Easy access to Powai and MIDC Andheri.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Rainwater Harvesting","Vastu Compliant"]',
            "address": "Mahindra Alcove, Chandivali, Andheri East",
            "locality": "Andheri", "company": "Mahindra Lifespace Developers",
            "is_featured": False, "views_count": 367
        },
        {
            "title": "Mahindra Happinest - 1 BHK Kalyan",
            "property_type": "flat", "listing_type": "buy",
            "price": 38, "price_unit": "lakh", "bhk": 1,
            "area_sqft": 400, "carpet_area": 310,
            "floor_number": 5, "total_floors": 14, "age_years": 3,
            "furnished": "unfurnished", "facing": "East",
            "description": "Affordable 1 BHK in Mahindra Happinest, Kalyan. Part of an integrated township designed for comfortable living. Compact yet well-planned layout. Society has garden, play area, and community hall. Close to Kalyan station and market. Excellent for first-time buyers.",
            "amenities": '["Parking","Lift","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Mahindra Happinest, Kalyan West",
            "locality": "Kalyan", "company": "Mahindra Lifespace Developers",
            "is_featured": False, "views_count": 612
        },

        # ===== PIRAMAL REALTY =====
        {
            "title": "Piramal Mahalaxmi - Super Luxury 4 BHK South Mumbai",
            "property_type": "flat", "listing_type": "buy",
            "price": 15, "price_unit": "crore", "bhk": 4,
            "area_sqft": 3800, "carpet_area": 2900,
            "floor_number": 50, "total_floors": 60, "age_years": 1,
            "furnished": "semi", "facing": "West",
            "description": "Piramal Mahalaxmi - one of South Mumbai's tallest residential towers. This ultra-luxury 4 BHK on the 50th floor offers 270-degree views of the sea, racecourse, and city skyline. Designed by Pei Cobb Freed (architects of the Louvre Pyramid). Features include private lift lobby, Italian marble, Gaggenau kitchen, and spa bathrooms. 5-star hotel-style amenities.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Concierge","Spa","Terrace","Jogging Track","CCTV","Intercom","Vastu Compliant"]',
            "address": "Piramal Mahalaxmi, N.M. Joshi Marg, Lower Parel",
            "locality": "Lower Parel", "company": "Piramal Realty Pvt Ltd",
            "is_featured": True, "views_count": 934
        },
        {
            "title": "Piramal Vaikunth - 2 BHK in Thane East",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.2, "price_unit": "crore", "bhk": 2,
            "area_sqft": 920, "carpet_area": 700,
            "floor_number": 14, "total_floors": 30, "age_years": 2,
            "furnished": "unfurnished", "facing": "North",
            "description": "Piramal Vaikunth in Balkum, Thane - a thoughtfully designed 2 BHK with vastu-compliant layout. Part of a 32-acre township with temple, organic farm, and nature trail. Premium specifications by Piramal. Close to Thane station and Eastern Express Highway.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track","Rainwater Harvesting","Vastu Compliant"]',
            "address": "Piramal Vaikunth, Balkum, Thane",
            "locality": "Thane East", "company": "Piramal Realty Pvt Ltd",
            "is_featured": False, "views_count": 412
        },

        # ===== L&T REALTY =====
        {
            "title": "L&T Emerald Isle - Premium 3 BHK Powai",
            "property_type": "flat", "listing_type": "buy",
            "price": 3.5, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1680, "carpet_area": 1260,
            "floor_number": 28, "total_floors": 45, "age_years": 2,
            "furnished": "semi", "facing": "West",
            "description": "L&T Emerald Isle in Powai - engineered by L&T with impeccable quality. This 3 BHK offers lake and hill views from the 28th floor. Earthquake-resistant structure, aluminium formwork construction. Amenities include infinity pool, outdoor theatre, pet park, and co-working space. Walk to IIT Bombay campus.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","Children Play Area","Jogging Track","CCTV","Intercom","Rainwater Harvesting"]',
            "address": "L&T Emerald Isle, Powai",
            "locality": "Powai", "company": "L&T Realty Ltd",
            "is_featured": True, "views_count": 523
        },
        {
            "title": "L&T Seawoods Residences - 2 BHK Navi Mumbai",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.55, "price_unit": "crore", "bhk": 2,
            "area_sqft": 1050, "carpet_area": 790,
            "floor_number": 18, "total_floors": 32, "age_years": 3,
            "furnished": "unfurnished", "facing": "East",
            "description": "L&T Seawoods Residences in Nerul, Navi Mumbai. Connected to Seawoods Grand Central Mall via skybridge. 2 BHK with harbor views and sea breeze. Direct access to Seawoods station. Planned township with office spaces, retail, and entertainment.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden","CCTV","Intercom"]',
            "address": "L&T Seawoods Residences, Nerul, Navi Mumbai",
            "locality": "Nerul", "company": "L&T Realty Ltd",
            "is_featured": False, "views_count": 378
        },

        # ===== ADDITIONAL VARIETY =====
        {
            "title": "Luxury Warehouse Space for Lease in Bhiwandi",
            "property_type": "warehouse", "listing_type": "rent",
            "price": 500000, "price_unit": "month", "bhk": None,
            "area_sqft": 25000, "carpet_area": 22000,
            "floor_number": 0, "total_floors": 1, "age_years": 2,
            "furnished": "unfurnished", "facing": "North",
            "description": "Modern Grade-A warehouse facility on Bhiwandi-Nashik Highway. 25,000 sqft with 32 ft clear height, 6 loading docks, fire sprinkler system, and 24/7 security. Suitable for e-commerce, FMCG, or logistics companies. Highway connectivity to Mumbai and Pune.",
            "amenities": '["Parking","Security","Power Backup","Fire Safety","CCTV","Road Access","Water Supply","Electricity"]',
            "address": "Bhiwandi-Nashik Highway, Bhiwandi",
            "locality": "Bhiwandi", "company": "L&T Realty Ltd",
            "is_featured": False, "views_count": 145
        },
        {
            "title": "Retail Showroom Space in Bandra Linking Road",
            "property_type": "shop", "listing_type": "rent",
            "price": 350000, "price_unit": "month", "bhk": None,
            "area_sqft": 1200, "carpet_area": 1050,
            "floor_number": 0, "total_floors": 4, "age_years": 12,
            "furnished": "unfurnished", "facing": "South",
            "description": "Prime ground-floor retail space on Bandra's famous Linking Road - Mumbai's top fashion and shopping street. High street frontage with massive footfall. Suitable for fashion brands, lifestyle stores, or flagship retail outlets. Recently renovated with modern facade.",
            "amenities": '["Parking","Security","Power Backup","CCTV","Visitor Parking"]',
            "address": "Linking Road, Bandra West",
            "locality": "Bandra", "company": "Kalpataru Ltd",
            "is_featured": False, "views_count": 267
        },
        {
            "title": "Residential Plot in Kharghar Sector 35",
            "property_type": "plot", "listing_type": "buy",
            "price": 1.5, "price_unit": "crore", "bhk": None,
            "area_sqft": 5000, "carpet_area": None,
            "floor_number": None, "total_floors": None, "age_years": None,
            "furnished": "unfurnished", "facing": "West",
            "description": "Premium NA residential plot in Kharghar Sector 35. Flat terrain, clear title, ready for construction. Surrounded by developed residential societies. Near proposed metro station and Central Park. Hill views and excellent ventilation. One of the last available plots in prime Kharghar.",
            "amenities": '["Road Access","Water Supply","Electricity"]',
            "address": "Sector 35, Kharghar, Navi Mumbai",
            "locality": "Kharghar", "company": "Hiranandani Group",
            "is_featured": False, "views_count": 356
        },
        {
            "title": "Duplex Villa in Vile Parle West",
            "property_type": "villa", "listing_type": "buy",
            "price": 8.5, "price_unit": "crore", "bhk": 4,
            "area_sqft": 3500, "carpet_area": 2800,
            "floor_number": 0, "total_floors": 2, "age_years": 15,
            "furnished": "semi", "facing": "South",
            "description": "Rare standalone duplex villa in the upscale Irla locality of Vile Parle West. Ground + 1 floor with private garden, terrace, and parking for 3 cars. 4 bedrooms with attached bathrooms, servant quarter, and spacious living-dining area. Quiet lane, walking distance to Vile Parle station and Juhu Beach.",
            "amenities": '["Parking","Garden","Security","Power Backup","Terrace","CCTV","Vastu Compliant"]',
            "address": "Irla, Vile Parle West",
            "locality": "Vile Parle", "company": "Rustomjee Builders",
            "is_featured": True, "views_count": 478
        },
        {
            "title": "Furnished 1 BHK for Rent in Airoli",
            "property_type": "flat", "listing_type": "rent",
            "price": 16000, "price_unit": "month", "bhk": 1,
            "area_sqft": 550, "carpet_area": 420,
            "floor_number": 7, "total_floors": 12, "age_years": 6,
            "furnished": "fully", "facing": "East",
            "description": "Fully furnished 1 BHK in Airoli, Navi Mumbai. Includes AC, washing machine, fridge, microwave, and all furniture. Gated society with parking and security. 5-minute walk to Airoli station. Surrounded by IT parks - ideal for working professionals in Airoli-Ghansoli belt.",
            "amenities": '["Parking","Lift","Security","Power Backup","Garden"]',
            "address": "Sector 20, Airoli, Navi Mumbai",
            "locality": "Airoli", "company": "Runwal Developers",
            "is_featured": False, "views_count": 534
        },
        {
            "title": "3 BHK Sea-Facing in Colaba",
            "property_type": "flat", "listing_type": "buy",
            "price": 18, "price_unit": "crore", "bhk": 3,
            "area_sqft": 2500, "carpet_area": 1900,
            "floor_number": 12, "total_floors": 14, "age_years": 25,
            "furnished": "fully", "facing": "West",
            "description": "Iconic sea-facing 3 BHK in a heritage building on Colaba Causeway. Breathtaking Arabian Sea and Gateway of India views. High ceilings, wooden flooring, and colonial-era charm with modern renovations. Walking distance to Taj Mahal Palace, Colaba Causeway market, and Mumbai's finest restaurants.",
            "amenities": '["Parking","Lift","Security","Power Backup","CCTV"]',
            "address": "Colaba Causeway, Colaba",
            "locality": "Colaba", "company": "Piramal Realty Pvt Ltd",
            "is_featured": True, "views_count": 1023
        },
        {
            "title": "2 BHK Flat for Rent near Ghatkopar Metro",
            "property_type": "flat", "listing_type": "rent",
            "price": 30000, "price_unit": "month", "bhk": 2,
            "area_sqft": 850, "carpet_area": 640,
            "floor_number": 4, "total_floors": 7, "age_years": 10,
            "furnished": "semi", "facing": "North",
            "description": "Semi-furnished 2 BHK just 2 minutes from Ghatkopar Metro station. Includes modular kitchen, wardrobes, and geysers. Quiet residential area with good society maintenance. Near R-City Mall, Ghatkopar station, and BEST bus routes. Ideal for families working in BKC or Powai.",
            "amenities": '["Parking","Lift","Security","Power Backup"]',
            "address": "Near Ghatkopar Metro, Ghatkopar West",
            "locality": "Ghatkopar", "company": "Godrej Properties Ltd",
            "is_featured": False, "views_count": 445
        },
        {
            "title": "Co-Working Office Space in Fort",
            "property_type": "office", "listing_type": "rent",
            "price": 85000, "price_unit": "month", "bhk": None,
            "area_sqft": 1500, "carpet_area": 1200,
            "floor_number": 5, "total_floors": 8, "age_years": 50,
            "furnished": "fully", "facing": "East",
            "description": "Charming office space in a restored heritage building in Fort, South Mumbai. Exposed brick walls, wooden beams, and modern amenities. Plug-and-play for 25 people with meeting room and pantry. Walking distance to CST station, Bombay High Court, and RBI. Perfect for law firms, startups, and creative agencies.",
            "amenities": '["Lift","Security","Power Backup","Fire Safety","Cafeteria","CCTV"]',
            "address": "DN Road, Fort, Mumbai",
            "locality": "Fort", "company": "Mahindra Lifespace Developers",
            "is_featured": False, "views_count": 234
        },
        {
            "title": "3 BHK with Servant Room in Kandivali West",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.75, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1200, "carpet_area": 910,
            "floor_number": 10, "total_floors": 20, "age_years": 3,
            "furnished": "unfurnished", "facing": "West",
            "description": "Well-designed 3 BHK with servant room in a reputed Kandivali West society. All bedrooms with attached bathrooms, spacious living area, and dry balcony. Located near Mahavir Nagar with excellent school and hospital access. Walking distance to Kandivali station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area","CCTV"]',
            "address": "Mahavir Nagar, Kandivali West",
            "locality": "Kandivali", "company": "Kalpataru Ltd",
            "is_featured": False, "views_count": 312
        },
        {
            "title": "Penthouse 5 BHK with Private Pool in Malabar Hill",
            "property_type": "flat", "listing_type": "buy",
            "price": 45, "price_unit": "crore", "bhk": 5,
            "area_sqft": 6500, "carpet_area": 5200,
            "floor_number": 20, "total_floors": 20, "age_years": 3,
            "furnished": "fully", "facing": "West",
            "description": "Ultra-luxury penthouse on Malabar Hill - Mumbai's most exclusive neighborhood. Sprawling 6500 sqft with private infinity pool and 360-degree views of the Arabian Sea, Marine Drive, and Hanging Gardens. 5 bedrooms, each with en-suite bathroom and walk-in closet. Home theatre, wine cellar, staff quarters. Triple-height living area. Truly one of Mumbai's finest homes.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Concierge","Spa","Terrace","CCTV","Intercom","Vastu Compliant"]',
            "address": "Malabar Hill, Mumbai",
            "locality": "Malabar Hill", "company": "Lodha Group",
            "is_featured": True, "views_count": 1567
        },
    ]

    count = 0
    for p in properties_data:
        company = p.pop("company")
        locality_name = p.pop("locality")
        user_id = builder_users.get(company)
        locality_id = loc_map.get(locality_name)

        base_slug = slugify(p["title"])
        slug = base_slug
        counter = 1
        while db.session.query(Property).filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        prop = Property(
            slug=slug,
            locality_id=locality_id,
            user_id=user_id,
            is_approved=True,
            status="active",
            **p
        )
        db.session.add(prop)
        count += 1

    db.session.commit()
    print(f"Seeded {count} builder properties from 10 top Mumbai builders.")
