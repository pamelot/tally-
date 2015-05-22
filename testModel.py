from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

DB_URI = "sqlite:///tally.db"

db = SQLAlchemy()

Model = declarative_base()

class Users(db.Model):

	__tablename__ = 'users'

	user_id = db.Column(db.String(50), primary_key=True)
	user_password = db.Column(db.String(50))

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tally.db'
    # db.app = app
    app = db.app 
    db.init_app(app)

 

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.



    print "Connected to DB."