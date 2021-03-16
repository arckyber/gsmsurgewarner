from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from sms.model.sms import Sms

db = SQLAlchemy()

class Transmitter(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	sim_number = db.Column(db.String(11))
	post_number = db.Column(db.Integer)
	post_description = db.Column(db.Text())
	location = db.Column(db.Text())
	create_at = db.Column(db.DateTime)
	updated_at = db.Column(db.DateTime)
	status = db.Column(db.Boolean)
	sms = db.relationship('Sms')

	def __init__(self, name, sim_number, post_number, post_description, location):
		self.name = name
		self.sim_number = sim_number
		self.post_number = post_number
		self.post_description = post_description
		self.location = location

class TransmitterSchema(ModelSchema):
	class Meta:
		model = Transmitter