import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from extensions import db
from models import Property, PropertyImage, Locality, EnquiryLog
from helpers import slugify, save_property_image, save_user_photo, delete_property_image
from functools import wraps

agent_bp = Blueprint('agent', __name__, url_prefix='/agent')


def agent_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.can_post:
            flash('Your account is not approved yet.', 'warning')
            return redirect(url_for('public.home'))
        return f(*args, **kwargs)
    return decorated


@agent_bp.route('/dashboard')
@agent_required
def dashboard():
    my_properties = current_user.properties.count()
    total_views = db.session.query(db.func.sum(Property.views_count)).filter_by(
        user_id=current_user.id
    ).scalar() or 0
    enquiry_clicks = db.session.query(EnquiryLog).join(Property).filter(
        Property.user_id == current_user.id
    ).count()
    recent = current_user.properties.order_by(Property.created_at.desc()).limit(5).all()

    return render_template('agent/dashboard.html',
                           my_properties=my_properties,
                           total_views=total_views,
                           enquiry_clicks=enquiry_clicks,
                           recent=recent)


@agent_bp.route('/properties')
@agent_required
def my_properties():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.properties.order_by(
        Property.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    return render_template('agent/my_properties.html',
                           properties=pagination.items,
                           pagination=pagination)


@agent_bp.route('/property/add', methods=['GET', 'POST'])
@agent_required
def add_property():
    localities = db.session.query(Locality).order_by(Locality.zone, Locality.name).all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        property_type = request.form.get('property_type')
        listing_type = request.form.get('listing_type')
        price = request.form.get('price', type=float)
        price_unit = request.form.get('price_unit', 'lakh')

        if not all([title, property_type, listing_type, price]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('agent/property_form.html', localities=localities, editing=False)

        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while db.session.query(Property).filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        prop = Property(
            title=title,
            slug=slug,
            property_type=property_type,
            listing_type=listing_type,
            price=price,
            price_unit=price_unit,
            bhk=request.form.get('bhk', type=int),
            area_sqft=request.form.get('area_sqft', type=float),
            carpet_area=request.form.get('carpet_area', type=float),
            floor_number=request.form.get('floor_number', type=int),
            total_floors=request.form.get('total_floors', type=int),
            age_years=request.form.get('age_years', type=int),
            furnished=request.form.get('furnished', 'unfurnished'),
            facing=request.form.get('facing'),
            description=request.form.get('description', '').strip(),
            address=request.form.get('address', '').strip(),
            locality_id=request.form.get('locality_id', type=int),
            user_id=current_user.id,
            is_approved=current_user.is_admin,
            status='active'
        )

        amenities = request.form.getlist('amenities')
        prop.amenities = amenities

        db.session.add(prop)
        db.session.commit()

        # Handle images
        files = request.files.getlist('images')
        for i, file in enumerate(files):
            if file and file.filename:
                filename = save_property_image(file, prop.id)
                if filename:
                    img = PropertyImage(
                        property_id=prop.id,
                        filename=filename,
                        is_primary=(i == 0),
                        sort_order=i
                    )
                    db.session.add(img)

        db.session.commit()
        flash('Property added successfully! It will be visible after admin approval.', 'success')
        return redirect(url_for('agent.my_properties'))

    return render_template('agent/property_form.html', localities=localities, editing=False)


@agent_bp.route('/property/edit/<int:id>', methods=['GET', 'POST'])
@agent_required
def edit_property(id):
    prop = db.session.get(Property, id)
    if not prop or (prop.user_id != current_user.id and not current_user.is_admin):
        flash('Property not found.', 'danger')
        return redirect(url_for('agent.my_properties'))

    localities = db.session.query(Locality).order_by(Locality.zone, Locality.name).all()

    if request.method == 'POST':
        prop.title = request.form.get('title', '').strip()
        prop.property_type = request.form.get('property_type')
        prop.listing_type = request.form.get('listing_type')
        prop.price = request.form.get('price', type=float)
        prop.price_unit = request.form.get('price_unit', 'lakh')
        prop.bhk = request.form.get('bhk', type=int)
        prop.area_sqft = request.form.get('area_sqft', type=float)
        prop.carpet_area = request.form.get('carpet_area', type=float)
        prop.floor_number = request.form.get('floor_number', type=int)
        prop.total_floors = request.form.get('total_floors', type=int)
        prop.age_years = request.form.get('age_years', type=int)
        prop.furnished = request.form.get('furnished', 'unfurnished')
        prop.facing = request.form.get('facing')
        prop.description = request.form.get('description', '').strip()
        prop.address = request.form.get('address', '').strip()
        prop.locality_id = request.form.get('locality_id', type=int)
        prop.amenities = request.form.getlist('amenities')

        # Handle delete images
        delete_ids = request.form.getlist('delete_images')
        for img_id in delete_ids:
            img = db.session.get(PropertyImage, int(img_id))
            if img and img.property_id == prop.id:
                delete_property_image(img.filename)
                db.session.delete(img)

        # Handle new images
        files = request.files.getlist('images')
        existing_count = prop.images.count()
        for i, file in enumerate(files):
            if file and file.filename:
                filename = save_property_image(file, prop.id)
                if filename:
                    img = PropertyImage(
                        property_id=prop.id,
                        filename=filename,
                        is_primary=(existing_count == 0 and i == 0),
                        sort_order=existing_count + i
                    )
                    db.session.add(img)

        # Set primary image
        primary_id = request.form.get('primary_image', type=int)
        if primary_id:
            for img in prop.all_images:
                img.is_primary = (img.id == primary_id)

        db.session.commit()
        flash('Property updated successfully.', 'success')
        return redirect(url_for('agent.my_properties'))

    return render_template('agent/property_form.html',
                           property=prop, localities=localities, editing=True)


@agent_bp.route('/property/delete/<int:id>', methods=['POST'])
@agent_required
def delete_property(id):
    prop = db.session.get(Property, id)
    if not prop or (prop.user_id != current_user.id and not current_user.is_admin):
        flash('Property not found.', 'danger')
        return redirect(url_for('agent.my_properties'))

    for img in prop.all_images:
        delete_property_image(img.filename)

    db.session.delete(prop)
    db.session.commit()
    flash('Property deleted.', 'success')
    return redirect(url_for('agent.my_properties'))


@agent_bp.route('/property/status/<int:id>/<status>', methods=['POST'])
@agent_required
def change_status(id, status):
    prop = db.session.get(Property, id)
    if not prop or (prop.user_id != current_user.id and not current_user.is_admin):
        flash('Property not found.', 'danger')
        return redirect(url_for('agent.my_properties'))

    if status in ('active', 'sold', 'rented', 'inactive'):
        prop.status = status
        db.session.commit()
        flash(f'Property marked as {status}.', 'success')

    return redirect(url_for('agent.my_properties'))


@agent_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.company = request.form.get('company', '').strip()
        current_user.rera_number = request.form.get('rera_number', '').strip()

        photo = request.files.get('photo')
        if photo and photo.filename:
            filename = save_user_photo(photo)
            if filename:
                current_user.photo = filename

        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('agent.profile'))

    return render_template('agent/profile.html')
