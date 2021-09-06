from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os

from model import *


app = Flask(__name__)
api = Api(app)

app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

model = get_model()

class Pneumonia(Resource):
    def get(self):
        args = request.args
        fname = args['fname']

        return jsonify(dict(result=predict(fname, model)))

api.add_resource(Pneumonia, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)