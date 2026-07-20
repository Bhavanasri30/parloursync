from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from parloursync.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register As', choices=[('customer', 'Customer'), ('owner', 'Salon Owner')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please log in.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    price = FloatField('Price ($)', validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (minutes)', validators=[DataRequired()])
    submit = SubmitField('Save Service')


class StaffForm(FlaskForm):
    name = StringField('Staff Name', validators=[DataRequired(), Length(max=100)])
    bio = TextAreaField('Bio / Specialty', validators=[Length(max=500)])
    email = StringField('Email', validators=[Email(), Length(max=120)])
    submit = SubmitField('Save Staff Member')


class AppointmentForm(FlaskForm):
    service_id = SelectField('Select Service', coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Select Stylist / Staff', coerce=int, validators=[DataRequired()])
    appointment_time = StringField('Appointment Date & Time', validators=[DataRequired()]) # HTML5 datetime-local field as a string
    notes = TextAreaField('Special Notes / Requests', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')
