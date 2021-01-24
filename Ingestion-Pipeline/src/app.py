import json
import boto3
import os
# import requests
list_under_7 = []
list_under_10 = []


def read_file(bucket, file):
    s3 = boto3.client('s3')
    with open('/tmp/file.json', 'wb') as f:
        s3.download_fileobj(bucket, file, f)

    with open('/tmp/file.json') as json_file:
        data = json.load(json_file)

    return data


def average_and_count(data):
    count = 0
    total = 0
    under_7 = 0
    releve = []
    for key, value in data["notes"].items():
        total += value
        count += 1
        if value < 7:
            under_7 += 1
            list_under_7.append(key)
        elif 10 > value >= 7:
            list_under_10.append(key)
        matiere = { 'code_matiere': key, 'note': str(value) }
        releve.append(matiere)
    avg = total / count
    print(avg)
    return avg, under_7, releve


def result(under_7, avg, data, releve):
    credits = []
    ratt = []
    if under_7 < 2:
        if avg >= 10:
            student_result = 'adm'
        else:
            student_result = 'rat'
            ratt.extend(list_under_7)
            ratt.extend(list_under_10)
    elif under_7 == 2:
        if avg >= 10:
            student_result = 'admcr'
            credits.extend(list_under_7)
            credits.extend(list_under_10)
        else:
            student_result = 'rat'
            ratt.extend(list_under_7)
            ratt.extend(list_under_10)
    elif under_7 == 3:
        student_result = 'rat'
        ratt.extend(list_under_7)
        ratt.extend(list_under_10)
    else:
        student_result = 'rdb'
        if data["resultat_Precedent"] == "rdb":
            student_result = 'expl'
    result_object = {
        "matricule": data["matricule"],
        "annee": data["annee"],
        "nom": data["nom"],
        "prenom": data["prenom"],
        "resultat": student_result,
        "moyenne": str(avg),
        "releve": releve,

    }
    if credits:
        result_object["credits"] = credits
    if ratt:
        result_object["rattrapage"] = ratt
    list_under_7.clear()
    list_under_10.clear()
    return result_object


def dynamodb_put_object(object):
    table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    table.put_item(Item=object)


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    data = read_file(bucket_name, file_key)
    avg, count, releve = average_and_count(data)
    s_result = result(count, avg, data, releve)
    print(s_result)
    dynamodb_put_object(s_result)
