# Import the libraries
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Reading the data and extracting the important data.
stations = pd.read_csv("Data/data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

# HomePage of our website.
@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())

# This is another page in our website.
# With this you can see the temp. of a specific place at a specific day.
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "Data/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}

# This is another page in our website.
# With this you can see the temp. of a specific place.
@app.route("/api/v1/<station>")
def all_data(station):
    filename = "Data/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    result = df.to_dict(orient="records")
    return result

# This is another page in our website.
# With this you can see the temp. of a specific place for the full year.
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "Data/data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result

# We run the program.
if __name__ == "__main__":
    app.run(debug=True)