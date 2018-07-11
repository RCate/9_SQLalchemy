import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///titanic.sqlite")
engine = create_engine('sqlite:///Hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
hawaii_measurement = Base.classes.Hawaii_measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/enterstartdate<br/>"
        f"/api/v1.0/enterstartdate/enterenddate<br/>"
    )


@app.route("/api/v1.0/precipitation")
def date_and_temp():
     # Query all precipitation
    last_12_months = session.query(hawaii_measurement.date, hawaii_measurement.prcp).filter(hawaii_measurement.date > '2016-08-23').all()
# Convert list of tuples into normal list
    prcp = list(np.ravel(last_12_months))
    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    all_stations = session.query(hawaii_measurement.station).group_by(hawaii_measurement.station).all()
# Convert list of tuples into normal list
    stations = list(np.ravel(all_stations))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temperatures"""
    # Query all tobs
    results = session.query(hawaii_measurement.date, hawaii_measurement.tobs).filter(hawaii_measurement.date > '2016-08-23').filter(hawaii_measurement.station == 'USC00519281').all()
 # Create a dictionary from the row data and append to tuples into normal list
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def date(start):

    date = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= start).all()
    return jsonify(date) 
@app.route("/api/v1.0/<start>/<end_date>")
def two_date(start, end_date):

    Two_dates = session.query(func.min(hawaii_measurement.tobs), func.avg(hawaii_measurement.tobs), func.max(hawaii_measurement.tobs)).\
        filter(hawaii_measurement.date >= start).filter(hawaii_measurement.date <= end_date).all()
    return jsonify(Two_dates) 

if __name__ == '__main__':
    app.run(debug=True)
