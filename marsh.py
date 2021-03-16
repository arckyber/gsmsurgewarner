from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marsh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'oisd0923434'

db = SQLAlchemy(app)

class Child(db.Model):
    fields = ['id', 'name', 'toys']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    toys = db.relationship('Toy')

class Toy(db.Model):
    fields = ['id', 'name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    child = db.relationship('Child')

class ChildSchema(ModelSchema):
    class Meta:
        model = Child
        fields = ['id', 'name', 'toys']

class ToySchema(ModelSchema):
    class Meta:
        model = Toy
        fields = ['id', 'name']

@app.route('/add')
def add():
    c = Child(name='Carlex', toys=[Toy(name='Airplane'), Toy(name='Yoyo')])
    db.session.add(c)
    db.session.commit()

    return f"<h1>Child "+c.name+" added toy </h1>"

@app.route('/')
def index():
    # q = Child.query.all()
    q = db.session.query(Toy).join(Child).filter(Child.id == Toy.child_id).all()
    # for qq in q:
    #     print(qq.toys.name)
    schema = ChildSchema(many=True)
    output = schema.dump(q)
    return jsonify(output)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)