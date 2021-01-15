from flask_sqlalchemy import SQLAlchemy

class Admin():

	model = None
	username = ''

	def __init__(self, model=SQLAlchemy()):
		self.model = model.Model