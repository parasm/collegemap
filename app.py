from flask import Flask, render_template, request, redirect
import jinja2
from pymongo import *
import os

app = Flask(__name__)

app.secret_key = 'bkvwrkhgbhwrng'
client = MongoClient('mongodb://admin:kobenevermisses@linus.mongohq.com:10083/collegemap')
db = client.get_default_database()
colleges = db.colleges

@app.route('/')
def hello():
	return render_template("index.html")
@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		full_name = request.form.get('name')
		college_name = request.form.get('college_name')
		location = request.form.get('location')
		if not(full_name):
			return render_template('add.html',error="Cannot leave name blank!")
		if not(college_name):
			return render_template('add.html',error="Cannot leave college name blank")
		if not(location):
			return render_template('add.html',error="Cannot leave location blank")
		colleges.insert({'name':full_name,'college_name':college_name,'location':location})
		return redirect('/view')
	return render_template("add.html")
@app.route('/view', methods=['GET', 'POST'])
def view():
	all_people = colleges.find({})
	return render_template("view.html",people=all_people)
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)
