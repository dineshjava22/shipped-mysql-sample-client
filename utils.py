import MySQLdb
from bson import ObjectId
from urlparse import urlparse
import os

MYSQL_URI = "mysql://mysql:mysql@localhost:3306/mysqlDB"

def dbConnection():
    deployTarget = os.environ.get('DEPLOY_TARGET')
    constr = os.environ.get('HOST_MYSQL_SINGLE')
    for i in range(0, 10):
        if i > 0:
            print("DB connection attempt %d of 10 failed; retrying connect string (%s)".format(i, constr))

        if deployTarget == "LOCAL_SANDBOX" or constr is None:
            constr = MYSQL_URI

        try:
            result = urlparse(constr)
            client = MySQLdb.connect(host=result.hostname,
                                     user=result.username,
                                     passwd=result.password,
                                     db=result.path[1:].split("?")[0])
            return client
        except Exception as err:
            print(err, constr)


def checkTableExists(dbcon, tablename):
    print ("check table %s" % tablename)
    dbcur = dbcon.cursor()
    dbcur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False


def createTable(dbcon, tablename):
    dbcur = dbcon.cursor()
    sql = '''CREATE TABLE {0} (
       vote int DEFAULT 0
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''.format(tablename)
    try:
        dbcur.execute(sql)
        dbcur.execute("insert into vote value (0)")
        dbcon.commit()
    except Exception as e:
        pass
    dbcur.close()


def getValue(dbcon):
    sql = "SELECT vote FROM vote LIMIT 1"
    dbcur = dbcon.cursor()
    dbcur.execute(sql)
    r = dbcur.fetchone()
    print "get count: %s" % r
    dbcur.close()
    return r[0]


def setValue(db, val):
    sql = "update vote set vote= %s" % val
    print "set count: %s" % sql
    dbcur = db.cursor()
    dbcur.execute(sql)
    dbcur.close()
    db.commit()



def setupDB():
    db = dbConnection()

    if checkTableExists(db, "vote"):
        getValue(db)
    else:
        createTable(db, "vote")
        setValue(db, 0)
    db.close()

