
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,TextAreaField, IntegerField, DateField
from wtforms.validators import InputRequired, EqualTo, Email, Length



class UserRegisterForm(FlaskForm):
	username = StringField("Username",validators=[InputRequired(),Length(max=100)])
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	phone = StringField("Phone",validators=[InputRequired(),Length(max=100)])
	password = PasswordField("Password",validators=[InputRequired(),Length(min=8),EqualTo("confirm",message="Password not match")])
	confirm = PasswordField("Confirm Password")


class UserLoginForm(FlaskForm):
	email = StringField("Email",validators=[InputRequired(),Length(max=100),Email()])
	password = PasswordField("Password",validators=[InputRequired()])


class AddContactForm(FlaskForm):
	name = StringField("Name",validators=[Length(max=200)])
	email = StringField("Email",validators=[Length(max=100),Email()])
	phone = StringField("Phone",validators=[Length(max=100)])
	company = StringField("Company",validators=[Length(max=100)])
	address = StringField("Address",validators=[Length(max=100)])
	about = TextAreaField("About")
	
class AddDealsForm(FlaskForm):
	name = StringField("Name",validators=[Length(max=30)])
	title = StringField("Title",validators=[Length(max=30)])
	description = TextAreaField("Description")
	status = StringField("Deals Status",validators=[Length(max=30)])


class ForgotPasswordForm(FlaskForm):
	email = StringField("Email",validators=[Length(max=100),Email()])


class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password",validators=[InputRequired(),Length(min=8),EqualTo("confirm",message="Password not match")])
	confirm = PasswordField("Confirm Password")


class KonfirmasiForm(FlaskForm):
	nama = StringField("Nama Di Rekening",validators=[InputRequired(),Length(max=100)])
	bank = StringField("Nama Bank",validators=[InputRequired(),Length(max=100)])
	
