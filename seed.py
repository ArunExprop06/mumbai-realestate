from extensions import db
from models import Locality, User
import re


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text


LOCALITIES = {
    "South Mumbai": [
        "Colaba", "Churchgate", "Marine Lines", "Nariman Point", "Fort",
        "Malabar Hill", "Worli", "Lower Parel", "Prabhadevi", "Dadar"
    ],
    "Western Suburbs": [
        "Bandra", "Khar", "Santacruz", "Vile Parle", "Andheri",
        "Jogeshwari", "Goregaon", "Malad", "Kandivali", "Borivali", "Dahisar"
    ],
    "Central Suburbs": [
        "Kurla", "Ghatkopar", "Vikhroli", "Kanjurmarg", "Bhandup",
        "Mulund", "Powai", "Chembur"
    ],
    "Harbour Line": [
        "Wadala", "Sion", "Mankhurd", "Vashi", "Nerul",
        "Belapur", "Kharghar", "Panvel"
    ],
    "Thane": [
        "Thane West", "Thane East", "Ghodbunder Road", "Kalyan",
        "Dombivli", "Bhiwandi"
    ],
    "Navi Mumbai": [
        "Vashi", "Nerul", "Belapur", "Kharghar", "Panvel",
        "Airoli", "Ghansoli", "Kopar Khairane"
    ]
}


def seed_localities():
    if db.session.query(Locality).count() > 0:
        return
    for zone, names in LOCALITIES.items():
        for name in names:
            slug = slugify(f"{name}-{zone}")
            loc = Locality(name=name, zone=zone, slug=slug)
            db.session.add(loc)
    db.session.commit()
    print(f"Seeded {db.session.query(Locality).count()} localities.")


def seed_admin():
    admin = db.session.query(User).filter_by(email='admin@exproperty.com').first()
    if admin:
        return
    admin = User(
        name='Admin',
        email='admin@exproperty.com',
        phone='9999999999',
        role='admin',
        is_approved=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created: admin@exproperty.com / admin123")


def seed_sample_properties():
    """Seed sample properties for demonstration."""
    from models import Property, PropertyImage

    if db.session.query(Property).count() > 0:
        return

    admin = db.session.query(User).filter_by(role='admin').first()
    if not admin:
        return

    # Create a sample agent
    agent = db.session.query(User).filter_by(email='agent@example.com').first()
    if not agent:
        agent = User(
            name='Rahul Sharma',
            email='agent@example.com',
            phone='9876543210',
            role='agent',
            company='Sharma Properties',
            rera_number='RERA12345',
            is_approved=True
        )
        agent.set_password('agent123')
        db.session.add(agent)
        db.session.commit()

    localities = db.session.query(Locality).all()
    loc_map = {l.name: l.id for l in localities}

    sample_properties = [
        {
            "title": "Luxurious 3 BHK Sea-View Flat in Worli",
            "slug": "luxurious-3bhk-sea-view-flat-worli",
            "property_type": "flat", "listing_type": "buy",
            "price": 4.5, "price_unit": "crore", "bhk": 3,
            "area_sqft": 1800, "carpet_area": 1350,
            "floor_number": 22, "total_floors": 40, "age_years": 2,
            "furnished": "semi", "facing": "West",
            "description": "Stunning sea-view apartment in one of Worli's premium towers. Features modern interiors, Italian marble flooring, modular kitchen, and panoramic views of the Arabian Sea. Located near Worli Sea Face with excellent connectivity.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House"]',
            "address": "Worli Sea Face Road, Worli",
            "locality_id": loc_map.get("Worli"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 245
        },
        {
            "title": "Spacious 2 BHK in Andheri West",
            "slug": "spacious-2bhk-andheri-west",
            "property_type": "flat", "listing_type": "buy",
            "price": 1.85, "price_unit": "crore", "bhk": 2,
            "area_sqft": 1050, "carpet_area": 780,
            "floor_number": 8, "total_floors": 20, "age_years": 5,
            "furnished": "semi", "facing": "East",
            "description": "Well-maintained 2 BHK in a prime Andheri West location. Walking distance to Andheri station and DN Nagar metro. Surrounded by schools, hospitals, and shopping centres.",
            "amenities": '["Parking","Lift","Security","Power Backup","Garden"]',
            "address": "Near DN Nagar Metro, Andheri West",
            "locality_id": loc_map.get("Andheri"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 180
        },
        {
            "title": "Modern 1 BHK for Rent in Powai",
            "slug": "modern-1bhk-rent-powai",
            "property_type": "flat", "listing_type": "rent",
            "price": 35000, "price_unit": "month", "bhk": 1,
            "area_sqft": 650, "carpet_area": 500,
            "floor_number": 12, "total_floors": 25, "age_years": 3,
            "furnished": "fully", "facing": "North",
            "description": "Fully furnished 1 BHK in Powai's Hiranandani Gardens. Modern interiors with AC, washing machine, and modular kitchen. Lake-view from balcony. Perfect for working professionals.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Garden"]',
            "address": "Hiranandani Gardens, Powai",
            "locality_id": loc_map.get("Powai"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 320
        },
        {
            "title": "Premium Villa in Bandra West",
            "slug": "premium-villa-bandra-west",
            "property_type": "villa", "listing_type": "buy",
            "price": 25, "price_unit": "crore", "bhk": 5,
            "area_sqft": 5000, "carpet_area": 4200,
            "floor_number": 0, "total_floors": 3, "age_years": 10,
            "furnished": "fully", "facing": "South",
            "description": "Iconic standalone villa in the heart of Bandra West. Spread over 5000 sqft with private garden, terrace, and parking for 4 cars. Walking distance to Bandstand, Carter Road, and Linking Road.",
            "amenities": '["Parking","Garden","Security","Power Backup","Terrace"]',
            "address": "Off Carter Road, Bandra West",
            "locality_id": loc_map.get("Bandra"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 412
        },
        {
            "title": "Commercial Office Space in Lower Parel",
            "slug": "commercial-office-lower-parel",
            "property_type": "office", "listing_type": "rent",
            "price": 150000, "price_unit": "month", "bhk": None,
            "area_sqft": 2500, "carpet_area": 2000,
            "floor_number": 15, "total_floors": 30, "age_years": 1,
            "furnished": "fully", "facing": "West",
            "description": "Premium office space in Lower Parel's business district. Plug-and-play setup with 40 workstations, 2 cabins, conference room, and pantry. Located in a Grade-A commercial tower with excellent Metro connectivity.",
            "amenities": '["Parking","Lift","Security","Power Backup","Fire Safety","Cafeteria"]',
            "address": "Senapati Bapat Marg, Lower Parel",
            "locality_id": loc_map.get("Lower Parel"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 156
        },
        {
            "title": "Affordable 1 BHK in Kharghar",
            "slug": "affordable-1bhk-kharghar",
            "property_type": "flat", "listing_type": "buy",
            "price": 55, "price_unit": "lakh", "bhk": 1,
            "area_sqft": 550, "carpet_area": 420,
            "floor_number": 4, "total_floors": 7, "age_years": 8,
            "furnished": "unfurnished", "facing": "East",
            "description": "Budget-friendly 1 BHK in Kharghar Sector 20. Close to railway station, schools, and markets. Ideal for first-time buyers or investment. Society with all basic amenities.",
            "amenities": '["Parking","Lift","Security","Garden"]',
            "address": "Sector 20, Kharghar",
            "locality_id": loc_map.get("Kharghar"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 95
        },
        {
            "title": "2 BHK Flat for Rent in Thane West",
            "slug": "2bhk-flat-rent-thane-west",
            "property_type": "flat", "listing_type": "rent",
            "price": 22000, "price_unit": "month", "bhk": 2,
            "area_sqft": 900, "carpet_area": 680,
            "floor_number": 6, "total_floors": 14, "age_years": 4,
            "furnished": "semi", "facing": "North",
            "description": "Semi-furnished 2 BHK in Thane's Ghodbunder Road. Gated community with ample amenities. Near schools, malls, and Thane station. Ideal for families.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area"]',
            "address": "Ghodbunder Road, Thane West",
            "locality_id": loc_map.get("Thane West"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 134
        },
        {
            "title": "Retail Shop in Dadar East",
            "slug": "retail-shop-dadar-east",
            "property_type": "shop", "listing_type": "buy",
            "price": 2.5, "price_unit": "crore", "bhk": None,
            "area_sqft": 400, "carpet_area": 350,
            "floor_number": 0, "total_floors": 5, "age_years": 15,
            "furnished": "unfurnished", "facing": "South",
            "description": "Prime ground-floor retail shop on a main road in Dadar East. High footfall area near Dadar station. Suitable for showroom, retail outlet, or restaurant.",
            "amenities": '["Parking","Security","Power Backup"]',
            "address": "Near Dadar Station, Dadar East",
            "locality_id": loc_map.get("Dadar"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 78
        },
        {
            "title": "3 BHK Penthouse in Goregaon East",
            "slug": "3bhk-penthouse-goregaon-east",
            "property_type": "flat", "listing_type": "buy",
            "price": 3.2, "price_unit": "crore", "bhk": 3,
            "area_sqft": 2200, "carpet_area": 1700,
            "floor_number": 30, "total_floors": 30, "age_years": 1,
            "furnished": "semi", "facing": "West",
            "description": "Brand new penthouse in Goregaon's premium Oberoi complex. Stunning city skyline views, private terrace, and world-class amenities. Close to Film City, Western Express Highway, and Goregaon station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Club House","Terrace","Jogging Track"]',
            "address": "Oberoi Commerz, Goregaon East",
            "locality_id": loc_map.get("Goregaon"),
            "is_featured": True, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 267
        },
        {
            "title": "Plot for Sale in Panvel",
            "slug": "plot-for-sale-panvel",
            "property_type": "plot", "listing_type": "buy",
            "price": 80, "price_unit": "lakh", "bhk": None,
            "area_sqft": 2400, "carpet_area": None,
            "floor_number": None, "total_floors": None, "age_years": None,
            "furnished": "unfurnished", "facing": "East",
            "description": "Residential NA plot in Panvel near upcoming Navi Mumbai International Airport. Clear title, ready for construction. Excellent investment opportunity with upcoming infrastructure projects.",
            "amenities": '["Road Access","Water Supply","Electricity"]',
            "address": "Near NMIA, Panvel",
            "locality_id": loc_map.get("Panvel"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 189
        },
        {
            "title": "Furnished Studio in Malad West",
            "slug": "furnished-studio-malad-west",
            "property_type": "flat", "listing_type": "rent",
            "price": 18000, "price_unit": "month", "bhk": 1,
            "area_sqft": 350, "carpet_area": 280,
            "floor_number": 3, "total_floors": 10, "age_years": 6,
            "furnished": "fully", "facing": "North",
            "description": "Compact fully furnished studio apartment near Malad station. Ideal for bachelors or working professionals. Includes AC, bed, wardrobe, and kitchen setup.",
            "amenities": '["Lift","Security","Power Backup"]',
            "address": "Near Malad Station, Malad West",
            "locality_id": loc_map.get("Malad"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 203
        },
        {
            "title": "4 BHK in Mulund East",
            "slug": "4bhk-mulund-east",
            "property_type": "flat", "listing_type": "buy",
            "price": 2.1, "price_unit": "crore", "bhk": 4,
            "area_sqft": 1600, "carpet_area": 1250,
            "floor_number": 10, "total_floors": 18, "age_years": 7,
            "furnished": "semi", "facing": "East",
            "description": "Spacious 4 BHK apartment in a premium Mulund society. Mountain views, cross ventilation, and vastu-compliant layout. Close to schools, hospitals, and Mulund station.",
            "amenities": '["Parking","Lift","Gym","Swimming Pool","Security","Power Backup","Garden","Children Play Area"]',
            "address": "LBS Marg, Mulund East",
            "locality_id": loc_map.get("Mulund"),
            "is_featured": False, "is_approved": True, "status": "active",
            "user_id": agent.id, "views_count": 112
        },
    ]

    for p_data in sample_properties:
        prop = Property(**p_data)
        db.session.add(prop)

    db.session.commit()
    print(f"Seeded {len(sample_properties)} sample properties.")


def seed_all():
    seed_localities()
    seed_admin()
    seed_sample_properties()
