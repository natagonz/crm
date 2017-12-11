
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



class AddDealsForm(FlaskForm):	
	product = StringField("Produk",validators=[Length(max=100)])
	amount = StringField("Harga Produk",validators=[Length(max=100)])
	description = TextAreaField("Catatan")	
	status = StringField("Status Penjualan",validators=[Length(max=100)])	
	name = StringField("Nama Konsumen",validators=[Length(max=100)])
	email = StringField("Email Konsumen",validators=[Length(max=100)])
	phone = StringField("Telepon Konsumen",validators=[Length(max=100)])
	

class ForgotPasswordForm(FlaskForm):
	email = StringField("Email",validators=[Length(max=100),Email()])


class ResetPasswordForm(FlaskForm):
	password = PasswordField("Password",validators=[InputRequired(),Length(min=8),EqualTo("confirm",message="Password not match")])
	confirm = PasswordField("Confirm Password")


class KonfirmasiForm(FlaskForm):
	nama = StringField("Nama Di Rekening",validators=[InputRequired(),Length(max=100)])
	bank = StringField("Nama Bank",validators=[InputRequired(),Length(max=100)])
	
