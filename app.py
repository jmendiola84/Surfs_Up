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
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurements
Station = Base.classes.stations

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
        f"/api/v1.0/stations</br>"
		f"/api/v1.0/tobs</br>"
		f"/api/v1.0/<start></br>"
		f"/api/v1.0/<start>/<end>"
		)
	


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of precipitation information"""
    # Query for the dates and temperature observations from the last year
    date = dt.datetime(2016, 8, 23)
    
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date).group_by(Measurement.date).order_by(Measurement.date).all()
	
    prec_data = []
    
    for prec in results:
        prcp_dict = {}
        prcp_dict[prec.date] = prec.prcp
        prec_data.append(prcp_dict)

    return jsonify(prec_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a dictionary of temperature observations"""
    # Query for the dates and temperature observations from the last year
    date = dt.datetime(2016, 8, 23)
    
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date).group_by(Measurement.date).order_by(Measurement.date).all()
	
    tobs_data = []
    
    for tobs in results:
        tobs_dict = {}
        tobs_dict[tobs.date] = tobs.tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_st(start):
    """Return a dictionary of temperature observations"""
    # Query for the dates and temperature observations from the last year
    min_tmp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all()
    max_tmp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all()
    avg_tmp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all()
    return min_tmp, max_tmp, avg_tmp

@app.route("/api/v1.0/<start>/<end>")
def temp_st_end(start, end):
    min_tmp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all()
    max_tmp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all()
    avg_tmp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all()
    return min_tmp, max_tmp, avg_tmp



if __name__ == '__main__':
    app.run(debug=True)