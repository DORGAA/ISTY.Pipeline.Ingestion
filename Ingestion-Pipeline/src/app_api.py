import boto3
from boto3.dynamodb.conditions import Key
from flask import request, jsonify
import decimal
import flask.json
from flask_lambda import FlaskLambda

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = FlaskLambda(__name__)
app.json_encoder = MyJSONEncoder
student_table_name = 'isty-ingestion-table'


@app.route('/hello', methods=('GET',))
def hello_world():
    return jsonify({"Result": "Hello world"}), 201


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
        confs.append(item["annee"])

    return jsonify(confs), 201


@app.route('/matricules/<annee>', methods=('GET',))
def matricules(annee):
    table = boto3.resource("dynamodb").Table(student_table_name)
    results = table.query(KeyConditionExpression=Key('annee').eq(annee))
    return jsonify(results["Items"]), 201
