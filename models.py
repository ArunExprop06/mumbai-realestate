import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='agent')  # admin, agent, broker
    company = db.Column(db.String(200))
    rera_number = db.Column(db.String(50))
    is_approved = db.Column(db.Boolean, default=False)
    photo = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    properties = db.relationship('Property', backref='owner', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def can_post(self):
        return self.is_approved or self.role == 'admin'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Locality(db.Model):
    __tablename__ = 'localities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(200))

    properties = db.relationship('Property', backref='locality', lazy='dynamic')


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    property_type = db.Column(db.String(20), nullable=False)  # flat, house, villa, office, shop, plot, warehouse
    listing_type = db.Column(db.String(10), nullable=False)  # buy, rent
    price = db.Column(db.Float, nullable=False)
    price_unit = db.Column(db.String(10), default='lakh')  # lakh, crore, month
    bhk = db.Column(db.Integer)
    area_sqft = db.Column(db.Float)
    carpet_area = db.Column(db.Float)
    floor_number = db.Column(db.Integer)
    total_floors = db.Column(db.Integer)
    age_years = db.Column(db.Integer)
    furnished = db.Column(db.String(20), default='unfurnished')  # unfurnished, semi, fully
    facing = db.Column(db.String(20))
    description = db.Column(db.Text)
    _amenities = db.Column('amenities', db.Text, default='[]')
    address = db.Column(db.String(300))
    locality_id = db.Column(db.Integer, db.ForeignKey('localities.id'))
    is_featured = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, sold, rented, inactive
    views_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('PropertyImage', backref='property', lazy='dynamic',
                             cascade='all, delete-orphan', order_by='PropertyImage.sort_order')

    @property
    def amenities(self):
        try:
            return json.loads(self._amenities) if self._amenities else []
        except (json.JSONDecodeError, TypeError):
            return []

    @amenities.setter
    def amenities(self, value):
        self._amenities = json.dumps(value) if value else '[]'

    @property
    def primary_image(self):
        img = db.session.query(PropertyImage).filter_by(
            property_id=self.id, is_primary=True
        ).first()
        if not img:
            img = db.session.query(PropertyImage).filter_by(
                property_id=self.id
            ).order_by(PropertyImage.sort_order).first()
        return img

    @property
    def formatted_price(self):
        if self.listing_type == 'rent':
            return f"\u20b9{self.price:,.0f}/month"
        if self.price_unit == 'crore':
            return f"\u20b9{self.price} Cr"
        return f"\u20b9{self.price} Lakhs"

    @property
    def all_images(self):
        return db.session.query(PropertyImage).filter_by(
            property_id=self.id
        ).order_by(PropertyImage.sort_order).all()


class PropertyImage(db.Model):
    __tablename__ = 'property_images'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)


class EnquiryLog(db.Model):
    __tablename__ = 'enquiry_logs'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    action = db.Column(db.String(20), nullable=False)  # phone_click, whatsapp_click
    visitor_ip = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
