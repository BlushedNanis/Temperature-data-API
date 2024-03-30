from flask import Flask, render_template
import pandas as pd
from numpy import nan

app = Flask(__name__)

stations = pd.read_csv("data\\stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", stations_id=stations.to_html())


@app.route("/api/v1/<station>/<year>/<month>/<day>")
def station_and_date(station, year, month, day):
    try:
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            #Construct date variable with endpoint data
            date = year + "-" + month + "-" + day
            
            #Construct filepath variable with endpoint data
            filepath = "data\\TG_STAID" + str(station).zfill(6) + ".txt"
            
            #Create data frame instance and get requiered row
            df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
            day_df = df.loc[df["    DATE"] == date][["    DATE", "   TG"]]
            
            #Add columns for celcius and fahrenheit temperatures
            day_df["TR"] = day_df["   TG"].mask(df["   TG"] == -9999, nan)
            day_df["TC"] = day_df["TR"] / 10
            day_df["TF"] = round((day_df["TC"] * 9/5 + 32), 2)
            
            #Construct result data frame instance
            result_df = day_df[["    DATE", "TC", "TF"]].to_dict('records')
            return result_df
        else:
            return "Please, provide a valid date"
    except FileNotFoundError:
        return "Please, provide a valid station."


@app.route("/api/v1/<station>/<year>/<month>")
def station_and_month(station, year, month):
    try:
        if len(year) == 4 and len(month) == 2:
            #Construct date variable with endpoint data
            date = year + month
            
            #Construct filepath variable with endpoint data
            filepath = "data\\TG_STAID" + str(station).zfill(6) + ".txt"
            
            #Create data frame instance from filepath
            df = pd.read_csv(filepath, skiprows=20)
            
            #Get requiered rows according to date
            df["    DATE"] = df["    DATE"].astype(str)
            year_df = df[df["    DATE"].str.startswith(date)]
            year_df["    DATE"] = pd.to_datetime(year_df["    DATE"])
            
            #Add columns for celcius and fahrenheit temperatures
            year_df["TR"] = year_df["   TG"].mask(df["   TG"] == -9999, nan)
            year_df["TC"] = year_df["TR"] / 10
            year_df["TF"] = round((year_df["TC"] * 9/5 + 32), 2)
            
            #Construct result data frame instance
            result_df = year_df[["    DATE", "TC", "TF"]].to_dict('records')
            return result_df
        else:
            return "Please, provide a valid date"
    except FileNotFoundError:
        return "Please, provide a valid station."


@app.route("/api/v1/<station>/<year>")
def station_and_year(station, year):
    try:
        if len(year) <= 4:
            #Construct date variable with endpoint data
            date = year
            
            #Construct filepath variable with endpoint data
            filepath = "data\\TG_STAID" + str(station).zfill(6) + ".txt"
            
            #Get requiered rows according to date
            df = pd.read_csv(filepath, skiprows=20)
            df["    DATE"] = df["    DATE"].astype(str)
            year_df = df[df["    DATE"].str.startswith(date)]
            year_df["    DATE"] = pd.to_datetime(year_df["    DATE"])
            
            #Add columns for celcius and fahrenheit temperatures
            year_df["TR"] = year_df["   TG"].mask(df["   TG"] == -9999, nan)
            year_df["TC"] = year_df["TR"] / 10
            year_df["TF"] = round((year_df["TC"] * 9/5 + 32), 2)
            
            #Construct result data frame instance
            result_df = year_df[["    DATE", "TC", "TF"]].to_dict('records')
            return result_df
        else:
            return "Please, provide a date"
    except FileNotFoundError:
        return "Please, provide a valid station."

@app.route("/api/v1/<station>")
def only_station(station):
    try:
        #Construct filepath variable with endpoint data
        filepath = "data\\TG_STAID" + str(station).zfill(6) + ".txt"
        
        #Create data frame instance from filepath
        df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
        
        #Add columns for celcius and fahrenheit temperatures
        df["TR"] = df["   TG"].mask(df["   TG"] == -9999, nan)
        df["TC"] = df["TR"] / 10
        df["TF"] = round((df["TC"] * 9/5 + 32), 2)
        
        #Construct result data frame instance
        result_df = df[["    DATE", "TC", "TF"]].to_dict('records')
        return result_df
    except FileNotFoundError:
        return "Please, provide a valid station."


if __name__ == "__main__":
    app.run(debug=True)