from flask import Flask, request, g
import time
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from json import dumps
from flask_jsonpify import jsonify

import src.estimator as mymodule
from collections import namedtuple
import json

import jxmlease

from flask_sqlalchemy import SQLAlchemy
import os
import backend.config as config


 

app = Flask(__name__)
api = Api(app)

CORS(app)

app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Logs(db.Model):
    __tablename__ = 'logs'


    id = db.Column(db.Integer, primary_key=True)
    httpmethod = db.Column(db.String)
    requestpath = db.Column(db.String)
    status = db.Column(db.String)
    timetook = db.Column(db.String)

    def __init__(self, httpmethod, requestpath, status, timetook):
        self.httpmethod = httpmethod
        self.requestpath = requestpath
        self.status = status
        self.timetook = timetook

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'httpmethod': self.httpmethod,
            'requestpath': self.requestpath,
            'status':self.status,
            'timetook':self.timetook

        }



db.create_all()





parser = reqparse.RequestParser()


@app.route('/')
def index():
    return "<h1>Welcome to Ian's server !!</h1>"
class Post_JsonData(Resource):  
    def post(self):
        
        parser.add_argument('region', type=str, location='json')
        parser.add_argument('periodType', type=str, location='json')
        parser.add_argument('timeToElapse', type=str, location='json')
        parser.add_argument('reportedCases', type=str, location='json')
        parser.add_argument('population', type=str, location='json')
        parser.add_argument('totalHospitalBeds', type=str, location='json')
        args = parser.parse_args() 

        region_data=str(args.region).replace("'", '"')
        args['region']= json.loads(region_data);

        result = mymodule.estimator(args)

        return jsonify(result)    

class Post_XmlData(Resource):  
    def post(self):
        
        parser.add_argument('region', type=str, location='json')
        parser.add_argument('periodType', type=str, location='json')
        parser.add_argument('timeToElapse', type=str, location='json')
        parser.add_argument('reportedCases', type=str, location='json')
        parser.add_argument('population', type=str, location='json')
        parser.add_argument('totalHospitalBeds', type=str, location='json')
        args = parser.parse_args() 

        region_data=str(args.region).replace("'", '"')
        args['region']= json.loads(region_data);

        result = mymodule.estimator(args)
        
        xml = jxmlease.emit_xml(result)
        print(xml)

        return  xml, 200, {'Content-Type': 'text/xml; charset=utf-8'} 

class Get_Logging(Resource):
    

    def get(self):
        mlogs = Logs.query.all()
        put_data = []
        for log in mlogs:
            put_data.append(f'{log.httpmethod}          {log.requestpath}               {log.status}          {log.timetook} ms  ')



        return  put_data, 200, {'Content-Type': 'text/plain; charset=utf-8'}        




log_info={}

@app.before_request
def before():
    g.start = time.time()
    log_info['method'] = request.method
    log_info['path'] = request.path

    

@app.after_request
def after(response):
    fn = g.get('fn', None)
    diff = int((time.time() - g.start) * 1000) 
    status=response.status_code 
    path = log_info['path']
    method = log_info['method']

    db.session.add(Logs(httpmethod=method, requestpath=path,status=status,timetook=str(diff)))
    db.session.commit()
    db.session.close()
    log_info.clear();
    return response









api.add_resource(Post_JsonData,'/api/v1/on-covid-19/json')
api.add_resource(Post_XmlData,'/api/v1/on-covid-19/xml')
api.add_resource(Get_Logging,'/api/v1/on-covid-19/logs')






if __name__ == '__main__':
    app.run(threaded=True,port=8000)