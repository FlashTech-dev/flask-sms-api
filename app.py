from flask import *
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config["SQLAlCHEMY_TRACK_NOTIFICATION"]=True
# app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"]=False

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'karan123',
#     'db': 'test',
#     'host': 'localhost',
#     'port': '5434',
# }
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#app.debug=True
#db= SQLAlchemy(app)


#class sms(db.Model):
   # __tablename__='SMS'
   # smsString=db.Column(db.String(),nullable=False,primary= True)
   # def __init__(self,smsString):
        #self.latitude= latitude
        #self.longitude=longitude
    #    self.smsString=smsString


@app.route('/SMS',methods=['POST'])
def psms():
    smsdata=request.get_json()
   # msg=sms(smsString=smsdata['smsString'])
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
    return jsonify(smsdata)





