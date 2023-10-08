
from flask import Flask ,request, make_response
import json
import pandas as pd
import numpy as np
import os
from flask_cors import  CORS, cross_origin
import pymysql
from flask import Flask
from flask import *

app = Flask(__name__)


USERNAME = 'root'
PASSWORD = 'password'
DATABASE = 'Employee'


cors = CORS
app.config['CORS_HEADERS'] = 'Content-Type'


def connect_db():
    return pymysql.connect(
        host="localhost", user = USERNAME, passwd = PASSWORD, database = DATABASE,
        autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_user',methods = ['GET'])      # get all users
@cross_origin(supports_credentials=True)
def getAllUser():
    try:
        cursor = connect_db().cursor()
        cursor.execute("SELECT name,company,jobTitle,phone,location,salary FROM users  WHERE deleted = '0' ")
        userRows = cursor.fetchall()
        resp = jsonify({'success': True, 'response': userRows})
        resp.status_code = 200
        return resp
    except Exception as ex:
        print(ex)
        resp = jsonify({'success': False, 'message': 'Some error occurred'})
        resp.status_code = 500
        return resp

@app.route('/register_user',methods = ['POST'])
@cross_origin(supports_credentials=True)
def register_user():
    try:
        data = request.json
        cursor = connect_db().cursor()
        check_user = "SELECT  name ,phone  FROM users WHERE phone = %s AND deleted = '0'"
        cursor.execute(check_user,(data['phone']))
        user_exist = cursor.fetchone()
        # print('user_exist    ------------ ',user_exist)
        if user_exist == None:
            sql = " INSERT INTO users (name,company,jobTitle,phone,location,salary) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,(data['name'],data['company'],data['jobTitle'],data['phone'],data['location'],data['salary']))
            cursor.connection.commit()
            insert = cursor.fetchone()
            print('insert',insert)
            resp = jsonify({'success': True, 'response': 'User registered SuccessFully'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'success': True, 'response': 'User Already Registered'})
            resp.status_code = 200
            return resp
    except Exception as ex:
        print('exception ',ex)
        resp = jsonify({'success': False, 'message': 'Some error occurred'})
        resp.status_code = 500
        return resp
    

@app.route('/update_user',methods = ['POST'])
@cross_origin(supports_credentials=True)
def update_user():
    try:
        data = request.json
        cursor = connect_db().cursor()
        update_sql = "UPDATE users SET name = %s,company = %s, jobTitle= %s, location = %s, salary = %s  WHERE id = %s AND phone = %s  AND deleted = '0' " 
        cursor.execute(update_sql,(data['name'],data['company'],data['jobTitle'],data['location'],data['salary'],data['id'],data['phone']))
        cursor.connection.commit()
        resp = jsonify({'success': True, 'response': 'User profile Updated Successfully'})
        resp.status_code = 200
        return resp
    except Exception as ex:
        print('exception ',ex)
        resp = jsonify({'success': False, 'message': 'Some error occurred'})
        resp.status_code = 500
        return resp
    


@app.route('/delete_user',methods = ['POST'])
@cross_origin(supports_credentials = True)
def delete_user():
    try:
        data = request.json
        cursor = connect_db().cursor()
        delete_sql = "UPDATE users SET deleted = 1 WHERE id = %s AND phone = %s"
        cursor.execute(delete_sql,(data['id'],data['phone']))    
        cursor.connection.commit()
        resp = jsonify({'success': True, 'response': 'profile removed'})
        resp.status_code = 200
        return resp
    except Exception as ex:
        print("exception ",ex)
        resp = jsonify({'success': False, 'message': 'Some error occurred'})
        resp.status_code = 500
        return resp



if __name__ == '__main__':
    app.run()
