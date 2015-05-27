from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
# //import os - not sure why this might be needed for log-in

import sqlite3

from alchemymodel import User, Donor, Donor_contact, Donor_note, Campaign, Contribution, db, connect_to_db

from datetime import datetime

app = Flask(__name__)



# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



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

	user_name = request.form["username"]
	# password = 
	connection = sqlite3.connect('test')
	# int dir(connection)
	# turn "working"

@app.route('/login', methods=['GET'])
def login_form():

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():

    user_login = request.form["username"]
    user_password = request.form["password"]

    user = User.query.filter_by(user_login=user_login).first()

    if not user:
        flash("User does not exist. Please try again")
        return redirect("/login")

    if user.user_password != user_password:
        flash("Password is not correct. Please try again.")
        return redirect("/login")

    # session["user_id"] = user.user_id

    flash("You are logged in!")
    return redirect("/home")

@app.route('/home')
def homepage():
    
    return render_template("home.html")

@app.route('/donors')
def donor_view():

    return render_template("donors.html")


@app.route('/donors/new', methods=['GET'])
def new_donor_form():

    return render_template("donors_new.html")

@app.route('/donors/new', methods=['POST'])
def new_donor_info():

    date_donor_added = datetime.now()
    date_contact_added = date_donor_added
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    middle_name = request.form["middle_name"]
    email = request.form['email']
    main_phone = request.form['phone']
    street_address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip_code = request.form['zip_code']
    employer = request.form['employer']
    position = request.form['position']

    new_donor = Donor(date_donor_added=date_donor_added, first_name=first_name, employer=employer, position=position, last_name=last_name, middle_name=middle_name)
    new_donor_contact = Donor_contact(date_contact_added=date_contact_added, main_phone=main_phone, street_address=street_address, state=state, zip_code=zip_code, email=email)

    db.session.add(new_donor, new_donor_contact)
    db.session.commit()

    flash("Donor %s added." % first_name)
    return redirect("/home")

@app.route('/contributions')
def contribution_view():

    return render_template("contributions.html")

@app.route('/contributions/new', methods=['GET'])
def new_contribution_form():
    
    lists = Campaign.query.all()
    
    return render_template("contributions_new.html", lists=lists)

@app.route('/contributions/new', methods=['POST'])
def new_contribution_info():

    donor_id = request.form["donor_id"]
    campaign_id = request.form["campaign_id"]
    date_of_contribution = request.form["date_of_contribution"]
    campaign_type = request.form["campaign_type"]
    contribution_amount = request.form["contribution_amount"]
    payment_method = request.form["payment_method"]
    date_acknowledgement_sent = request.form["date_acknowledgement_sent"]
    contribution_note = request.form["contribution_note"]

    new_contribution = Contribution(donor_id=donor_id, campaign_id=campaign_id, date_of_contribution=date_of_contribution, contribution_amount=contribution_amount, payment_method=payment_method, date_acknowledgement_sent=date_acknowledgement_sent, contribution_note=contribution_note)
    

    db.session.add(new_contribution)
    db.session.commit()

    flash("Contribution for Donor %s has been added." % donor_id)
    return redirect("/home")


@app.route('/campaigns')
def campaign_view():

    return render_template("campaigns.html")


@app.route('/campaigns/new', methods=['GET'])
def new_campaign_form():

    return render_template("campaigns_new.html")

@app.route('/campaigns/new', methods=['POST'])
def new_campaign_info():


    campaign_type = request.form['campaign_type']
    campaign_description = request.form['campaign_description']
    campaign_start_date = request.form["campaign_start_date"]
    campaign_end_date = request.form["campaign_end_date"]
    outreach_channels = request.form[len('outreach_channel')].append('outreach_channel')
    total_funds_raised = request.form['total_funds_raised']
 
    new_campaign = Campaign(campaign_description=campaign_description, campaign_start_date=campaign_start_date, campaign_end_date=campaign_end_date, outreach_channel_one=outreach_channel_one, total_funds_raised=total_funds_raised, campaign_type=campaign_type)
    db.session.add(new_campaign)
    db.session.commit()

    flash("Campaign %s added." % campaign_description)
    return redirect("/home")

@app.route('/reports')
def report_view():

    return render_template("reports.html")

@app.route('/reports/topcontributions')
def top_contribution_view():

    contributions = Contribution.query.limit(100).all() 

    return render_template("top_contributions.html", contributions=contributions)

# cursor = connection.cursor()
# QUERY = "INSERT INTO test VALUES(?)"
# cursor.execute(QUERY, (firstname,))
# 	# print dir(connection)
# 	connection.commit()
# 		return redirect('/show')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()

    


