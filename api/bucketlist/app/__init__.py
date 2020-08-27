



from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy 
from flask import request , jsonify , abort , make_response
from flask import Blueprint
from flask.views import MethodView

from flask_migrate import Migrate 


from datetime import datetime



import os 
basedir = os.path.abspath(os.path.dirname(__file__))
db_file = 'sqlite:///' + os.path.join(basedir,'bucketlist')

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= db_file 
app.config['SQL_TRACK_MODIFICATIONS']= False 
db = SQLAlchemy(app)
migrate = Migrate(app,db)


auth_blueprint = Blueprint('auth',__name__)



from app.models import BucketList , User


from flask_bcrypt import Bcrypt

@app.route('/api/v1/bucketlist/',methods=["POST","GET"])
def get_bucketlist():
    #get access tocken from header
    auth_header = request.headers.get('Authorization')
    
    access_token = auth_header.split(" ")[1]
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id,str):
            if request.method == "POST":
                topic = str(request.data.get('topic',''))
                topic_by = str(request.data.get('topic_by',''))
                if topic:
                    bucketlist = BucketList(topic=topic,topic_by=topic_by,created_by=user_id)
                    bucketlist.save()
                    response = jsonify({'id' : bucketlist.id,'topic' : bucketlist.topic,
                            'topic_by': bucketlist.topic_by,'created_date': bucketlist.created_date,
                            'date_modified':bucketlist.date_modified , 'created_by': user_id})         
                    return make_response(response) , 201

            else:
                bucketlists = BucketList.get_all()
                results = []
                for bucketlist in bucketlists :
                    obj = {
                        'id' : bucketlist.id,
                        'topic' : bucketlist.topic,
                        'topic_by': bucketlist.topic_by,
                        'created_date': bucketlist.created_date,
                        'date_modified':bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    results.append(obj)        
                return make_response(jsonify(results)),200
        else :
            message = user_id
            response ={
                'message': message
            }
            return make_response(jsonify(response)), 401

@app.route('/api/v1/bucketlist/<int:id>',methods=["PUT","GET","DELETE"])
def modify_bucketlist(id,**kwargs):

    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    if access_token:
        user_id = User.decode_token(access_token)
        if not isinstance(user_id,str):
            bucketlist = BucketList.query.filter_by(id=id).first()
            if not bucketlist:
                abort(404)

            if request.method == "DELETE":
                bucketlist.delete()
                return {
                    "message" : "bucketlist {} deleted successfully".format(bucketlist.id)
                        }
    
            elif request.method == "PUT":
                
                topic = str(request.data.get('topic',''))
                topic_by = str(request.data.get('topic_by',''))
                bucketlist.topic = topic
                bucketlist.topic_by = topic_by
                bucketlist.save()

                response = {
                    'id' : bucketlist.id,
                    'topic' : bucketlist.topic,
                    'topic_by': bucketlist.topic_by,
                    'created_date': bucketlist.created_date,
                    'date_modified':bucketlist.date_modified,
                    'created_by': bucketlist.created_by

                }
         
                return make_response(jsonify(response)), 200
    
            else :

                response = {
                    'id' : bucketlist.id,
                    'topic' : bucketlist.topic,
                    'topic_by': bucketlist.topic_by,
                    'created_date': bucketlist.created_date,
                    'date_modified':bucketlist.date_modified,
                    'created_by': bucketlist.created_by

                 }         
                return make_response(jsonify(response)), 200
        else:

            message = user_id
            response = {
                'message': message
                }
                # return an error response, telling the user he is Unauthorized
            return make_response(jsonify(response)), 401

from .auth import auth_blueprint
app.register_blueprint(auth_blueprint)


