from flask import Flask, render_template, request, json, jsonify, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(23)

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://<your_login>:<password>@db.4pn7x.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test

@app.route('/')
def home():
    if 'user' in session:
        # can be any user
        if session['user'] == 'admin@gmail.com':
            return render_template('page.html', data = db.test.find(), status = 'admin')
    return render_template('page.html', data = db.test.find(), status = None)
@app.route('/add', methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        print(db.test.insert_one(request.json))
        return db.test.insert_one(request.json) 
    return 'success' 

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        # print(request.form) 

# admin@gmail.com admin

        if request.form.get('login') == 'admin@gmail.com' and request.form.get('password') == 'admin':
            session['user'] = request.form.get('login')
            # return redirect(url_for(''))
            return redirect('/')



    else:
        if 'user' in session:
            return redirect('/')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/') 

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    
    if request.method == 'POST':
        id = request.json['id']
        db.test.delete_one({'_id' : ObjectId(id)})
        return 'success'
    return 'success'

if __name__ == '__main__':
    app.run(debug=True) 
