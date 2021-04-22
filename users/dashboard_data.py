from flask import jsonify
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema, User, UserSchema, Extra, ExtraSchema, db,\
    Role, RoleSchema
from sqlalchemy import func, extract
import datetime

def transmitters_count():
    count = db.session.query(func.count(Transmitter.id)).filter(Transmitter.status == True).scalar()
    return count

def users_count():
    count = db.session.query(func.count(User.id)).filter(User.status == True).scalar()
    return count

def sms_count():
    count = db.session.query(func.count(Extra.id)).filter(Extra.status == True).scalar()
    return count

def alert_count():
    count = db.session.query(func.count(Sms.id)).filter(Sms.status == True).scalar()
    return count

def transmitters():
    query = Transmitter.query.filter(Transmitter.status==True).all()
    output = TransmitterSchema(many=True).dump(query)
    return jsonify(output)

def users():
    query = User.query.filter(User.status == True).all()
    output = UserSchema(many=True).dump(query)
    return jsonify(output)

def detection_history():
    current_year = datetime.datetime.now().year
    sms = Sms.query.first()
    output = SmsSchema(many=False).dump(sms)
    return str("output['created_at']")

def alertsStat():
    data = []
    c_count = db.session.query(func.count(Sms.id)).filter(Sms.alert_type == 3).scalar()
    d_count = db.session.query(func.count(Sms.id)).filter(Sms.alert_type == 4).scalar()

    d1 = {
        'alert_type' : 'Warnings',
        'count' : c_count
    }
    data.append(d1)
    d2 = {
        'alert_type' : 'Danger',
        'count' : d_count
    }
    data.append(d2)
    return data



def roles_():
    roles = Role.query.all()
    data = []
    for r in roles:
        user_count = db.session.query(func.count(User.id)).filter(User.role_id == r.id).scalar()
        d = {
            'count' : user_count,
            'role' : r.role
        }
        data.append(d)
    return data