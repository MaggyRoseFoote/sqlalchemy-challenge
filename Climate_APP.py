# Import the dependencies.
import pandas as pd 
import datetime as dt 
import numpy as np 

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
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

startDate = '2016-08-03'



#################################################
# Flask Routes
#################################################
app.route('/')
def homePage():
    return(
        f"<p><b> Hawaii Climate API, August 2016 - August 2017 </b> </p>"
        f"<p> Choose a Path: </p>"
        f"<b> /api/v1.0/stations </b><br/>"
        f"provides a list of weather stations available in the dataset <br/><br/>"
        f"<b> /api/v1.0/tobs </b><br/>"
        f"provides a list of tempuratures available from the most active station <br/><br/>"
        f" <b> /api/v1.0/precipitation </b> <br/>"
        f"provides a list of recorded precipitation quanities by date <br/><br/>"
        f"<b> /api/v1.0/<date> </b><br/>"
        f"provides the minimum, maximum, and average tempurature between a given start date and the end of the dataset"
        f"<b> /api/v1.0/<start_date>/<end_date> </b><br/>"
        f"provides the minimum, maximum, and average temperature between a given start date and a given end date"
   
    ) 

#stations path 
@app.route("/api/v1.0/stations") 
def stations():
   outputStation = session.query(Station.station, Station.name).all()
   stations = list(np.ravel(outputStation))
   return jsonify(stations)

#tobs path 
@app.route("/api/v1.0/tobs")
def Tobs(): 
    outputTobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).filter(Measurement.station == 'USC00519281', Measurement.date>=startDate).all()
    tobs = list(np.ravel(outputTobs)) 
    return jsonify(tobs)

#precipitation path 
@app.route("/api/v1.0/precipitation")
def Precipitation(): 
    outputPrecip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=startDate).all()
    precipitation = {date: prcp for date, prcp in outputPrecip}
    return jsonify(precipitation)

#date path 
@app.route("/api/v1.0/<date>")
def Date(date): 
    outputTemp = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs).filter(Measurement.date >= date)).all()
    temp = list(np.ravel(outputTemp))
    return jsonify(temp)


#date range path 
app.route("api/v1.0/<start_date>/<end_date>")
def Range(startingDate, endingDate): 
    outputRangeTemp = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs).filter(Measurement.date >= startingDate).filter(Measurement.date <= endingDate)).all()
    tempRange = list(np.ravel(outputRangeTemp))    
    return jsonify(tempRange)     