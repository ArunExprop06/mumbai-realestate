import os
import re
import uuid
from PIL import Image
from flask import current_app


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return re.sub(r'-+', '-', text)


def save_property_image(file, property_id):
    """Save an uploaded property image, create thumbnail, return filename."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
        return None

    filename = f"{property_id}_{uuid.uuid4().hex[:8]}{ext}"
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'properties')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    img = Image.open(file)
    img.thumbnail((1200, 900), Image.LANCZOS)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.save(filepath, quality=85, optimize=True)

    # Create thumbnail
    thumb_dir = os.path.join(upload_dir, 'thumbs')
    os.makedirs(thumb_dir, exist_ok=True)
    thumb = Image.open(filepath)
    thumb.thumbnail(current_app.config['THUMBNAIL_SIZE'], Image.LANCZOS)
    thumb.save(os.path.join(thumb_dir, filename), quality=80, optimize=True)

    return filename


def save_user_photo(file):
    """Save user profile photo, return filename."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ('.jpg', '.jpeg', '.png', '.webp'):
        return None

    filename = f"user_{uuid.uuid4().hex[:8]}{ext}"
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'users')
    os.makedirs(upload_dir, exist_ok=True)

    filepath = os.path.join(upload_dir, filename)
    img = Image.open(file)
    img.thumbnail((300, 300), Image.LANCZOS)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    img.save(filepath, quality=85, optimize=True)
    return filename


def delete_property_image(filename):
    """Delete a property image and its thumbnail."""
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'properties')
    filepath = os.path.join(upload_dir, filename)
    thumb_path = os.path.join(upload_dir, 'thumbs', filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)


AMENITY_ICONS = {
    "Parking": "bi-car-front",
    "Lift": "bi-arrow-up-square",
    "Gym": "bi-heart-pulse",
    "Swimming Pool": "bi-water",
    "Security": "bi-shield-check",
    "Power Backup": "bi-lightning",
    "Club House": "bi-building",
    "Garden": "bi-tree",
    "Children Play Area": "bi-balloon",
    "Terrace": "bi-sun",
    "Jogging Track": "bi-person-walking",
    "Fire Safety": "bi-fire",
    "Cafeteria": "bi-cup-hot",
    "Road Access": "bi-signpost-split",
    "Water Supply": "bi-droplet",
    "Electricity": "bi-plug",
    "CCTV": "bi-camera-video",
    "Intercom": "bi-telephone",
    "Rainwater Harvesting": "bi-cloud-rain",
    "Vastu Compliant": "bi-compass",
    "Piped Gas": "bi-fuel-pump",
    "Visitor Parking": "bi-p-square",
}
