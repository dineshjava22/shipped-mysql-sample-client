from bson import ObjectId
import os
import mysql.connector
from mysql.connector import errorcode

MYSQL_DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'testuser',
    'password': 'test',
    'database': 'test'
}

CREATE_TBL = "CREATE TABLE IF NOT EXISTS tbl_counter(id int PRIMARY KEY, counter INT DEFAULT 0);"
SEED_DATA = 'INSERT INTO tbl_counter(id, counter) VALUES(1, 0) ON DUPLICATE KEY UPDATE counter = counter + 1;'

id = 0
client = None

def dbConnection():
    deployTarget = os.environ.get('DEPLOY_TARGET')
    connConfig = {
        'host': os.environ.get(''),
        'user': os.environ.get('MYSQL_USER'),
        'password': os.environ.get('MYSQL_PASSWORD'),
        'database': os.environ.get('MYSQL_DATABASE')
    }
    if deployTarget == "LOCAL_SANDBOX":
        connConfig = MYSQL_DEFAULT_CONFIG

    print("Current deploy target %s" % deployTarget)
    try:
        client = mysql.connector.connect(**connConfig)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    return client

def setupDB():
    dbConnection()
    try:
        cursor = client.cursor()
        cursor.execute(CREATE_TBL)
        cursor.execute(SEED_DATA)
        id = cursor.lastrowid
    except mysql.connector.Error as err:
        print(err.msg)

    return id

def closeDB():
    client.close()
