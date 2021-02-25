from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema
from config.const import NORMAL, YELLOW, ORANGE, RED
import datetime

db = SQLAlchemy()


class Desequivalert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	_normal = db.Column(db.Float)
	_yellow = db.Column(db.Float)
	_orange = db.Column(db.Float)
	_red = db.Column(db.Float)
	transmitter_id = db.Column(db.Integer, db.ForeignKey('transmitter.id'))
	created_at = db.Column(db.DateTime)

	def __init__(self, _normal, _yellow, _orange, _red, transmitter_id):
		self._normal = _normal
		self._yellow = _yellow
		self._orange = _orange
		self._red = _red
		self.transmitter_id = transmitter_id
		self.created_at = datetime.datetime.now()

class DesequivalertSchema(ModelSchema):
	transmitter_id = fields.Integer()
	class Meta:
		model = Desequivalert

class Transmitter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	sim_number = db.Column(db.String(11))
	post_number = db.Column(db.Integer)
	post_description = db.Column(db.Text())
	location = db.Column(db.Text())
	create_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)

	# desequivealert_id = db.Column(db.Integer, db.ForeignKey('desequivalert.id'))
	desequivealert = db.relationship('Desequivalert')

	def __init__(self, name, sim_number, post_number, post_description, location):
		self.name = name
		self.sim_number = sim_number
		self.post_number = post_number
		self.post_description = post_description
		self.location = location
		self.create_at = datetime.datetime.now()
		self.updated_at = datetime.datetime.now()

class TransmitterSchema(ModelSchema):
	desequivealert = fields.List(fields.Nested(DesequivalertSchema, required=True))
	class Meta:
		model = Transmitter

class Sms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	alert_level = db.Column(db.Integer)
	water_distance = db.Column(db.Float)
	transmitter_id = db.Column(db.Integer, db.ForeignKey('transmitter.id'))
	transmitter = db.relationship('Transmitter')
	date_sent = db.Column(db.DateTime)
	created_at = db.Column(db.DateTime)
	is_opened = db.Column(db.Boolean)
	status = db.Column(db.Boolean)

class SmsSchema(ModelSchema):
	transmitter = fields.Nested(TransmitterSchema)
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

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	email = db.Column(db.String())
	password = db.Column(db.String())
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	# role = db.relationship('Role')

class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String())
	# user = db.relationship('User')

class UserSchema(ModelSchema):
	class Meta:
		model = User

class RoleSchema(ModelSchema):
	class Meta:
		model = Role

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