from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema

db = SQLAlchemy()

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

	def __init__(self, name, sim_number, post_number, post_description, location):
		self.name = name
		self.sim_number = sim_number
		self.post_number = post_number
		self.post_description = post_description
		self.location = location

class TransmitterSchema(ModelSchema):
	class Meta:
		model = Transmitter

class Sms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	alert_level = db.Column(db.Integer)
	water_distance = db.Column(db.Float)
	transmitter_id = db.Column(db.Integer, db.ForeignKey('transmitter.id'))
	transmitter = db.relationship('Transmitter')
	created_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)

class SmsSchema(ModelSchema):
	transmitter = fields.Nested(TransmitterSchema)
	class Meta:
		model = Sms

class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(200))
	email = db.Column(db.String(200))
	password = db.Column(db.String(200))

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String())
	role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
	# role = db.relationship('Role')

class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	role = db.Column(db.String())
	user = db.relationship('User')

class UserSchema(ModelSchema):
	class Meta:
		model = User

class RoleSchema(ModelSchema):
	class Meta:
		model = Role