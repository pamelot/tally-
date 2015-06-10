from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
# //import os - not sure why this might be needed for log-in

import sqlite3

import lazyload

from alchemymodel import User, Donor, Campaign, Contribution, db, connect_to_db

from sqlalchemy import *

from datetime import datetime, date


app = Flask(__name__)



# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined



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

@app.route('/donors', methods=['GET'])
def donor_home():

    return render_template("donors.html")


@app.route('/donors', methods=['POST'])
def donors_list():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    
    donors = Donor.query.filter_by(first_name=first_name, last_name=last_name).all()

    if not donors:
        flash("Donor does not exist. Please try again")
        return redirect('/donors')
    

    return render_template('donors_list.html', donors=donors, first_name=first_name, last_name=last_name)



@app.route('/donors/<int:donor_id>', methods=['GET'])
def donor_list_view(donor_id):

    donors = Donor.query.filter_by(donor_id = donor_id).all()
    for donor in donors:

        return render_template("donors_view.html", donors=donors)


@app.route ('/donors/<int:donor_id>', methods=['POST'])
def submit_edit_donor(donor_id):
    
    
    donors = Donor.query.filter_by(donor_id=donor_id).first()

    donor_change = Donor.query.get(donor_id)
    donor_change.first_name = request.form["first_name"]
    donor_change.last_name = request.form["last_name"]
    donor_change.middle_name = request.form["middle_name"]
    donor_change.employer = request.form["employer"]
    donor_change.position = request.form["position"]
    donor_change.email = request.form["email"]
    donor_change.main_phone = request.form["phone"]
    donor_change.street_address = request.form["street_address"]
    donor_change.city = request.form["city"]
    donor_change.state = request.form["state"]
    donor_change.zip_code = request.form["zip_code"]

    
    db.session.commit()
    flash("Donor has been updated.")
    # return redirect("/donors")


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

    new_donor = Donor(date_donor_added=date_donor_added, first_name=first_name, employer=employer, position=position, last_name=last_name, middle_name=middle_name, main_phone=main_phone, street_address=street_address, state=state, zip_code=zip_code, email=email)

    db.session.add(new_donor)
    db.session.commit()

    flash("Donor %s added." % first_name)
    return redirect("/home")

@app.route('/contributions', methods=['GET'])
def contribution_view():

    lists = Campaign.query.all()
    
    return render_template("contributions.html", lists=lists)

@app.route('/contributions', methods=['POST'])
def contributions_view():

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    

    donors = Donor.query.filter_by(first_name=first_name, last_name=last_name).all()
    lists = Campaign.query.all()

    if not donors:
        flash("Donor does not exist. Please try again")
        return redirect("/contributions")
    

    return render_template("contribution_list.html", donors=donors, first_name=first_name, last_name=last_name, lists=lists)

@app.route('/contributions/list', methods=['POST'])
def contributions_view_list():
     
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    search_field = request.form["search_field"]
    donors = Donor.query.filter_by(last_name=last_name, first_name=first_name).all()
    campaign_description = request.form["campaign_description"]
    
    if search_field == "first_last":

        for donor in donors:
            donor_id = donor.donor_id
            contributions = Contribution.query.filter_by(donor_id=donor_id)
            for contribution in contributions:
                full_date = datetime.strptime(contribution.date_of_contribution, "%Y-%m-%d %H:%M:%S")
                date = datetime.date(full_date)

            return render_template('existing_contribution_list.html', date=date, contributions=contributions)


    if search_field == "campaign":
         
        contributions = Contribution.query.filter_by(campaign_description=campaign_description).all()
        for contribution in contributions:
            full_date = datetime.strptime(contribution.date_of_contribution, "%Y-%m-%d %H:%M:%S")
            date = datetime.date(full_date)
            print full_date
            

            return render_template('existing_contribution_list.html', date=date, contributions=contributions)

    if search_field == "campaign_last":

        contributions = db.session.query(Contribution).join(Donor).filter(Donor.last_name == last_name).all()
        for contribution in contributions:
            full_date = datetime.strptime(contribution.date_of_contribution, "%Y-%m-%d %H:%M:%S")
            date = datetime.date(full_date)
            print date 
            print full_date
        return render_template('existing_contribution_list.html', date=date, contributions=contributions)

        
    if search_field == "campaign_first":
     
        contributions = db.session.query(Contribution).join(Donor).filter(Donor.first_name == first_name).all()
        for contribution in contributions:
            full_date = datetime.strptime(contribution.date_of_contribution, "%Y-%m-%d %H:%M:%S")
            date = datetime.date(full_date)
            
        return render_template('existing_contribution_list.html', date=date, contributions=contributions)



@app.route('/contributions/edit/<int:contribution_id>', methods=['GET'])
def edit_contribution_form(contribution_id):

    contributions = Contribution.query.filter_by(contribution_id=contribution_id).all()
    print contributions
    for contribution in contributions:
        donor_id = contribution.donor_id 
        donors = Donor.query.filter_by(donor_id=donor_id).all()
        lists = Campaign.query.all()
        campaign_id = contribution.campaign_id
        campaigns = Campaign.query.filter_by(campaign_id=campaign_id)
        

    return render_template("contributions_edit.html", contribution_id=contribution_id, donor_id=donor_id, campaigns=campaigns, contributions=contributions, donors=donors, lists=lists)

@app.route ('/contributions/edit/<int:contribution_id>', methods=['POST'])
def submit_edit_contribution_form(contribution_id):


    print "hi again"
    contribution_change = Contribution.query.get(contribution_id)
    contribution_change.campaign_description = request.form["campaign_description"]
    contribution_change.date_of_contribution = request.form["date_of_contribution"]
    contribution_change.contribution_amount = request.form["contribution_amount"]
    contribution_change.payment_method = request.form["payment_method"]
    contribution_change.date_acknowledgement_sent = request.form["date_acknowledgement_sent"]
    contribution_change.contribution_note = request.form["contribution_note"]

    db.session.commit()
    flash("Contribution has been added.")
    return redirect("/contributions")



@app.route("/contributions/<int:donor_id>", methods=['GET'])
def new_contribution_form(donor_id):
    
    lists = Campaign.query.all()
    donor = Donor.query.filter_by(donor_id=donor_id).first()
    donor_id = donor.donor_id
    
    return render_template("contributions_new.html", lists=lists, donor_id=donor_id, donor=donor)


@app.route('/contributions/<int:donor_id>', methods=['POST'])
def new_contribution_info(donor_id):

    donor_id = donor_id
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

    flash("Contribution has been added.")
    return redirect("/contributions")

@app.route('/campaigns', methods=['GET'])
def campaign_view():

    lists = Campaign.query.all()
    return render_template("campaigns.html", lists=lists)

@app.route('/campaigns', methods=['POST'])
def campaign_view_edit():

    campaign_id = request.form['campaign_id']
    campaigns = Campaign.query.filter_by(campaign_id=campaign_id).all()
    # return redirect("/campaigns/view")
    return render_template('campaign_view.html', campaigns=campaigns)

@app.route('/campaigns/view')

@app.route('/campaigns/new', methods=['GET'])
def new_campaign_form():

    return render_template("campaigns_new.html")

@app.route('/campaigns/new', methods=['POST'])
def new_campaign_info():


    campaign_description = request.form['campaign_description']
    campaign_start_date = request.form["campaign_start_date"]
    campaign_end_date = request.form["campaign_end_date"]
    total_funds_raised = request.form['total_funds_raised']

 
    new_campaign = Campaign(campaign_description=campaign_description, campaign_start_date=campaign_start_date, campaign_end_date=campaign_end_date, total_funds_raised=total_funds_raised)
    db.session.add(new_campaign)
    db.session.commit()

    flash("Campaign %s added." % campaign_description)
    return redirect("/home")

@app.route('/reports')
def report_view():

    return render_template("reports.html")

@app.route('/reports/topcontributions')
def top_contribution_view():

    contributions = db.session.query(Contribution).filter(Contribution.contribution_amount > 800).all()
    for contribution in contributions:
        contribution_amount = contribution.contribution_amount

    return render_template("top_contributions.html", contributions=contributions, contribution_amount=contribution_amount)

@app.route('/reports/campaign2014')
def campaign_report_2014():

    # campaigns = Campaign.query.all()
    # contributions = Contribution.query(Contribution.contribution_amount).group_by(Contribution.campaign_id)
    # for contribution in contributions:
    #     print contribtution 

    campaigns = Campaign.query.all()
    contribution_total_list = []
    for campaign in campaigns:
        campaign_id = campaign.campaign_id
        contributions = db.session.query(func.sum(Contribution.contribution_amount)).join(Campaign).filter(Contribution.campaign_id == campaign_id).all() 
        contributions = contributions[0][0]
        contribution_total_list.append(contributions)
   
    print contribution_total_list
        
        # for contribution in contributions:
        #     contribution_total = contribution[0]
        #     contribution_amount = contribution.contribution_amount
        #     print contribution_amount, campaign_id
        
    # donors = Donor.query.all()
    # for donor in donors:
    #     donor_id = donor.donor_id
    #     frequency_of_contributions = db.session.query(func.count(Contribution.donor_id)).filter(Contribution.donor_id==donor_id).all()
    #     frequency = frequency_of_contributions[0][0]
    #     first_name = donor.first_name
    #     last_name = donor.last_name
    #     if frequency_of_contributions > 2:
    #         print first_name, last_name, frequency



    

    return render_template("2014_campaign_report.html", contribution_total_list=contribution_total_list, campaigns=campaigns, contributions=contributions) 

@app.route('/reports/campaign2013')
def campaign_report_2013():

    return render_template("2013_campaign_report.html") 

# cursor = connection.cursor()
# QUERY = "INSERT INTO test VALUES(?)"
# cursor.execute(QUERY, (firstname,))
# 	# print dir(connection)
# 	connection.commit()
# 		return redirect('/show')

@app.route('/reports/frequent_donors')
def frequency_report():
    donors = Donor.query.all()
    for donor in donors:
        donor_id = donor.donor_id
        frequency_of_contributions = db.session.query(func.count(Contribution.donor_id)).filter(Contribution.donor_id==donor_id).all()
        frequency = frequency_of_contributions[0][0]
        print frequency_of_contributions

    return render_template("frequent_donors.html", donors=donors, frequency=frequency)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()

    


