from flask import Blueprint, render_template, url_for, current_app, request, flash, jsonify, session, redirect
from model.models import db, Sms, SmsSchema, Transmitter
import datetime
from sqlalchemy import desc, asc, func
import random
from config.const import SUCCESS, FAILED, ERROR, ALERT_3_MESSAGE, ALERT_4_MESSAGE, DISTANCE_DEFAULT_UNIT

recycle = Blueprint('recycle', __name__, static_folder='static', template_folder='templates')

@recycle.route('/')
def index():
    return render_template('/index.html')