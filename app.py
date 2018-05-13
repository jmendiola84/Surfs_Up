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
engine = create_engine("sqlite:///hawaii.sqlite",connect_args={'check_same_thread':False})

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
        f"<style> table, th, td {{ border: 1px solid black; border-collapse: collapse;}} </style>"
        f"<h1 align=\"center\"><b>HAWAII CLIMATE API</b></h1>"
        f"<table style=\"width:100%\">"
        f"<tr>"
        f"<th align=\"left\">Available Routes</th>"
        f"<th align=\"left\">Description</th>"
        f"</tr>"
        f"<tr>"
        f"<td>/api/v1.0/precipitation</td>"
        f"<td>Return a json list of precipitation data in Hawaii from 08/23/2016 to 08/23/2017.</td>"
        f"</tr>"
        f"<tr>"
        f"<td>/api/v1.0/stations</td>"
        f"<td>Return a json list of Hawaii weather stations</td>"
        f"</tr>"
        f"<tr>"
		f"<td>/api/v1.0/tobs</td>"
		f"<td>Return a json list of Temperature Observations in Hawaii from 08/23/2016 to 08/23/2017.</td>"		
		f"</tr>"
        f"<tr>"
		f"<td>/api/v1.0/[start-date]</td>"
        f"<td>Json list of minimum, average, and max temperature for a given start date (data available: 01/01/2010 - 08/23/2017)</td>"
		f"</tr>"
        f"<tr>"
        f"<td>/api/v1.0/[start-date]/[end-date]</td>"
        f"<td> Json list of minimum, average, and max temperature for a start-end date range (data available: 01/01/2010 - 08/23/2017)</td>"
        f"</tr>"
        f"</table>"
		)
	


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of precipitation information"""
    # Query for the dates and temperature observations from the last year
    date_prcp = dt.datetime(2016, 8, 23)
    
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > date_prcp).group_by(Measurement.date).order_by(Measurement.date).all()
	
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
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a dictionary of temperature observations"""
    # Query for the dates and temperature observations from the last year
    date_tobs = dt.datetime(2016, 8, 23)
    
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > date_tobs).group_by(Measurement.date).order_by(Measurement.date).all()
	
    tobs_data = []
    
    for tobs in results:
        tobs_dict = {}
        tobs_dict[tobs.date] = tobs.tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def temp_st(start):
    """Return min, max and avg temperature from given date until 08/23/2017"""
    # Query for Query for min, max and avg temperature for given date
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= start).group_by(Measurement.date).order_by(Measurement.date).all()
	    
    for tobs in results:
        tobs_dict = {}
        tobs_dict[tobs.date] = tobs.tobs
        
        for key in tobs_dict.keys():
            if start == key:
                min_tmp = str(session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all())
                max_tmp = str(session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all())
                avg_tmp = str(session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all())
                min_tmp = int((min_tmp.replace("[(","")).replace(",)]",""))
                max_tmp = int((max_tmp.replace("[(","")).replace(",)]",""))
                avg_tmp = float((avg_tmp.replace("[(","")).replace(",)]",""))

                temps_calc = {"Min Temp":min_tmp, "Max Temp":max_tmp, "Avg Temp":avg_tmp}
                
                return jsonify(temps_calc)

    return jsonify({"error": f"Date not found: {start}"}), 404


@app.route("/api/v1.0/<start>/<end>")
def temp_st_end(start, end):
    """Return min, max and avg temperature for given dates"""
    # Query for min, max and avg temperature for given dates
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all()
	    
    for tobs in results:
        tobs_dict = {}
        tobs_dict[tobs.date] = tobs.tobs

        for key in tobs_dict.keys():
            if start == key:
                min_tmp = str(session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all())
                max_tmp = str(session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all())
                avg_tmp = str(session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date).all())
                min_tmp = int((min_tmp.replace("[(","")).replace(",)]",""))
                max_tmp = int((max_tmp.replace("[(","")).replace(",)]",""))
                avg_tmp = float((avg_tmp.replace("[(","")).replace(",)]",""))

                temps_calc = {"Min Temp":min_tmp, "Max Temp":max_tmp, "Avg Temp":avg_tmp}                
                return jsonify(temps_calc)

    return jsonify({"error": f"Date not found: {start}"}), 404


if __name__ == '__main__':
    app.run(debug=True)
