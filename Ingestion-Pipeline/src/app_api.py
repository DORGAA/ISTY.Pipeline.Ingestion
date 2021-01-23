import boto3
from flask import request, jsonify
from flask_lambda import FlaskLambda

app = FlaskLambda(__name__)


@app.route('/hello', methods=('GET',))
def create_list():
    return jsonify({"Result": "Hello world"}), 201


@app.route('/hello', methods=('POST',))
def create():
    return jsonify({"Result": "world"}), 201
