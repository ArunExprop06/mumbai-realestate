from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import func
from extensions import db
from models import Property, Locality, User, EnquiryLog

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def home():
    featured = db.session.query(Property).filter_by(
        is_approved=True, status='active', is_featured=True
    ).order_by(Property.created_at.desc()).limit(8).all()

    localities = db.session.query(Locality).all()
    zones = {}
    for loc in localities:
        zones.setdefault(loc.zone, []).append(loc)

    # Stats
    total_properties = db.session.query(Property).filter_by(is_approved=True, status='active').count()
    total_agents = db.session.query(User).filter(User.role.in_(['agent', 'broker']), User.is_approved == True).count()
    total_localities = db.session.query(Locality).count()

    return render_template('public/home.html',
                           featured=featured,
                           zones=zones,
                           total_properties=total_properties,
                           total_agents=total_agents,
                           total_localities=total_localities)


@public_bp.route('/properties')
def properties():
    page = request.args.get('page', 1, type=int)
    per_page = 12

    query = db.session.query(Property).filter_by(is_approved=True, status='active')

    # Filters
    listing_type = request.args.get('listing_type')
    if listing_type in ('buy', 'rent'):
        query = query.filter_by(listing_type=listing_type)

    property_type = request.args.get('property_type')
    if property_type:
        query = query.filter_by(property_type=property_type)

    locality_id = request.args.get('locality')
    if locality_id:
        query = query.filter_by(locality_id=locality_id)

    zone = request.args.get('zone')
    if zone:
        loc_ids = [l.id for l in db.session.query(Locality).filter_by(zone=zone).all()]
        if loc_ids:
            query = query.filter(Property.locality_id.in_(loc_ids))

    bhk = request.args.get('bhk')
    if bhk:
        bhk_list = [int(b) for b in bhk.split(',') if b.isdigit()]
        if bhk_list:
            query = query.filter(Property.bhk.in_(bhk_list))

    furnished = request.args.get('furnished')
    if furnished:
        query = query.filter_by(furnished=furnished)

    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Property.price >= min_price)
    if max_price is not None:
        query = query.filter(Property.price <= max_price)

    search_q = request.args.get('q', '').strip()
    if search_q:
        search_term = f"%{search_q}%"
        query = query.filter(
            db.or_(
                Property.title.ilike(search_term),
                Property.description.ilike(search_term),
                Property.address.ilike(search_term)
            )
        )

    # Sort
    sort = request.args.get('sort', 'newest')
    if sort == 'price_low':
        query = query.order_by(Property.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Property.price.desc())
    elif sort == 'area':
        query = query.order_by(Property.area_sqft.desc())
    else:
        query = query.order_by(Property.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    localities = db.session.query(Locality).order_by(Locality.zone, Locality.name).all()

    return render_template('public/properties.html',
                           properties=pagination.items,
                           pagination=pagination,
                           localities=localities,
                           filters=request.args)


@public_bp.route('/property/<slug>')
def property_detail(slug):
    prop = db.session.query(Property).filter_by(slug=slug).first_or_404()

    # Increment view count
    prop.views_count = (prop.views_count or 0) + 1
    db.session.commit()

    # Similar properties
    similar = db.session.query(Property).filter(
        Property.id != prop.id,
        Property.is_approved == True,
        Property.status == 'active',
        db.or_(
            Property.locality_id == prop.locality_id,
            Property.property_type == prop.property_type
        )
    ).limit(4).all()

    return render_template('public/property_detail.html', property=prop, similar=similar)


@public_bp.route('/locality/<slug>')
def locality_detail(slug):
    locality = db.session.query(Locality).filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = db.session.query(Property).filter_by(
        locality_id=locality.id, is_approved=True, status='active'
    ).order_by(Property.created_at.desc()).paginate(page=page, per_page=12, error_out=False)

    return render_template('public/locality.html',
                           locality=locality,
                           properties=pagination.items,
                           pagination=pagination)


@public_bp.route('/api/enquiry', methods=['POST'])
def log_enquiry():
    data = request.get_json()
    log = EnquiryLog(
        property_id=data.get('property_id'),
        action=data.get('action'),
        visitor_ip=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
    return jsonify({'status': 'ok'})


@public_bp.route('/api/localities')
def api_localities():
    localities = db.session.query(Locality).order_by(Locality.zone, Locality.name).all()
    return jsonify([{'id': l.id, 'name': l.name, 'zone': l.zone} for l in localities])
