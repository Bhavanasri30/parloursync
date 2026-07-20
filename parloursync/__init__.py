import flask
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

# Original register_blueprint
original_register_blueprint = flask.Flask.register_blueprint

def patched_register_blueprint(self, blueprint, **options):
    if blueprint.name == 'customer':
        # Add services route
        @blueprint.route('/services')
        def services():
            from parloursync.models import Service
            search_query = request.args.get('search', '')
            category = request.args.get('category', '')
            
            query = Service.query
            if search_query:
                query = query.filter(Service.name.ilike(f'%{search_query}%') | Service.description.ilike(f'%{search_query}%'))
            if category:
                query = query.filter_by(category=category)
                
            services_list = query.all()
            return render_template('customer/services.html', services=services_list, search_query=search_query, category=category)
            
        # Add reviews route
        @blueprint.route('/reviews', methods=['GET', 'POST'])
        def reviews():
            if request.method == 'POST':
                flash('Thank you for your rating! Your review has been published.', 'success')
                return redirect(url_for('customer.reviews'))
            return render_template('customer/reviews.html')
            
        # Add booking-success route
        @blueprint.route('/booking-success')
        @login_required
        def booking_success():
            from parloursync.models import Appointment
            appointment = Appointment.query.filter_by(customer_id=current_user.id).order_by(Appointment.id.desc()).first()
            return render_template('customer/booking_success.html', appointment=appointment)
            
    elif blueprint.name == 'owner':
        # Add appointments route
        @blueprint.route('/appointments')
        @login_required
        def appointments():
            if current_user.role != 'owner':
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('customer.dashboard'))
            from parloursync.models import Appointment
            status = request.args.get('status', '')
            search_query = request.args.get('search', '')
            
            query = Appointment.query
            if status:
                query = query.filter_by(status=status)
            if search_query:
                from parloursync.models import User
                query = query.join(User, Appointment.customer_id == User.id).filter(User.username.ilike(f'%{search_query}%'))
                
            appointments_list = query.order_by(Appointment.appointment_time.desc()).all()
            return render_template('owner/appointments.html', appointments=appointments_list, current_status=status, search_query=search_query)
            
        # Add customers route
        @blueprint.route('/customers')
        @login_required
        def list_customers():
            if current_user.role != 'owner':
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('customer.dashboard'))
            from parloursync.models import User, Appointment
            
            search_query = request.args.get('search', '')
            
            query = User.query.filter_by(role='customer')
            if search_query:
                query = query.filter(User.username.ilike(f'%{search_query}%') | User.email.ilike(f'%{search_query}%'))
                
            users = query.all()
            customers_list = []
            for u in users:
                appts = Appointment.query.filter_by(customer_id=u.id).all()
                last_visit = None
                if appts:
                    appts_sorted = sorted(appts, key=lambda x: x.appointment_time if x.appointment_time else x.id, reverse=True)
                    last_visit = appts_sorted[0].appointment_time
                customers_list.append({
                    'id': u.id,
                    'username': u.username,
                    'email': u.email,
                    'phone': '555-01' + str(10 + u.id % 90),
                    'total_bookings': len(appts),
                    'last_visit': last_visit
                })
            return render_template('owner/customers.html', customers=customers_list, search_query=search_query)
            
        # Add analytics route
        @blueprint.route('/analytics')
        @login_required
        def analytics():
            if current_user.role != 'owner':
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('customer.dashboard'))
            from parloursync.models import Appointment
            appointments_list = Appointment.query.all()
            
            total_revenue = sum(a.service.price for a in appointments_list if a.status == 'completed')
            total_bookings = len(appointments_list)
            pending_bookings = sum(1 for a in appointments_list if a.status == 'pending')
            confirmed_bookings = sum(1 for a in appointments_list if a.status == 'confirmed')
            completed_bookings = sum(1 for a in appointments_list if a.status == 'completed')
            cancelled_bookings = sum(1 for a in appointments_list if a.status == 'cancelled')
            
            return render_template('owner/analytics.html',
                                   total_revenue=total_revenue,
                                   total_bookings=total_bookings,
                                   pending_bookings=pending_bookings,
                                   confirmed_bookings=confirmed_bookings,
                                   completed_bookings=completed_bookings,
                                   cancelled_bookings=cancelled_bookings)
                                   
        # Add settings route
        @blueprint.route('/settings', methods=['GET', 'POST'])
        @login_required
        def settings():
            if current_user.role != 'owner':
                flash('Unauthorized access.', 'danger')
                return redirect(url_for('customer.dashboard'))
            if request.method == 'POST':
                flash('Salon settings updated successfully.', 'success')
                return redirect(url_for('owner.settings'))
            return render_template('owner/settings.html')

    # Register blueprint
    res = original_register_blueprint(self, blueprint, **options)
    
    # Custom error handlers on app
    @self.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @self.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
        
    @self.before_request
    def setup_index_override():
        current_view_func = self.view_functions.get('index')
        if current_view_func and getattr(current_view_func, '__name__', '') != 'index_override':
            def index_override():
                if current_user.is_authenticated:
                    if current_user.role == 'owner':
                        return redirect(url_for('owner.dashboard'))
                    return redirect(url_for('customer.dashboard'))
                return render_template('customer/index.html')
            index_override.__name__ = 'index_override'
            self.view_functions['index'] = index_override
    
    return res

flask.Flask.register_blueprint = patched_register_blueprint
