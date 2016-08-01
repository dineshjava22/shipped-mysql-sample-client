from flask import Flask, render_template
from utils import *

import json

app = Flask(__name__)
id = []


setupDB()

@app.route("/")
def hello():
    db = dbConnection()
    i = getValue(db)
    return render_template("index.html", count=i)


@app.route("/count", methods=['GET'])
def getData():
    db = dbConnection()
    i = getValue(db)
    db.close()
    return render_template("index.html", count=i)


@app.route("/like", methods=['POST'])
def postData():
    db = dbConnection()
    i = getValue(db)
    setValue(db, i + 1)

    return render_template("index.html", count=i)


@app.route("/reset", methods=['POST'])
def resetData():
    db = dbConnection()
    setValue(db, 0)
    return render_template("index.html", count=0)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
