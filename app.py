from flask import Flask, render_template, redirect, request, flash, session

import sqlite3 


app = Flask(__name__)

@app.route('/hello')
def sayhello():
	return "say hello playas!"

@app.route('/show')
def name():
	connection = sqlite3.connect('test')
	# int dir(connection)
	# turn "working"
	cursor = connection.cursor()
	QUERY = "SELECT * FROM test"
	cursor.execute(QUERY)
	test = cursor.fetchall()
	# print dir(connection)
	return str(test)

@app.route('/input', methods=['GET'])
def form():

	return render_template("input.html")

@app.route('/submit', methods=['POST'])
def inputform():

	firstname = request.form["firstname"]
	connection = sqlite3.connect('test')
	# int dir(connection)
	# turn "working"
	cursor = connection.cursor()
	QUERY = "INSERT INTO test VALUES(?)"
	cursor.execute(QUERY, (firstname,))
	# print dir(connection)
	connection.commit()
	return redirect('/show')



if __name__== "__main__":
	app.run(debug = True)




