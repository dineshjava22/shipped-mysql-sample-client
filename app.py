from flask import Flask, render_template
from bson import ObjectId
from utils import *

import json

app = Flask(__name__)
id = 0

@app.route("/")
def hello():
    id = setupDB()
    db = dbConnection()
    cursor = db.cursor()
    query = "SELECT counter FROM tbl_counter WHERE id = %d"
    cursor.execute(query, (id))
    for counter in cursor:
        return render_template("index.html", count=counter)

@app.route("/count",  methods=['GET'])
def getData():
    db = dbConnection()
    cursor = db.cursor()
    query = "SELECT counter FROM tbl_counter WHERE id = %d"
    cursor.execute(query, (id))
    for counter in cursor:
        return render_template("index.html", count=counter)

@app.route("/like",  methods=['POST'])
def postData():
    db = dbConnection()
    cursor = db.cursor()
    updateSql = "UPDATE tbl_counter SET counter = counter + 1 WHERE id = %d"
    cursor.execute(updateSql, (id))
    
    query = "SELECT counter FROM tbl_counter WHERE id = %d"
    cursor.execute(query, (id))
    for counter in cursor:
        return render_template("index.html", count=counter)

@app.route("/reset",  methods=['POST'])
def resetData():
    db = dbConnection()
    cursor = db.cursor()
    updateSql = "UPDATE tbl_counter SET counter = 0 WHERE id = %d"
    cursor.execute(updateSql, (id))
    
    query = "SELECT counter FROM tbl_counter WHERE id = %d"
    cursor.execute(query, (id))
    for counter in cursor:
        return render_template("index.html", count=counter)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')




