from flask import Flask

app = Flask(__name__)


@app.route("/hello")
def hello():
    return {"result": "Hello World!"}
