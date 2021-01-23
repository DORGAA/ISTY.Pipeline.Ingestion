import boto3
from boto3.dynamodb.conditions import Key
from flask import request, jsonify
import decimal
import os
import flask.json
from flask_lambda import FlaskLambda
from flask_cors import CORS, cross_origin


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = FlaskLambda(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.json_encoder = MyJSONEncoder
student_table_name = os.environ["TABLE_NAME"]


@app.route('/hello', methods=('GET',))
@cross_origin()
def hello_world():
    return jsonify({"Result": "Hello world"}), 200


@app.route('/annee', methods=('GET',))
@cross_origin()
def annee():
    table = boto3.resource("dynamodb").Table(student_table_name)
    result = table.scan(AttributesToGet=['annee'])
    items = []

    items.extend(result["Items"])

    while "LastEvaluatedKey" in result:
        result = table.scan()
        items.extend(result["Items"])
    confs = []
    for item in items:
    	if item["annee"] not in confs:
        	confs.append(item["annee"])

    return jsonify(confs), 200


@app.route('/matricules/<annee>', methods=('GET',))
@cross_origin()
def matricules(annee):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.query(KeyConditionExpression=Key('annee').eq(annee))
    return jsonify(results["Items"]), 200


@app.route('/etudiant/<annee>/<matricule>', methods=('GET',))
@cross_origin()
def get_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.get_item(Key={"annee": annee, "matricule": matricule})
    return jsonify(results["Item"]), 200


@app.route('/etudiant/<annee>/<matricule>', methods=('DELETE',))
@cross_origin()
def delete_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.delete_item(Key={"annee": annee, "matricule": matricule})
    return jsonify(results["Item"]), 200

@app.route('/etudiant/<annee>/<matricule>', methods=('POST',))
@cross_origin()
def post_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    table.put_item(request.json)
    return jsonify(results["Item"]), 200
