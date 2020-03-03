import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create an engine for the chinook.sqlite database
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
#Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
# Create a database session object
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"- List precipitation by dates of prior year<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of stations numbers and names<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List tempreratures from all stations for prior tear<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date, calculates `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date, calculates the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive<br/>"
        
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    prcp_data_list = dict(prcp_data)
    return jsonify(prcp_data_list)

@app.route("/api/v1.0/stations")
def stations():
    stations_all = session.query(Station.station, Station.name).all()
    station_list = list(stations_all)
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        order_by(Measurement.date).all()
    tobs_data_list = list(tobs_data)
    return jsonify(tobs_data_list)

@app.route("/api/v1.0/<start>")
def start_day(start):
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    start_day_list = list(start_day)
    return jsonify(start_day_list)

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
    start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    start_end_day_list = list(start_end_day)
    return jsonify(start_end_day_list)    

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)
