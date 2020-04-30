



from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy 
from flask import request , jsonify , abort


from datetime import datetime



import os 
basedir = os.path.abspath(os.path.dirname(__file__))
db_file = 'sqlite:///' + os.path.join(basedir,'bucketlist')

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= db_file 
app.config['SQL_TRACK_MODIFICATIONS']= False 
db = SQLAlchemy(app)






class BucketList(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(255))
    topic_by = db.Column(db.String(100))
    created_date = db.Column(db.DateTime,nullable= False,default = datetime.now())

    def __init__(self,topic,topic_by):
        self.topic=topic
        self.topic_by=topic_by      


    def save(self):
        db.session.add(self)
        db.session.commit()


    @staticmethod
    def get_all():
        return BucketList.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.topic)




@app.route('/api/v1/bucketlist/',methods=["POST","GET"])
def get_bucketlist():
    if request.method == "POST":
        topic = (request.data.get('topic',''))
        topic_by = (request.data.get('topic_by',''))
       
        bucketlist = BucketList(topic=topic,topic_by=topic_by)
        bucketlist.save()
        response = jsonify({'id' : bucketlist.id,'topic' : bucketlist.topic,'topic_by': bucketlist.topic_by,'created_date': bucketlist.created_date })

        response.status_code = 201
        return response

    else:
        bucketlists = BucketList.get_all()
        results = []
        for bucketlist in bucketlists : 
            obj = {
                'id' : bucketlist.id,
                'topic' : bucketlist.topic,
                'topic_by': bucketlist.topic_by,
                'created_date': bucketlist.created_date
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
        

    return app







