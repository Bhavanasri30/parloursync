from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from parloursync.extensions import db
from parloursync.models import User, Service, Staff, Appointment
from parloursync.forms import AppointmentForm

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('owner.dashboard'))
        
    # Get user appointments
    appointments = Appointment.query.filter_by(customer_id=current_user.id).order_by(Appointment.appointment_time.asc()).all()
    
    # Split into upcoming and past
    now = datetime.now()
    upcoming = [a for a in appointments if a.appointment_time >= now and a.status != 'cancelled']
    past_or_cancelled = [a for a in appointments if a.appointment_time < now or a.status == 'cancelled']
    
    return render_template('customer/dashboard.html', upcoming=upcoming, past_or_cancelled=past_or_cancelled)


@customer_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if current_user.role != 'customer':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('owner.dashboard'))
        
    form = AppointmentForm()
    
    # Populate select fields
    services = Service.query.all()
    staff_members = Staff.query.all()
    
    form.service_id.choices = [(s.id, f"{s.name} - ${s.price:.2f} ({s.duration_minutes} mins)") for s in services]
    form.staff_id.choices = [(st.id, st.name) for st in staff_members]
    
    if not services or not staff_members:
        flash('Booking is temporarily unavailable. Salon owner has not set up services or stylists yet.', 'warning')
        
    if form.validate_on_submit():
        try:
            # Parse datetime string from HTML5 datetime-local (format: YYYY-MM-DDTHH:MM)
            time_str = form.appointment_time.data
            appointment_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
            
            appointment = Appointment(
                customer_id=current_user.id,
                service_id=form.service_id.data,
                staff_id=form.staff_id.data,
                appointment_time=appointment_time,
                notes=form.notes.data,
                status='pending'
            )
            db.session.add(appointment)
            db.session.commit()
            flash('Your appointment has been booked successfully and is pending confirmation!', 'success')
            return redirect(url_for('customer.dashboard'))
        except ValueError as e:
            flash('Invalid date or time format.', 'danger')
            
    return render_template('customer/book.html', form=form, has_services=bool(services), has_staff=bool(staff_members))


@customer_bp.route('/appointment/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(id):
    if current_user.role != 'customer':
        return redirect(url_for('owner.dashboard'))
        
    appointment = Appointment.query.get_or_404(id)
    if appointment.customer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.dashboard'))
        
    appointment.status = 'cancelled'
    db.session.commit()
    flash('Appointment successfully cancelled.', 'success')
    return redirect(url_for('customer.dashboard'))
