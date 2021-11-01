from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLAlCHEMY_TRACK_NOTIFICATION"]=True
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"]=False

POSTGRES = {
    'user': 'postgres',
    'pw': 'karan123',
    'db': 'test',
    'host': 'localhost',
    'port': '5434',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.debug=True
db= SQLAlchemy(app)


class sms(db.Model):
    __tablename__='SMS'
    latitude=db.Column(db.Integer(), nullable=False, primary_key=True )
    longitude=db.Column(db.Integer(), nullable=False)
    smsString=db.Column(db.String(),nullable=False)
    def __init__(self,latitude,longitude,smsString):
        self.latitude= latitude
        self.longitude=longitude
        self.smsString=smsString

@app.route('/test',methods=['GET'])
def test():
    return {
        'test':'test1'
    }

@app.route('/SMS',methods=['POST'])
def psms():
    smsdata=request.get_json()
    msg=sms(latitude=smsdata['latitude'],longitude=smsdata['longitude'],smsString=smsdata['smsString'])
    db.session.add(msg)
    db.session.commit()
    return jsonify(smsdata)
