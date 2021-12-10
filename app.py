from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import re
from flask import request
from flask import jsonify
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)

app.config["SQLAlCHEMY_TRACK_NOTIFICATION"] = True
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"] = True

POSTGRES = {
    'user': 'postgres',
    'pw': 'karan123',
    'db': 'ffsdb',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.debug = True
db = SQLAlchemy(app)


class sms(db.Model):
    __tablename__ = 'data_entry'
    id = Column(Integer, Sequence('data_entry_id_seq'), primary_key=True)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    date_of_fire = db.Column(db.DateTime(), nullable=False)
    fire_start_time = db.Column(db.Time(), nullable=False)
    record_type = db.Column(db.String(10), nullable=False)

    def __init__(self, latitude, longitude, date_of_fire, fire_start_time, record_type):
        self.id
        self.latitude = latitude
        self.longitude = longitude
        self.date_of_fire = date_of_fire
        self.fire_start_time = fire_start_time
        self.record_type = record_type


@app.route('/SMS', methods=['POST'])
def psms():
    smsdata = request.get_json()
    stringtemp = smsdata["smsString"]
    value = smsdata["smsString"].rfind("(")
    valueEnd = smsdata["smsString"].rfind(")")
    finalValue = smsdata["smsString"][value+1:valueEnd]
    last = finalValue.split(",")
    print(last)

    latitude = last[0]
    longitude = last[1].lstrip()
    latitude = sum(float(x) / 60 ** n for n, x in enumerate(
        latitude[:-1].split(' '))) * (1 if 'N' in latitude[-1] else -1)
    longitude = sum(float(x) / 60 ** n for n, x in enumerate(
        longitude[:-1].split(' '))) * (1 if 'E' in longitude[-1] else -1)
    final_latitude = round(latitude, 4)
    final_longitude = round(longitude, 4)
    print(final_latitude, final_longitude)

    matchdate = re.search(r'\d{2}-\d{2}-\d{2}', stringtemp)
    matchtime = re.search(r'\d{2}:\d{2}:\d{2}', stringtemp)
    finaldate = matchdate.group()
    finaldate = datetime.strptime(
        finaldate, '%d-%m-%y').strftime("%Y-%m-%d %H:%M:%S")
    finaltime = matchtime.group()
    finaltime = datetime.strptime(finaltime, '%H:%M:%S').time()

    print(finaldate, finaltime)
    record_type = "S"
    print(record_type)
    msg = sms(latitude=final_latitude, longitude=final_longitude,
              date_of_fire=finaldate, fire_start_time=finaltime, record_type=record_type)
    db.session.add(msg)
    db.session.commit()

    return jsonify(smsdata)
