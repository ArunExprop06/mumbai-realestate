from flask import Blueprint, request, jsonify
from extensions import db
from models import Property, PropertyImage, Locality, User, EnquiryLog
from sqlalchemy import func, or_

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def serialize_property_card(prop):
    """Minimal property data for list/card views."""
    primary = prop.primary_image
    locality = prop.locality
    return {
        'id': prop.id,
        'title': prop.title,
        'slug': prop.slug,
        'property_type': prop.property_type,
        'listing_type': prop.listing_type,
        'price': prop.price,
        'price_unit': prop.price_unit,
        'formatted_price': prop.formatted_price,
        'bhk': prop.bhk,
        'area_sqft': prop.area_sqft,
        'carpet_area': prop.carpet_area,
        'furnished': prop.furnished,
        'locality': locality.name if locality else None,
        'zone': locality.zone if locality else None,
        'locality_id': prop.locality_id,
        'image': f'/static/uploads/properties/thumbs/{primary.filename}' if primary else None,
        'is_featured': prop.is_featured,
        'views_count': prop.views_count,
        'created_at': prop.created_at.isoformat() if prop.created_at else None,
    }


def serialize_property_detail(prop):
    """Full property data for detail view."""
    card = serialize_property_card(prop)
    owner = prop.owner
    images = prop.all_images
    card.update({
        'floor_number': prop.floor_number,
        'total_floors': prop.total_floors,
        'age_years': prop.age_years,
        'facing': prop.facing,
        'description': prop.description,
        'amenities': prop.amenities,
        'address': prop.address,
        'status': prop.status,
        'images': [
            {
                'id': img.id,
                'url': f'/static/uploads/properties/{img.filename}',
                'thumb': f'/static/uploads/properties/thumbs/{img.filename}',
                'is_primary': img.is_primary,
            }
            for img in images
        ],
        'agent': {
            'id': owner.id,
            'name': owner.name,
            'phone': owner.phone,
            'company': owner.company,
            'photo': f'/static/uploads/users/{owner.photo}' if owner.photo else None,
        } if owner else None,
    })
    return card


def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


@api_bp.after_request
def after_request(response):
    return add_cors(response)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@api_bp.route('/home', methods=['GET'])
def home():
    """Home screen data: featured, zones, property types, stats."""
    # Featured properties
    featured = db.session.query(Property).filter_by(
        is_featured=True, is_approved=True, status='active'
    ).order_by(Property.created_at.desc()).limit(10).all()

    # Zones with counts
    zone_data = db.session.query(
        Locality.zone, func.count(Property.id)
    ).outerjoin(Property, (Property.locality_id == Locality.id) & (Property.status == 'active') & (Property.is_approved == True)).group_by(
        Locality.zone
    ).all()
    zones = [{'name': z, 'property_count': c} for z, c in zone_data]

    # Property types with counts
    type_data = db.session.query(
        Property.property_type, func.count(Property.id)
    ).filter_by(status='active', is_approved=True).group_by(
        Property.property_type
    ).all()
    property_types = [{'name': t, 'count': c} for t, c in type_data]

    # Stats
    total = db.session.query(func.count(Property.id)).filter_by(
        status='active', is_approved=True
    ).scalar() or 0
    buy_count = db.session.query(func.count(Property.id)).filter_by(
        status='active', is_approved=True, listing_type='buy'
    ).scalar() or 0
    rent_count = db.session.query(func.count(Property.id)).filter_by(
        status='active', is_approved=True, listing_type='rent'
    ).scalar() or 0
    locality_count = db.session.query(func.count(Locality.id)).scalar() or 0

    return jsonify({
        'featured': [serialize_property_card(p) for p in featured],
        'zones': zones,
        'property_types': property_types,
        'stats': {
            'total_properties': total,
            'for_sale': buy_count,
            'for_rent': rent_count,
            'localities': locality_count,
        }
    })


@api_bp.route('/properties', methods=['GET'])
def properties_list():
    """Paginated property list with filters."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    per_page = min(per_page, 50)

    q = db.session.query(Property).filter_by(status='active', is_approved=True)

    # Filters
    listing_type = request.args.get('listing_type')
    if listing_type:
        q = q.filter(Property.listing_type == listing_type)

    property_type = request.args.get('property_type')
    if property_type:
        q = q.filter(Property.property_type == property_type)

    locality_id = request.args.get('locality')
    if locality_id:
        q = q.filter(Property.locality_id == int(locality_id))

    zone = request.args.get('zone')
    if zone:
        locality_ids = [l.id for l in db.session.query(Locality.id).filter_by(zone=zone).all()]
        if locality_ids:
            q = q.filter(Property.locality_id.in_(locality_ids))

    bhk = request.args.get('bhk')
    if bhk:
        bhk_list = [int(b) for b in bhk.split(',') if b.isdigit()]
        if bhk_list:
            q = q.filter(Property.bhk.in_(bhk_list))

    furnished = request.args.get('furnished')
    if furnished:
        q = q.filter(Property.furnished == furnished)

    min_price = request.args.get('min_price', type=float)
    if min_price is not None:
        q = q.filter(Property.price >= min_price)

    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        q = q.filter(Property.price <= max_price)

    search = request.args.get('q')
    if search:
        pattern = f'%{search}%'
        q = q.filter(or_(
            Property.title.ilike(pattern),
            Property.address.ilike(pattern),
            Property.description.ilike(pattern),
        ))

    # Sort
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        q = q.order_by(Property.price.asc())
    elif sort == 'price_high':
        q = q.order_by(Property.price.desc())
    elif sort == 'area':
        q = q.order_by(Property.area_sqft.desc().nullslast())
    else:
        q = q.order_by(Property.created_at.desc())

    total = q.count()
    properties = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'properties': [serialize_property_card(p) for p in properties],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    })


@api_bp.route('/properties/<int:prop_id>', methods=['GET'])
def property_detail(prop_id):
    """Full property detail."""
    prop = db.session.get(Property, prop_id)
    if not prop or prop.status == 'inactive':
        return jsonify({'error': 'Property not found'}), 404

    # Increment views
    prop.views_count = (prop.views_count or 0) + 1
    db.session.commit()

    # Similar properties (same locality or type, exclude self)
    similar_q = db.session.query(Property).filter(
        Property.id != prop.id,
        Property.status == 'active',
        Property.is_approved == True,
        or_(
            Property.locality_id == prop.locality_id,
            Property.property_type == prop.property_type,
        )
    ).order_by(Property.views_count.desc()).limit(6).all()

    return jsonify({
        'property': serialize_property_detail(prop),
        'similar': [serialize_property_card(p) for p in similar_q],
    })


@api_bp.route('/localities', methods=['GET'])
def localities():
    """All localities grouped by zone with property counts."""
    results = db.session.query(
        Locality,
        func.count(Property.id).label('count')
    ).outerjoin(
        Property,
        (Property.locality_id == Locality.id) & (Property.status == 'active') & (Property.is_approved == True)
    ).group_by(Locality.id).order_by(Locality.zone, Locality.name).all()

    zones = {}
    for loc, count in results:
        if loc.zone not in zones:
            zones[loc.zone] = []
        zones[loc.zone].append({
            'id': loc.id,
            'name': loc.name,
            'slug': loc.slug,
            'property_count': count,
        })

    return jsonify({'zones': zones})


@api_bp.route('/localities/<int:loc_id>/properties', methods=['GET'])
def locality_properties(loc_id):
    """Properties in a locality (paginated)."""
    locality = db.session.get(Locality, loc_id)
    if not locality:
        return jsonify({'error': 'Locality not found'}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    per_page = min(per_page, 50)

    q = db.session.query(Property).filter_by(
        locality_id=loc_id, status='active', is_approved=True
    ).order_by(Property.created_at.desc())

    total = q.count()
    properties = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        'locality': {
            'id': locality.id,
            'name': locality.name,
            'zone': locality.zone,
            'slug': locality.slug,
        },
        'properties': [serialize_property_card(p) for p in properties],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    })


@api_bp.route('/search/suggestions', methods=['GET'])
def search_suggestions():
    """Autocomplete: top 5 localities + 5 properties matching query."""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({'localities': [], 'properties': []})

    pattern = f'%{query}%'

    locs = db.session.query(Locality).filter(
        Locality.name.ilike(pattern)
    ).limit(5).all()

    props = db.session.query(Property).filter(
        Property.status == 'active',
        Property.is_approved == True,
        or_(
            Property.title.ilike(pattern),
            Property.address.ilike(pattern),
        )
    ).limit(5).all()

    return jsonify({
        'localities': [
            {'id': l.id, 'name': l.name, 'zone': l.zone}
            for l in locs
        ],
        'properties': [serialize_property_card(p) for p in props],
    })


@api_bp.route('/enquiry', methods=['POST'])
def log_enquiry():
    """Log phone/WhatsApp click."""
    data = request.get_json(silent=True) or {}
    property_id = data.get('property_id')
    action = data.get('action')

    if not property_id or action not in ('phone_click', 'whatsapp_click'):
        return jsonify({'error': 'Invalid data'}), 400

    log = EnquiryLog(
        property_id=property_id,
        action=action,
        visitor_ip=request.remote_addr,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'status': 'ok'})
