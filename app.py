from flask import Flask,render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager , UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from form import UserRegisterForm, UserLoginForm, AddContactForm, AddDealsForm, ForgotPasswordForm, ResetPasswordForm, ChangeImagesForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
from datetime import datetime, timedelta
from config import secret,database

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database
app.config["SECRET_KEY"] = secret


#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "UserLogin"

images = UploadSet("images",IMAGES)
app.config["UPLOADED_IMAGES_DEST"] = "static/img/profile/"
app.config["UPLOADED_IMAGES_URL"] = "http://127.0.0.1:5000/static/img/profile/"
configure_uploads(app,images)

#fungsi mail
app.config.from_pyfile("config.py") 
mail = Mail(app)
s = URLSafeTimedSerializer("secret")




class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(100))
	email = db.Column(db.String(100))
	password = db.Column(db.String(500))
	phone = db.Column(db.String(200))
	contact = db.relationship("Contact",backref="owner",lazy="dynamic")
	deals = db.relationship("Deals",backref="deals",lazy="dynamic")

	def is_active(self):
		return True

	def get_id(self):
		return self.id

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return False


class Contact(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	phone = db.Column(db.String(100))
	company = db.Column(db.String(200))
	address = db.Column(db.String(200))
	about = db.Column(db.UnicodeText())
	image = db.Column(db.String(100))
	owner_id = db.Column(db.Integer(),db.ForeignKey("user.id"))



class Deals(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	title = db.Column(db.String(30))
	description = db.Column(db.UnicodeText())
	created = db.Column(db.DateTime())
	status = db.Column(db.String(30))
	deals_id = db.Column(db.Integer(),db.ForeignKey("user.id"))



#user loader
@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))



#################### front page & user function  ####################################

@app.route("/",methods=["GET","POST"])
def Index():
	return render_template("index.html")



@app.route("/register",methods=["GET","POST"])
def UserRegister():
	form = UserRegisterForm()
	if form.validate_on_submit():
		hass_pass = generate_password_hash(form.password.data,method="sha256")
		user = User(username=form.username.data,email=form.email.data,phone=form.phone.data,password=hass_pass)
		db.session.add(user)
		db.session.commit()

		flash("Registration successfully","success")
		return redirect(url_for("UserLogin"))
	return render_template("user/register.html",form=form)


@app.route("/login",methods=["GET","POST"])
def UserLogin():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			if check_password_hash(user.password,form.password.data):
				login_user(user)
				flash("Loggin success","success")
				return redirect(url_for("UserDashboard"))

		flash("Invalid login","danger")
		return render_template("user/login.html",form=form)
	return render_template("user/login.html",form=form)




@app.route("/logout")
@login_required
def Logout():
	logout_user()	
	return redirect(url_for("Index"))



@app.route("/forgot-password",methods=["GET","POST"])
def ForgotPassword():
	form = ForgotPasswordForm()
	if form.validate_on_submit():
		email = form.email.data
		user = User.query.filter_by(email=email).first()
		if user :
			token = s.dumps(email, salt="email-confirm")

			msg = Message("Reset Password", sender="kerjasales.com@gmail.com", recipients=[email])

			link = url_for("ResetPassword", token=token, _external=True)

			msg.body = "your link is {}".format(link)
			mail.send(msg)
		
			flash("Please check your inbox and click reset password link","success")
			return redirect(url_for("UserLogin"))
		else :
			flash("Invalid email","danger")
			return render_template("user/forgot_password.html",form=form)
	return render_template("user/forgot_password.html",form=form)



@app.route("/reset-password/<token>",methods=["GET","POST"])
def ResetPassword(token):
	form = ResetPasswordForm()
	try :
		email = s.loads(token, salt="email-confirm", max_age=3000)
		if form.validate_on_submit():
			user = User.query.filter_by(email=email).first()
			hass_pass = generate_password_hash(form.password.data,method="sha256")
			user.password = hass_pass
			db.session.commit()

			flash("Password been successfully changed","success")
			return redirect(url_for("UserLogin"))
	except :
		flash("Link Expired","danger")
		return redirect(url_for("ForgotPassword"))

	return render_template("user/reset_password.html",form=form)	


@app.route("/dashboard/reset-password",methods=["GET","POST"])
@login_required
def UserResetPassword():
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(id=current_user.id).first()
		hass_pass = generate_password_hash(form.password.data,method="sha256")
		user.password = hass_pass

		db.session.commit()
		logout_user()

		flash("Your password been changed,now loggin again","success")
		return redirect(url_for("UserLogin"))
	return render_template("user/reset_password.html",form=form)		
			


@app.route("/dashboard/change-images/<string:id>",methods=["GET","POST"])
@login_required
def ChangeImages(id):
	form = ChangeImagesForm()
	if form.validate_on_submit():
		contact = Contact.query.filter_by(id=id).first()
		filename = images.save(form.images.data)
		contact.image = filename
		db.session.commit()
		flash("Images been updated","success")
		return redirect(url_for("UserContact"))
	return render_template("user/photo.html",form=form)	





################################# dashboard #############################
@app.route("/dashboard",methods=["GET","POST"])
@login_required
def UserDashboard():
	contact = Contact.query.filter_by(owner_id=current_user.id).all()
	deals = Deals.query.filter_by(deals_id=current_user.id).all()
	len_deal = len(deals)
	len_contact = len(contact)
	return render_template("user/dashboard.html",len_contact=len_contact,len_deal=len_deal)




################################# contact ###############################################


@app.route("/dashboard/contact",methods=["GET","POST"])
def UserContact():
	contacts = Contact.query.filter_by(owner_id=current_user.id).all()
	return render_template("user/contact.html",contacts=contacts)



@app.route("/dashboard/contact/<string:id>",methods=["GET","POST"])
def UserContactId(id):
	contact = Contact.query.filter_by(id=id).first()
	return render_template("user/contact_id.html",contact=contact)



@app.route("/dashboard/add-contact",methods=["GET","POST"])
def AddContact():
	form = AddContactForm()
	if form.validate_on_submit():
		filename = images.save(form.images.data)
		contact = Contact(name=form.name.data,email=form.email.data,phone=form.phone.data,company=form.company.data,address=form.address.data,about=form.about.data,owner_id=current_user.id,image=filename)
		db.session.add(contact)
		db.session.commit()

		flash("Contact Added","success")
		return redirect(url_for("UserContact"))

	return render_template("user/add_contact.html",form=form)

@app.route("/dashboard/edit-contact/<string:id>",methods=["GET","POST"])
def EditContact(id):
	form = AddContactForm()
	contact = Contact.query.filter_by(id=id).first()
	form.name.data = contact.name
	form.email.data = contact.email
	form.phone.data = contact.phone
	form.address.data = contact.address
	form.company.data = contact.company
	form.about.data = contact.about
	if form.validate_on_submit():
		contact.name = request.form["name"]
	  	contact.email = request.form["email"]
	 	contact.phone = request.form["phone"]
	 	contact.address = request.form["address"]
	  	contact.company = request.form["company"]
	 	contact.about = request.form["about"]
	 	db.session.commit()
	 	flash("Contact successfully edited","success")
	 	return redirect(url_for("UserContact"))

	return render_template("user/edit_contact.html",form=form)



@app.route("/dashboard/delete-contact/<string:id>",methods=["GET","POST"])
def DeleteContact(id):
	contact = Contact.query.filter_by(id=id).first()
	db.session.delete(contact)
	db.session.commit()

	flash("Contact successfully deleted","success")
	return redirect(url_for("UserContact"))





############################# Deals #################################

@app.route("/dashboard/deals",methods=["GET","POST"])
@login_required
def UserDeals():
	deals = Deals.query.filter_by(deals_id=current_user.id).all()
	return render_template("user/deal.html",deals=deals)



@app.route("/dashboard/add-deals",methods=["GET","POST"])
@login_required
def AddDeals():
	form = AddDealsForm()
	if form.validate_on_submit():
		today = datetime.today()
		deals = Deals(name=form.name.data,title=form.title.data,description=form.description.data,created=today,status=form.status.data,deals_id=current_user.id)
		db.session.add(deals)
		db.session.commit()

		flash("Deals Successfully Added","success")
		return redirect(url_for("UserDeals"))	
	return render_template("user/add_deals.html",form=form)


@app.route("/dashboard/deals/<string:id>",methods=["GET","POST"])
@login_required
def UserDealsId(id):
	deal = Deals.query.filter_by(id=id).first()
	return render_template("user/deal_id.html",deal=deal)



@app.route("/dashboard/edit-deals/<string:id>",methods=["GET","POST"])
@login_required
def EditDeals(id):
	form = AddDealsForm()
	deal = Deals.query.filter_by(id=id).first()
	form.name.data = deal.name
	form.title.data = deal.title
	form.description.data = deal.description
	form.status.data = deal.status
	if form.validate_on_submit():
		deal.name = request.form["name"]
		deal.title = request.form["title"]
		deal.description = request.form["description"]
		deal.status = request.form["status"]
		db.session.commit()

		flash("Deals been edited","success")
		return redirect(url_for("UserDeals"))

	return render_template("user/edit_deals.html",form=form)	



@app.route("/dashboard/delete-deals/<string:id>",methods=["GET","POST"])
@login_required
def DeleteDeals(id):
	deal = Deals.query.filter_by(id=id).first()
	db.session.delete(deal)
	db.session.commit()

	flash("Deals been deleted","success")
	return redirect(url_for("UserDeals"))





















	







if __name__ == "__main__":
	app.run(host='0.0.0.0')
