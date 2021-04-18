from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema
import datetime

db = SQLAlchemy()

class Transmitter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	sim_number = db.Column(db.String(11))
	post_number = db.Column(db.Integer)
	post_description = db.Column(db.Text())
	location = db.Column(db.Text())
	longitude = db.Column(db.Float)
	latitude = db.Column(db.Float)
	create_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)

	def __init__(self, name, sim_number, post_number, post_description, location, longitude, latitude):
		self.name = name
		self.sim_number = sim_number
		self.post_number = post_number
		self.post_description = post_description
		self.location = location
		self.longitude = longitude
		self.latitude = latitude
		self.create_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()
		self.status = True

class TransmitterSchema(ModelSchema):
	class Meta:
		model = Transmitter

class Sms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	alert_type = db.Column(db.Integer)
	water_distance = db.Column(db.Float)
	transmitter_id = db.Column(db.Integer, db.ForeignKey('transmitter.id'))
	transmitter = db.relationship('Transmitter')
	date_sent = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	is_opened = db.Column(db.Boolean)
	status = db.Column(db.Boolean)

	# def create_at_year(self):
	# 	return str(created_at)[0:4]

class SmsSchema(ModelSchema):
	transmitter_id = fields.Integer()
	transmitter = fields.Nested(TransmitterSchema)
	# create_at_year = fields.Function()
	class Meta:
		model = Sms

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	number = db.Column(db.String(13))
	create_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)

class ContactSchema(ModelSchema):
	class Meta:
		model = Contact

class ExtraSms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	message = db.Column(db.Text())
	contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
	contact = db.relationship('Contact')
	created_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)

class ExtraSmsSchema(ModelSchema):
	contact = fields.Nested(ContactSchema)
	class Meta:
		model = ExtraSms

class UserInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(50))
	middlename = db.Column(db.String(50))
	lastname = db.Column(db.String(50))
	gender = db.Column(db.String(10))
	address = db.Column(db.Text())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	image = db.Column(db.Text(), nullable=True)

class UserInfoSchema(ModelSchema):
	class Meta:
		model = UserInfo

class RoleAccess(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	access = db.Column(db.String())

class RoleAccessShema(ModelSchema):
	role_id = fields.Integer()
	class Meta:
		model = RoleAccess

class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String())
	role_access = db.relationship('RoleAccess')
	# user = db.relationship('User')

class RoleSchema(ModelSchema):
	role_access = fields.List(fields.Nested(RoleAccessShema))
	class Meta:
		model = Role

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String())
	email = db.Column(db.String())
	password = db.Column(db.String())
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	userinfo = db.relationship('UserInfo')
	role = db.relationship('Role')
	status = db.Column(db.Boolean)

class UserSchema(ModelSchema):
	userinfo = fields.Nested(UserInfoSchema, required=True)
	role = fields.Nested(RoleSchema, required=True)
	class Meta:
		model = User

class Extra(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	number = db.Column(db.String(13))
	message = db.Column(db.Text())
	created_at = db.Column(db.DateTime)
	date_sent = db.Column(db.DateTime)
	is_opened = db.Column(db.Boolean)
	status = db.Column(db.Boolean)

class ExtraSchema(ModelSchema):
	class Meta:
		model = Extra