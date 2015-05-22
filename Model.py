from collections import OrderedDict
import datetime
import sys

from flask import Flask
from peewee import *
from flask_peewee.db import Database

DATABASE = {
    'name': 'tally.db',
    'engine': 'peewee.SqliteDatabase',
}

app = Flask(__name__)
app.config.from_object(__name__)


db = SqliteDatabase("tally.db")

class User(Model):
	user_login = CharField(max_length = 25)
	user_password = CharField(max_length = 25)

	class Meta:
		database = db

class Donor(Model):
	donor_id = PrimaryKeyField(primary_key = True)
	#I had to take  contact id out
	donor_contact_id = CharField(null = True)
	date_donor_added = DateField(null = True)
	# this needs to be a timestamp for new entries
	first_name = CharField(max_length = 40, null = True)
	last_name = CharField(max_length = 40, null = True)
	middle_name = CharField(max_length = 40, null = True)
	employer = CharField(max_length = 40, null = True)
	position = CharField(max_length = 40, null = True)

	class Meta:
		database = db
	
class Donor_contact(Model):
	donor_contact_id = PrimaryKeyField()
	#for new entries, I need to figure out a way for it to autoincrement
	donor_id = CharField(null = True)
	# date_contact_added = CharField()
	date_contact_added = DateField(null = True)
	# this needs to be a timestamp for new entries
	main_phone = CharField(max_length = 14, null = True)
	street_address = CharField(max_length = 200, null = True)
	state = CharField(max_length = 14, null = True)
	zip_code = CharField(max_length = 14, null = True)
	email = CharField(max_length = 14, null = True)

	class Meta:
		database = db

class Donor_note(Model):
	donor_note_id = PrimaryKeyField(primary_key= True)
	#for new entries, I need to figure out a way for it to autoincrement
	donor_id = CharField(null = True)
	date_note_added = DateField(null = True)
	# this needs to be a timestamp for new entries
	donor_note = TextField(null = True)

	class Meta:
		database = db

class Campaign(Model):
	auto_id = PrimaryKeyField()
	campaign_id = CharField(null = True)
	#for new entries, I need to figure out a way for it to autoincrement
	campaign_description = TextField(null = True)
	campaign_start_date = DateField(null = True)
	campaign_end_date = DateField(null = True)
	outreach_channel_one = CharField(max_length = 14, null = True)
	outreach_channel_two = CharField(max_length = 14, null = True)
	outreach_channel_three = CharField(max_length = 14, null = True)
	total_funds_raised = CharField(null = True)
	campaign_type = CharField(max_length = 40, null = True)

	class Meta:
		database = db

class Contribution(Model):
	contribution_id = PrimaryKeyField()
	#for new entries, I need to figure out a way for it to autoincrement
	campaign_id = CharField(null = True)
	# need to set this as a foreign key, was getting error message
	donor_id = CharField(null = True)
	# need to set this as a foreign key, was getting error message
	contribution_amount = CharField(null = True)
	date_of_contribution = DateField(null = True)
	payment_method = CharField(max_length = 14)
	date_acknowledgement_sent = DateField(null = True)
	contribution_note = TextField(null = True)

	class Meta:
		database = db



if __name__ == '__main__':
	db.connect
	db.create_tables([User, Donor, Donor_contact, Donor_note, Campaign, Contribution], safe = True)


	print "Database created"