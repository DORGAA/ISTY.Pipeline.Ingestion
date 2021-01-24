import boto3
from boto3.dynamodb.conditions import Key
from flask import request, jsonify
import decimal
import os
import flask.json
import json
from flask_lambda import FlaskLambda


class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = FlaskLambda(__name__)
app.json_encoder = MyJSONEncoder
student_table_name = os.environ["TABLE_NAME"]


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Api-Key')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  response.headers.add('Content-Type', 'application/json')
  return response


@app.route('/hello', methods=('GET',))
def hello_world():
    return jsonify({"Result": "Hello world"}), 200


@app.route('/annee', methods=('GET',))
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
def matricules(annee):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.query(KeyConditionExpression=Key('annee').eq(annee))
    return jsonify(results["Items"]), 200


@app.route('/etudiant/<annee>/<matricule>', methods=('GET',))
def get_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.get_item(Key={"annee": annee, "matricule": matricule})
    if "Item" in results:
    	return jsonify(results["Item"]), 200
    else:
    	return jsonify({}), 200


@app.route('/etudiant/<annee>/<matricule>', methods=('DELETE',))
def delete_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.delete_item(Key={"annee": annee, "matricule": matricule})
    return jsonify({"delete": f"{annee}-{matricule}"}), 200


@app.route('/etudiant/<annee>/<matricule>', methods=('POST',))
def post_etudiant(annee, matricule):
    table = boto3.resource("dynamodb").Table(student_table_name)
    table.put_item(Item=request.json)
    return jsonify({"insert":request.json}), 200
