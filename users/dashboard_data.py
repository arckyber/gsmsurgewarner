from flask import jsonify
from model.models import Transmitter, TransmitterSchema, Sms, SmsSchema, User, UserSchema, Extra, ExtraSchema, db
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
    # init months
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'sep', 'oct', 'nov', 'dec']
    # set current date
    current_date = datetime.datetime.now()
    # filter create_at field with the current YEAR
    cur_year_str = str(current_date.year)
    # query = Sms.query.filter((str(Sms.created_at)[0:4]) == cur_year_str).all()
    return ""
    query = Sms.query.all()
    output = SmsSchema(many=True).dump(query)
    return jsonify(output)