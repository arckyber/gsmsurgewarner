from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Toy(db.Model):
    fields = ['id', 'name']
    id = db.Column(db.Integer(), primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    name = db.Column(db.String)

class Child(db.Model):
    fields = ['id', 'name', 'toys']
    id = db.Column(db.Integer(), primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    name = db.Column(db.String)
    toys = db.relationship('Toy')

class Parent(db.Model):
    id = db.Column(db.Integer(), primary_key=True)  
    name = db.Column(db.String)
    children = db.relationship('Child')

class ToySchema(ModelSchema):
    class Meta:
        model = Toy

class ChildSchema(ModelSchema):
    class Meta:
        model = Child

class ParentSchema(ModelSchema):
    class Meta:
        model = Parent


db.create_all()
if __name__ == '__main__':
    parent = Parent(
        name='kay',
        children=[
            Child(
                name='Taylor',
                toys=[Toy(name='video game')],
            ),
            Child(
                name='Paige',
                toys=[Toy(name='baby')],
            ),
        ],
    )
    # parent = Parent.query.first()
    db.session.add(parent)
    db.session.commit()   
    print(ParentSchema().dump(parent))