"""Utility file to seed tally database from donor/user data in Tally_generated_data/"""

from alchemymodel import User, Donor, Campaign, Contribution, connect_to_db, db
from tallyServer import app
from datetime import datetime

print 'hi'
def load_users():
   
    
    U = open("Tally_generated_data/users.csv")
    for line in U:
        line = line.split(",")
        user_login = line[1]
        user_password = line[2]

        user = User(user_login=user_login, user_password=user_password)
        
        db.session.add(user)

    db.session.commit()
  


def load_donors():
    
    D = open("Tally_generated_data/donor_details.csv")
    for line in D:
        line = line.rstrip()
        line = line.split(",")
        donor_id = line[0]
        d = line[1]
        date_donor_added = datetime.strptime(d,"%Y-%m-%d %H:%M:%S")
        first_name = line[2]
        last_name = line[3]
        middle_name = line[4]
        employer = line[5]
        position = line[6]
        main_phone = line[7]
        street_address = line[8]
        city = line[9]
        state = line[10]
        zip_code = line[11]
        email = line[12]

        donor = Donor(donor_id=donor_id, date_donor_added=date_donor_added, first_name=first_name, last_name=last_name, middle_name=middle_name, employer=employer, position=position, main_phone=main_phone, street_address=street_address, city=city, state=state, zip_code=zip_code, email=email)
      
        db.session.add(donor)

    db.session.commit()
        

def load_campaigns():

    CP = open("Tally_generated_data/campaigns.csv")
    for line in CP:
        line = line.rstrip()
        line = line.split(",")
        campaign_id = line[0]
        campaign_description = line[1]
        s = line[2]
        campaign_start_date = datetime.strptime(s,"%Y-%m-%d %H:%M:%S")
        e = line[3]
        campaign_end_date = datetime.strptime(e,"%Y-%m-%d %H:%M:%S")
        outreach_channel_one = line[4]
        outreach_channel_two = line[5]
        outreach_channel_three = line[6]
        total_funds_raised = line[7]
        campaign_type = line[8]


        campaign = Campaign(
            campaign_id=campaign_id,
            campaign_description=campaign_description,
            campaign_start_date=campaign_start_date,  
            campaign_end_date=campaign_end_date,
            outreach_channel_one=outreach_channel_one,
            outreach_channel_two=outreach_channel_two,
            outreach_channel_three=outreach_channel_three,
            total_funds_raised=total_funds_raised,
            campaign_type=campaign_type
            )
        db.session.add(campaign)

    db.session.commit()


def load_contributions():

    CO = open("Tally_generated_data/contributions.csv")
    for line in CO:
        line = line.rstrip()
        line = line.split(",")
        contribution_id = line[0]
        campaign_id = line[1]
        donor_id = line[2]
        contribution_amount = line[3]
        c = line[4]
        date_of_contribution = datetime.strptime(c,"%Y-%m-%d %H:%M:%S")
        payment_method = line[5]
        a = line[6]
        date_acknowledgement_sent = datetime.strptime(a,"%Y-%m-%d %H:%M:%S")
        contribution_note = line[7]
        campaign_description = line[8]
        


        contribution = Contribution(
            contribution_id=contribution_id,
            campaign_id=campaign_id,
            donor_id=donor_id,
            contribution_amount=contribution_amount,
            date_of_contribution=date_of_contribution,
            payment_method=payment_method,
            date_acknowledgement_sent=date_acknowledgement_sent,
            contribution_note=contribution_note,
            campaign_description=campaign_description
            )
        db.session.add(contribution)

    db.session.commit()


      

if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_donors()
    load_campaigns()
    load_contributions()


     