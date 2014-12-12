from flask import Flask, render_template, request, redirect
import jinja2
from pymongo import *
import os
import requests
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
		raw_location = location.replace(' ','+')
		r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCd0-ydQhPpfKbjtIud0xUuoPw6kjbfvyk" % raw_location)
		data = json.loads(r.text)
		print 'paras' + location
		print data
		lat = data['results'][0]['geometry']['location']['lat']
		lon = data['results'][0]['geometry']['location']['lng']
		colleges.insert({'name':full_name.strip(),'college_name':college_name.strip(),'location':location.strip(),'cords':[lat,lon]})
		return redirect('/view')
	return render_template("add.html")
@app.route('/draw', methods=['GET', 'POST'])
def view():
	all_people = colleges.find({})
	return render_template("view.html",people=all_people)
@app.route('/view')
def draw():
	all_people = colleges.find({})
	raw_data = {}
	for person in all_people:
		raw_data[person['college_name']] = person['cords']
	# for loc in all_people:
	# 	raw_location = loc['location'].replace(' ','+')
	# 	r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyCd0-ydQhPpfKbjtIud0xUuoPw6kjbfvyk" % raw_location)
	# 	data = json.loads(r.text)
	# 	lat = data['results'][0]['geometry']['location']['lat']
	# 	lon = data['results'][0]['geometry']['location']['lng']
	# 	raw_data[loc['college_name']] = [lat,lon]
	return render_template('draw.html',data=json.dumps(raw_data),count=len(raw_data))


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)
