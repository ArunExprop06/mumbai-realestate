from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = db.session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_approved and user.role != 'admin':
                flash('Your account is pending approval. Please wait for admin approval.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if user.is_admin:
                return redirect(next_page or url_for('admin.dashboard'))
            return redirect(next_page or url_for('agent.dashboard'))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'agent')
        company = request.form.get('company', '').strip()
        rera_number = request.form.get('rera_number', '').strip()

        if db.session.query(User).filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))

        if not all([name, email, phone, password]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('auth.register'))

        if role not in ('agent', 'broker'):
            role = 'agent'

        user = User(
            name=name, email=email, phone=phone,
            role=role, company=company, rera_number=rera_number,
            is_approved=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Your account is pending admin approval.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('public.home'))
