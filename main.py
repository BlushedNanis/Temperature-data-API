from flask import Flask, render_template
import pandas as pd
from numpy import float64

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/v1/<station>/<date>")
def api(station, date):
    try:
        filepath = "data\TG_STAID" + str(station).zfill(6) + ".txt"
        df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
        temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
        print(type(temperature))
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