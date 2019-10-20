"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    records_over_10 = Record.query.filter(Record.value >=10).all()
    return str(records_over_10)

# Function for part 2 of the sprint challenge
def measurements(city='Los Angeles', parameter='pm25'):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    return [(i['date']['utc'], i['value']) for i in body['results']]
    # to check the code from part one, add the following the root() function
    # display_data = measurements()
    # return str(display_data)

# Part 3
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '--- Date: {}, Value: {} --- \n'.format(self.datetime, self.value)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    data = measurements()
    for record in data:
        instance = Record(datetime=record[0], value=record[1])
        DB.session.add(instance)
    DB.session.commit()
    return 'Data refreshed!'
