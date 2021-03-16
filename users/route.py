from flask import Blueprint, url_for, render_template, jsonify
from model.models import User, db, Role, UserSchema
from util.user_serializer import serialize_user_role

users = Blueprint('users', __name__, static_folder="static", template_folder="templates")

@users.route('/')
@users.route('/index')
def index():
    return render_template('users_index.html')

@users.route('/show')
def show():
    results = user.query.join(Role, User._id == Role.id).all()
    # results = user.query.filter().join(user, role).filter(user._id == role.id).all()
    # results = db.session.query(user).join(role).all()
    res = serialize_class().serialize(results[0])
    return jsonify(res)

@users.route('/test')
def test():
    # user = user.query.all()
    # user_schema = UserSchema()
    # output = user_schema.dump(user).data
    # return jsonify({'user' : output})
    return f"<h3>hi</h3>"

@users.route('/adduser')
def adduser():
    u = User('Gagay')
    db.session.add(u)
    db.session.commit()

@users.route('/addrole')
def addrole():
    r = Role('Admin')
    db.session.add(r)
    db.session.commit()

    q = Role.query.all()

    for qq in q:
        print(qq.id)
        print(qq.role)
    
    return f"<h3>Inserted role</h3>"