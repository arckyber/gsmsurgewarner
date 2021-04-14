from flask import jsonify
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema, User, UserSchema, Extra, ExtraSchema, db,\
    Role, RoleSchema
from sqlalchemy import func, extract
import datetime

def transmitters_count():
    count = db.session.query(func.count(Transmitter.id)).scalar()
    return count

def users_count():
    count = db.session.query(func.count(User.id)).scalar()
    return count

def sms_count():
    count = db.session.query(func.count(Extra.id)).scalar()
    return count

def alert_count():
    count = db.session.query(func.count(Sms.id)).scalar()
    return count

def transmitters():
    query = Transmitter.query.filter(Transmitter.status==True).all()
    output = TransmitterSchema(many=True).dump(query)
    return jsonify(output)

def users():
    query = User.query.all()
    output = UserSchema(many=True).dump(query)
    return jsonify(output)

def detection_history():
    current_year = datetime.datetime.now().year
    sms = Sms.query.first()
    output = SmsSchema(many=False).dump(sms)
    return str(output['created_at'])

def roles_():
    roles = Role.query.all()
    data = {}
    for r in roles:
        user_count = db.session.query(func.count(User.id)).filter(User.role_id == r.id).scalar()
        data[r.role] = user_count
    return jsonify(data)