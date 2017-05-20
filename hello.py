from flask import Flask
from flask import jsonify
from flask import request
import pymysql
pymysql.install_as_MySQLdb()
from geopy.distance import great_circle

connection = pymysql.connect(host='',
                             user='',
                             password='',
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



app = Flask(__name__)

@app.route("/airports")
def searchRadius():
    try:
        with connection.cursor() as cursor:
            lat = request.args.get('lat')
            lng = request.args.get('long')
            rad = request.args.get('r')
            sql = "select *, ( 6371 * acos( cos( radians(" + lat + ") ) * cos( radians( Airports.latitude ) ) * cos( radians(Airports.longitude) - radians(" + lng + ")) + sin(radians(" + lat + ")) * sin( radians(Airports.latitude)))) AS distance from Airports HAVING distance < " + rad + " ORDER BY distance;"
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
    finally: 
        asdf = "1"

    return jsonify(result)

@app.route("/distance")
def findDistance():
    try:
        with connection.cursor() as cursor:
            apid1 = request.args.get('apid1')
            apid2 = request.args.get('apid2')
            sql1 = "select * from Airports where id=" + apid1 + " limit 1;"
            sql2 = "select * from Airports where id=" + apid2 + " limit 1;"
            cursor.execute(sql1)
            connection.commit()
            result = cursor.fetchone()
            cursor.execute(sql2)
            connection.commit()
            result2 = cursor.fetchone()
            return jsonify(great_circle((result['latitude'], result['longitude']), (result2['latitude'], result2['longitude'])).kilometers)
    finally: 
        asdf = "1"


@app.route("/countries")
def findCountries():
    try:
        with connection.cursor() as cursor:
            c1 = request.args.get('c1')
            c2 = request.args.get('c2')
            sql1 = "SELECT * FROM `Airports` AS `Airports` WHERE `Airports`.`country` = '" + c1 + "';"
            sql2 = "SELECT * FROM `Airports` AS `Airports` WHERE `Airports`.`country` = '" + c2 + "';"
            cursor.execute(sql1)
            connection.commit()
            result = cursor.fetchall()
            cursor.execute(sql2)
            connection.commit()
            result2 = cursor.fetchall()
            minDist = 99999999
            f1 = ''
            f2 = ''
            for r in result:
                for s in result2:
                    tmpDist = great_circle((r['latitude'], r['longitude']), (s['latitude'], s['longitude'])).kilometers
                    if tmpDist < minDist:
                        f1 = r
                        f2 = s
                        minDist = tmpDist
            return jsonify(f1, f2)
    finally: 
        asdf = "1"
    
if __name__ == "__main__":
    app.run()
