import io
import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Property, PropertyImage, User, Locality, EnquiryLog
from helpers import slugify
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def dashboard():
    total_properties = db.session.query(Property).count()
    pending_properties = db.session.query(Property).filter_by(is_approved=False).count()
    total_agents = db.session.query(User).filter(User.role.in_(['agent', 'broker'])).count()
    pending_agents = db.session.query(User).filter_by(is_approved=False).filter(
        User.role.in_(['agent', 'broker'])
    ).count()
    total_enquiries = db.session.query(EnquiryLog).count()
    phone_clicks = db.session.query(EnquiryLog).filter_by(action='phone_click').count()
    whatsapp_clicks = db.session.query(EnquiryLog).filter_by(action='whatsapp_click').count()

    recent_properties = db.session.query(Property).order_by(
        Property.created_at.desc()
    ).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_properties=total_properties,
                           pending_properties=pending_properties,
                           total_agents=total_agents,
                           pending_agents=pending_agents,
                           total_enquiries=total_enquiries,
                           phone_clicks=phone_clicks,
                           whatsapp_clicks=whatsapp_clicks,
                           recent_properties=recent_properties)


@admin_bp.route('/properties')
@admin_required
def manage_properties():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    approval_filter = request.args.get('approval', '')

    query = db.session.query(Property)
    if status_filter:
        query = query.filter_by(status=status_filter)
    if approval_filter == 'pending':
        query = query.filter_by(is_approved=False)
    elif approval_filter == 'approved':
        query = query.filter_by(is_approved=True)

    pagination = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/properties.html',
                           properties=pagination.items,
                           pagination=pagination)


@admin_bp.route('/property/approve/<int:id>', methods=['POST'])
@admin_required
def approve_property(id):
    prop = db.session.get(Property, id)
    if prop:
        prop.is_approved = True
        db.session.commit()
        flash(f'Property "{prop.title}" approved.', 'success')
    return redirect(request.referrer or url_for('admin.manage_properties'))


@admin_bp.route('/property/reject/<int:id>', methods=['POST'])
@admin_required
def reject_property(id):
    prop = db.session.get(Property, id)
    if prop:
        prop.is_approved = False
        prop.status = 'inactive'
        db.session.commit()
        flash(f'Property "{prop.title}" rejected.', 'warning')
    return redirect(request.referrer or url_for('admin.manage_properties'))


@admin_bp.route('/property/feature/<int:id>', methods=['POST'])
@admin_required
def toggle_feature(id):
    prop = db.session.get(Property, id)
    if prop:
        prop.is_featured = not prop.is_featured
        db.session.commit()
        status = 'featured' if prop.is_featured else 'unfeatured'
        flash(f'Property "{prop.title}" {status}.', 'success')
    return redirect(request.referrer or url_for('admin.manage_properties'))


@admin_bp.route('/property/delete/<int:id>', methods=['POST'])
@admin_required
def delete_property(id):
    prop = db.session.get(Property, id)
    if prop:
        db.session.delete(prop)
        db.session.commit()
        flash('Property deleted.', 'success')
    return redirect(url_for('admin.manage_properties'))


@admin_bp.route('/users')
@admin_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    role_filter = request.args.get('role', '')
    query = db.session.query(User).filter(User.role != 'admin')
    if role_filter:
        query = query.filter_by(role=role_filter)
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html',
                           users=pagination.items,
                           pagination=pagination)


@admin_bp.route('/user/approve/<int:id>', methods=['POST'])
@admin_required
def approve_user(id):
    user = db.session.get(User, id)
    if user:
        user.is_approved = True
        db.session.commit()
        flash(f'User "{user.name}" approved.', 'success')
    return redirect(request.referrer or url_for('admin.manage_users'))


@admin_bp.route('/user/suspend/<int:id>', methods=['POST'])
@admin_required
def suspend_user(id):
    user = db.session.get(User, id)
    if user:
        user.is_approved = False
        db.session.commit()
        flash(f'User "{user.name}" suspended.', 'warning')
    return redirect(request.referrer or url_for('admin.manage_users'))


@admin_bp.route('/user/promote/<int:id>', methods=['POST'])
@admin_required
def promote_user(id):
    user = db.session.get(User, id)
    if user:
        user.role = 'admin'
        user.is_approved = True
        db.session.commit()
        flash(f'User "{user.name}" promoted to admin.', 'success')
    return redirect(request.referrer or url_for('admin.manage_users'))


@admin_bp.route('/bulk-upload', methods=['GET', 'POST'])
@admin_required
def bulk_upload():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename:
            flash('Please select a file.', 'danger')
            return redirect(url_for('admin.bulk_upload'))

        ext = file.filename.rsplit('.', 1)[-1].lower()
        if ext not in ('csv', 'xlsx', 'xls'):
            flash('Please upload a CSV or Excel file.', 'danger')
            return redirect(url_for('admin.bulk_upload'))

        try:
            if ext == 'csv':
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            required_cols = ['title', 'property_type', 'listing_type', 'price']
            missing = [c for c in required_cols if c not in df.columns]
            if missing:
                flash(f'Missing required columns: {", ".join(missing)}', 'danger')
                return redirect(url_for('admin.bulk_upload'))

            count = 0
            for _, row in df.iterrows():
                title = str(row.get('title', '')).strip()
                if not title:
                    continue

                base_slug = slugify(title)
                slug = base_slug
                counter = 1
                while db.session.query(Property).filter_by(slug=slug).first():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                locality_id = None
                locality_name = str(row.get('locality', '')).strip()
                if locality_name:
                    loc = db.session.query(Locality).filter(
                        Locality.name.ilike(locality_name)
                    ).first()
                    if loc:
                        locality_id = loc.id

                price_unit = str(row.get('price_unit', 'lakh')).strip().lower()
                if price_unit not in ('lakh', 'crore', 'month'):
                    price_unit = 'lakh'

                prop = Property(
                    title=title,
                    slug=slug,
                    property_type=str(row.get('property_type', 'flat')).strip().lower(),
                    listing_type=str(row.get('listing_type', 'buy')).strip().lower(),
                    price=float(row.get('price', 0)),
                    price_unit=price_unit,
                    bhk=int(row['bhk']) if pd.notna(row.get('bhk')) else None,
                    area_sqft=float(row['area_sqft']) if pd.notna(row.get('area_sqft')) else None,
                    carpet_area=float(row['carpet_area']) if pd.notna(row.get('carpet_area')) else None,
                    floor_number=int(row['floor_number']) if pd.notna(row.get('floor_number')) else None,
                    total_floors=int(row['total_floors']) if pd.notna(row.get('total_floors')) else None,
                    age_years=int(row['age_years']) if pd.notna(row.get('age_years')) else None,
                    furnished=str(row.get('furnished', 'unfurnished')).strip().lower(),
                    facing=str(row.get('facing', '')).strip() or None,
                    description=str(row.get('description', '')).strip() or None,
                    address=str(row.get('address', '')).strip() or None,
                    locality_id=locality_id,
                    is_approved=True,
                    status='active',
                    user_id=current_user.id
                )

                amenities_str = str(row.get('amenities', '')).strip()
                if amenities_str and amenities_str != 'nan':
                    prop.amenities = [a.strip() for a in amenities_str.split(',')]

                db.session.add(prop)
                count += 1

            db.session.commit()
            flash(f'Successfully imported {count} properties.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error importing file: {str(e)}', 'danger')

        return redirect(url_for('admin.bulk_upload'))

    return render_template('admin/bulk_upload.html')


@admin_bp.route('/localities')
@admin_required
def manage_localities():
    localities = db.session.query(Locality).order_by(Locality.zone, Locality.name).all()
    zones = {}
    for loc in localities:
        zones.setdefault(loc.zone, []).append(loc)
    return render_template('admin/localities.html', zones=zones)


@admin_bp.route('/locality/add', methods=['POST'])
@admin_required
def add_locality():
    name = request.form.get('name', '').strip()
    zone = request.form.get('zone', '').strip()
    if name and zone:
        slug = slugify(f"{name}-{zone}")
        if not db.session.query(Locality).filter_by(slug=slug).first():
            loc = Locality(name=name, zone=zone, slug=slug)
            db.session.add(loc)
            db.session.commit()
            flash(f'Locality "{name}" added.', 'success')
        else:
            flash('Locality already exists.', 'warning')
    return redirect(url_for('admin.manage_localities'))


@admin_bp.route('/locality/delete/<int:id>', methods=['POST'])
@admin_required
def delete_locality(id):
    loc = db.session.get(Locality, id)
    if loc:
        db.session.delete(loc)
        db.session.commit()
        flash(f'Locality "{loc.name}" deleted.', 'success')
    return redirect(url_for('admin.manage_localities'))


@admin_bp.route('/analytics')
@admin_required
def analytics():
    # Top properties by enquiry
    from sqlalchemy import func
    top_properties = db.session.query(
        Property.title, Property.slug,
        func.count(EnquiryLog.id).label('clicks')
    ).join(EnquiryLog, EnquiryLog.property_id == Property.id
    ).group_by(Property.id).order_by(func.count(EnquiryLog.id).desc()).limit(10).all()

    # Popular localities
    popular_localities = db.session.query(
        Locality.name, Locality.zone,
        func.count(Property.id).label('count')
    ).join(Property, Property.locality_id == Locality.id
    ).filter(Property.is_approved == True
    ).group_by(Locality.id).order_by(func.count(Property.id).desc()).limit(10).all()

    # Top agents
    top_agents = db.session.query(
        User.name, User.company,
        func.count(Property.id).label('count')
    ).join(Property, Property.user_id == User.id
    ).group_by(User.id).order_by(func.count(Property.id).desc()).limit(10).all()

    return render_template('admin/analytics.html',
                           top_properties=top_properties,
                           popular_localities=popular_localities,
                           top_agents=top_agents)
