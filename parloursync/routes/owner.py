from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from parloursync.extensions import db
from parloursync.models import User, Service, Staff, Appointment
from parloursync.forms import ServiceForm, StaffForm
from sqlalchemy import func

owner_bp = Blueprint('owner', __name__, url_prefix='/owner')

@owner_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'owner':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('customer.dashboard'))
        
    # Get all appointments
    appointments = Appointment.query.order_by(Appointment.appointment_time.desc()).all()
    
    # Calculate some dashboard stats
    total_appointments = len(appointments)
    pending_count = sum(1 for a in appointments if a.status == 'pending')
    confirmed_count = sum(1 for a in appointments if a.status == 'confirmed')
    completed_count = sum(1 for a in appointments if a.status == 'completed')
    
    # Total revenue from completed appointments
    total_revenue = sum(a.service.price for a in appointments if a.status == 'completed')
    
    return render_template('owner/dashboard.html', 
                           appointments=appointments,
                           total_appointments=total_appointments,
                           pending_count=pending_count,
                           confirmed_count=confirmed_count,
                           completed_count=completed_count,
                           total_revenue=total_revenue)


@owner_bp.route('/appointment/<int:id>/status/<string:status>', methods=['POST'])
@login_required
def update_status(id, status):
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
        
    appointment = Appointment.query.get_or_404(id)
    if status in ['confirmed', 'completed', 'cancelled', 'pending']:
        appointment.status = status
        db.session.commit()
        flash(f'Appointment status updated to {status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
        
    return redirect(url_for('owner.dashboard'))


# --- Services Management ---

@owner_bp.route('/services')
@login_required
def list_services():
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    services = Service.query.all()
    return render_template('owner/services.html', services=services)


@owner_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            duration_minutes=form.duration_minutes.data
        )
        db.session.add(service)
        db.session.commit()
        flash('New service added successfully!', 'success')
        return redirect(url_for('owner.list_services'))
    return render_template('owner/service_form.html', form=form, title='Add New Service')


@owner_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.duration_minutes = form.duration_minutes.data
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('owner.list_services'))
    return render_template('owner/service_form.html', form=form, title=f'Edit Service: {service.name}')


@owner_bp.route('/services/<int:id>/delete', methods=['POST'])
@login_required
def delete_service(id):
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    service = Service.query.get_or_404(id)
    # Check if there are active appointments referencing this service
    has_appointments = Appointment.query.filter_by(service_id=id).first()
    if has_appointments:
        flash('Cannot delete service because it has existing appointments linked to it.', 'danger')
    else:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully.', 'success')
    return redirect(url_for('owner.list_services'))


# --- Staff Management ---

@owner_bp.route('/staff')
@login_required
def list_staff():
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    staff_members = Staff.query.all()
    return render_template('owner/staff.html', staff_members=staff_members)


@owner_bp.route('/staff/add', methods=['GET', 'POST'])
@login_required
def add_staff():
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    form = StaffForm()
    if form.validate_on_submit():
        staff = Staff(
            name=form.name.data,
            bio=form.bio.data,
            email=form.email.data
        )
        db.session.add(staff)
        db.session.commit()
        flash('New staff member added successfully!', 'success')
        return redirect(url_for('owner.list_staff'))
    return render_template('owner/staff_form.html', form=form, title='Add Stylist / Staff Member')


@owner_bp.route('/staff/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_staff(id):
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    staff = Staff.query.get_or_404(id)
    form = StaffForm(obj=staff)
    if form.validate_on_submit():
        staff.name = form.name.data
        staff.bio = form.bio.data
        staff.email = form.email.data
        db.session.commit()
        flash('Staff member details updated successfully!', 'success')
        return redirect(url_for('owner.list_staff'))
    return render_template('owner/staff_form.html', form=form, title=f'Edit Stylist: {staff.name}')


@owner_bp.route('/staff/<int:id>/delete', methods=['POST'])
@login_required
def delete_staff(id):
    if current_user.role != 'owner':
        return redirect(url_for('customer.dashboard'))
    staff = Staff.query.get_or_404(id)
    # Check if there are active appointments referencing this staff
    has_appointments = Appointment.query.filter_by(staff_id=id).first()
    if has_appointments:
        flash('Cannot delete staff member because they have existing appointments linked to them.', 'danger')
    else:
        db.session.delete(staff)
        db.session.commit()
        flash('Staff member removed successfully.', 'success')
    return redirect(url_for('owner.list_staff'))
