from flask import Flask, render_template
import pandas as pd
from numpy import float64, nan

app = Flask(__name__)

stations = pd.read_csv("data\stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", stations_id=stations.to_html())


@app.route("/api/v1/<station>/<year>/<month>/<day>")
def station_and_date(station, year, month, day):
    try:
        if len(year) == 4 and len(month) == 2 and len(day) == 2:
            date = year + "-" + month + "-" + day
            filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
            df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
            temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
            type(temperature) is float64
            return {"station": station,
                    "date": date,
                    "temperature": temperature}
        else:
            return "Please, provide a valid date"
    except FileNotFoundError:
        return "Please, provide a valid station."


@app.route("/api/v1/<station>/<year>/<month>")
def station_and_month(station, year, month):
    try:
        if len(year) == 4 and len(month) == 2:
            date = year + month
            filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
            df = pd.read_csv(filepath, skiprows=20)
            df["    DATE"] = df["    DATE"].astype(str)
            month_df = df[df["    DATE"].str.startswith(date)]
            month_df["    DATE"] = pd.to_datetime(month_df["    DATE"])
            result_df = month_df[["    DATE", "   TG"]].to_dict('records')
            return result_df
        else:
            return "Please, provide a valid date"
    except FileNotFoundError:
        return "Please, provide a valid station."


@app.route("/api/v1/<station>/<year>")
def station_and_year(station, year):
    try:
        if len(year) <= 4:
            date = year
            filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
            df = pd.read_csv(filepath, skiprows=20)
            df["    DATE"] = df["    DATE"].astype(str)
            year_df = df[df["    DATE"].str.startswith(date)]
            year_df["    DATE"] = pd.to_datetime(year_df["    DATE"])
            result_df = year_df[["    DATE", "   TG"]].to_dict('records')
            return result_df
        else:
            return "Please, provide a date"
    except FileNotFoundError:
        return "Please, provide a valid station."

@app.route("/api/v1/<station>")
def only_station(station):
    try:
        filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
        df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
        df["TR"] = df["   TG"].mask(df["   TG"] == -9999, nan)
        df["TC"] = df["TR"] / 10
        df["TF"] = round((df["TC"] * 9/5 + 32), 2)
        result_df = df[["    DATE", "TC", "TF"]].to_dict('records')
        return result_df
    except FileNotFoundError:
        return "Please, provide a valid station."


if __name__ == "__main__":
    app.run(debug=True)