from flask import Flask, render_template, request, redirect
import jinja2
from pymongo import *
import os
import requests
import json
import facebook
from bs4 import BeautifulSoup

app = Flask(__name__)

app.secret_key = 'bkvwrkhgbhwrng'
client = MongoClient('mongodb://admin:kobenevermisses@linus.mongohq.com:10083/collegemap')
db = client.get_default_database()
colleges = db.colleges
paras_token = "CAALtvWRP9p8BAGQFRooVNC4OpFZCfs5q03NHtncjfP3ddd1lork1mKEGbEj15Jg1eznte0WdPZC6ZA1IbZBthMZChInFkrHJXoHUhmGa0qDfN9gPrro2zb235VR8ZBbMk9g8zGklxZBUB52cZAV7H3MwlmSZAmlBQ7RxZA1algYqoUje9O0DlYqzA0IUD5QoWvtgkZD"
@app.route('/bca')
def bca():
	# print request.cookies
	# user = facebook.get_user_from_cookie(request.cookies,'824347640985247','7b0817e9466cf8265817533e382be0c6')
	# if user:
		# r = requests.get("https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=824347640985247&client_secret=7b0817e9466cf8265817533e382be0c6&fb_exchange_token=" + user.get('access_token'))
		# long_token = r.text.split('access_token=')[1].replace('&expires=5183952','')
	# graph = facebook.GraphAPI(paras_token)
	# profile = graph.get_object("me")
	# print profile
	# college_doc = graph.get_object('785762128126876/docs').get('data')[0].get('message')
	# #print college_doc
	# parsed_data = college_doc.split('<br />')
	# for raw in parsed_data:
	# 	soup = BeautifulSoup(raw)
	# 	colleges.insert({'college':soup.p,'raw_data':parsed_data})
	# 	print 'College: ' + str(soup.p)
	#print dir(soup)
	return render_template("index.html")
@app.route('/')
def hello():
	return render_template("bens_page.html")
@app.route('/bca/add', methods=['GET', 'POST'])
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
		lat = data['results'][0]['geometry']['location']['lat']
		lon = data['results'][0]['geometry']['location']['lng']
		colleges.insert({'name':full_name.strip(),'college_name':college_name.strip(),'location':location.strip(),'cords':[lat,lon]})
		return redirect('/bca/view')
	return render_template("add.html")
@app.route('/bca/draw', methods=['GET', 'POST'])
def view():
	all_people = colleges.find({})
	return render_template("view.html",people=all_people)
@app.route('/bca/view')
def draw():
	all_people = colleges.find({})
	raw_data = {}
	for person in all_people:
		raw_data[person['college_name']] = person['cords']
	return render_template('draw.html',data=json.dumps(raw_data),count=len(raw_data))


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)
