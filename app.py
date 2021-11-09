from flask import *
from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import date
import re
app = Flask(__name__)

app.config["SQLAlCHEMY_TRACK_NOTIFICATION"]=True
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"]=True

POSTGRES = {
     'user': 'postgres',
     'pw': 'karan123',
     'db': 'sms',
     'host': 'localhost',
     'port': '5434',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.debug=True
db= SQLAlchemy(app)


class sms(db.Model):
    __tablename__='SMS'
    latitude = db.Column(db.Float(),primary_key=True)
    longitude = db.Column(db.Float(),nullable=False)
    date = db.Column(db.String(),nullable=False)
    time = db.Column(db.String(),nullable=False)
    def __init__(self,latitude,longitude,date,time):
        self.latitude=latitude
        self.longitude=longitude
        self.date=date
        self.time=time



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
    latitude = sum(float(x) / 60 ** n for n, x in enumerate(latitude[:-1].split(' ')))  * (1 if 'N' in latitude[-1] else -1)
    longitude = sum(float(x) / 60 ** n for n, x in enumerate(longitude[:-1].split(' ')))  * (1 if 'E' in longitude[-1] else -1)
    print(latitude,longitude)
    matchdate= re.search(r'\d{2}-\d{2}-\d{2}', stringtemp)
    matchtime= re.search(r'\d{2}:\d{2}:\d{2}', stringtemp)
    finaldate=matchdate.group()
    finaltime=matchtime.group()
    print(finaldate,finaltime)

    msg= sms(latitude=latitude,longitude=longitude,date=finaldate,time=finaltime)
    db.session.add(msg)
    db.session.commit()

    return jsonify(smsdata)





