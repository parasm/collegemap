from flask import Flask, render_template, request, redirect
import jinja2
from pymongo import *
import os
from requests import *
import json

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
@app.route('/draw')
def draw():
	all_people = colleges.find({})
	r = get("https://maps.googleapis.com/maps/api/geocode/json?address=96+Davidson+Rd,+Piscataway+Township,+NJ&key=AIzaSyCd0-ydQhPpfKbjtIud0xUuoPw6kjbfvyk")
	data = json.loads(r.text)
	# for x in data['results']:
	# 	print x
	lat = data['results'][0]['geometry']['location']['lat']
	lon = data['results'][0]['geometry']['location']['lng']
	return render_template('draw.html',college_name=all_people[0]['college_name'],lat=lat,lon=lon)
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)
