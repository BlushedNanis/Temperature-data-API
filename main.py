from flask import Flask, render_template
import pandas as pd
from numpy import float64, nan

app = Flask(__name__)

stations = pd.read_csv("data\stations.txt", skiprows=17)
stations = stations[["STAID","STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", stations_id=stations.to_html())


@app.route("/api/v1/<station>")
def only_station(station):
    filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    df["TR"] = df["   TG"].mask(df["   TG"] == -9999, nan)
    df["TC"] = df["TR"] / 10
    df["TF"] = round((df["TC"] * 9/5 + 32), 2)
    result_df = df[["    DATE", "TC", "TF"]].to_dict('records')
    return result_df

@app.route("/api/v1/<station>/<date>")
def station_and_date(station, date):
    try:
        filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
        df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
        temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
        if type(temperature) is float64:
            return {"station": station,
                    "date": date,
                    "temperature": temperature}
        else:
            return "Please, provide a valid date."
    except FileNotFoundError:
        return "Please, provide a valid station."


if __name__ == "__main__":
    app.run(debug=True)