from enum import unique
from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime
import re
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)

app.config["SQLAlCHEMY_TRACK_NOTIFICATION"]=True
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"]=True

POSTGRES = {
     'user': 'postgres',
     'pw': 'prem0409',
     'db': 'forestfiresimulation',
     'host': 'localhost',
     'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.debug=True
db= SQLAlchemy(app)


class sms(db.Model):
    __tablename__='data_entry'
    id = Column(Integer, Sequence('data_sequence'), primary_key=True)
    latitude = db.Column(db.Float(),nullable=False)
    longitude = db.Column(db.Float(),nullable=False)
    date_of_fire = db.Column(db.DateTime(),nullable=False)
    fire_start_time = db.Column(db.Time(),nullable=False)
    def __init__(self,latitude,longitude,date_of_fire,fire_start_time):
        self.id
        self.latitude=latitude
        self.longitude=longitude
        self.date_of_fire=date_of_fire
        self.fire_start_time=fire_start_time



@app.route('/SMS',methods=['POST'])
def psms():
    smsdata=request.get_json()
    stringtemp=smsdata["smsString"]
    value=smsdata["smsString"].rfind("(")
    valueEnd=smsdata["smsString"].rfind(")")
    finalValue=smsdata["smsString"][value+1:valueEnd]
    last=finalValue.split(",")
    print(last)
    latitude=last[0]
    longitude=last[1].lstrip()    
    # latitude = sum(float(x) / 60 ** n for n, x in enumerate(latitude[:-1].split(' ')))  * (1 if 'N' in latitude[-1] else -1)
    # longitude = sum(float(x) / 60 ** n for n, x in enumerate(longitude[:-1].split(' ')))  * (1 if 'E' in longitude[-1] else -1)
    print(latitude,longitude)
    matchdate= re.search(r'\d{2}-\d{2}-\d{2}', stringtemp)
    matchtime= re.search(r'\d{2}:\d{2}:\d{2}', stringtemp)
    finaldate=matchdate.group()
    finaldate=datetime.strptime(finaldate,'%d-%m-%y').strftime("%Y-%m-%d %H:%M:%S")
    finaltime=matchtime.group()
    finaltime = datetime.strptime(finaltime,'%H:%M:%S').time()

    print(finaldate,finaltime)

    msg= sms(latitude=latitude,longitude=longitude,date_of_fire=finaldate,fire_start_time=finaltime)
    db.session.add(msg)
    db.session.commit()

    return jsonify(smsdata)





