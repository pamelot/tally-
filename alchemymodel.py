from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref




# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_login = db.Column(db.String(64), nullable=False)
    user_password = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)


    def __repr__(self):
        """provide helpful representation when printed"""
        return "<User user_id=%s user_login=%s>" % (self.user_id, self.user_login)


class Donor(db.Model):
    
    __tablename__ = "donors"


    donor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_donor_added = db.Column(db.DateTime, nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    middle_name = db.Column(db.String(64), nullable=True)
    employer = db.Column(db.String(64), nullable=True)
    position = db.Column(db.String(64), nullable=True)
    main_phone = db.Column(db.String(64), nullable=True)
    street_address = db.Column(db.String(64), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    zip_code = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)

    contributionsd = relationship('Contribution', backref='donors')
    

    def __repr__(self):
        """provide helpful representation when printed"""
        return "<Donor donor_id=%s first_name=%s>" % (self.donor_id, self.first_name)


class Campaign(db.Model):
    
    __tablename__ = "campaigns"

    campaign_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_description = db.Column(db.String(64), nullable=True)
    campaign_start_date = db.Column(db.String(64), nullable=True)
    campaign_end_date = db.Column(db.String(64), nullable=True)
    outreach_channel_one = db.Column(db.String(64), nullable=True)
    outreach_channel_two = db.Column(db.String(64), nullable=True)
    outreach_channel_three = db.Column(db.String(64), nullable=True)
    total_funds_raised = db.Column(db.Integer, nullable=True)
    campaign_type = db.Column(db.String(64), nullable=True)

    contributionc = relationship('Contribution', backref='campaigns')

    def to_jsonc(self):
        print dict(campaign_id=self.campaign_id, campaign_description=self.campaign_description, campaign_start_date=self.campaign_start_date, campaign_end_date=self.campaign_end_date)

        return dict(campaign_id=self.campaign_id, campaign_description=self.campaign_description, campaign_start_date=self.campaign_start_date, campaign_end_date=self.campaign_end_date)
    
    def __repr__(self):
        """provide helpful representation when printed"""
        return "<Campaign campaign_id=%s campaign_description=%s>" % (self.campaign_id, self.campaign_description)

class Contribution(db.Model):
    
    __tablename__ = "contributions"

    contribution_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey ('campaigns.campaign_id'))
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.donor_id'))
    contribution_amount = db.Column(db.Integer, nullable=True)
    date_of_contribution = db.Column(db.String(64), nullable=True)
    payment_method = db.Column(db.String(64), nullable=True)
    date_acknowledgement_sent = db.Column(db.String(64), nullable=True)
    campaign_description = db.Column(db.String(64))
    contribution_note = db.Column(db.String(64), nullable=True)

    donorc = relationship("Donor", backref=backref('contributions'))

    campaignc = relationship("Campaign", backref=backref('campaigns'))

    def to_json(self):
        return dict(contribution_id=self.contribution_id, campaign_id=self.campaign_id, donor_id=self.donor_id, contribution_amount=self.contribution_amount, date_of_contribution=self.date_of_contribution, payment_method=self.payment_method, date_acknowledgement_sent=self.date_acknowledgement_sent, campaign_description=self.campaign_description, contribution_note=self.contribution_note)
    
    
    
    def __repr__(self):
        """provide helpful representation when printed"""
        return "<Contribution contribution_id=%s contribution_amount=%s>" % (self.contribution_id, self.contribution_amount)




##############################################################################
# Helper functions

def connect_to_db(app):
    # Connect the database to Flask app.

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tally.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from tallyServer import app
    connect_to_db(app)
    print "Connected to DB."
