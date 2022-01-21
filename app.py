#import necessary library
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from security import authenticate, identity
from flask_jwt import JWT, jwt_required, current_identity

#configuring your application
app = Flask(__name__)
app.secret_key = b'\xab\xf7P~\x008 L\x91ln\xc4\x91\x98J\xa2'

#Creating our Api
api = Api(app)

jwt = JWT(app, authenticate, identity)

