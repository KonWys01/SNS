from datetime import datetime, timedelta
import json
from typing import Union

import ast
from flask import Flask, render_template, request, redirect, url_for, make_response
import inflect
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import urllib.request

from main import Satellites
from python.plotly_skyplot import plot_skyplot

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home() -> Union[make_response, render_template]:
    if request.method == "POST":
        file_chosen = request.form["almach"]
        if file_chosen == "default_almach":
            file_name = "almanac.yuma.week0150.589824.txt"
        else:
            url_current = (
                "https://www.navcen.uscg.gov/?pageName=currentAlmanac&format=yuma"
            )
            almanac_name = "current_almanac.alm"
            urllib.request.urlretrieve(url_current, almanac_name)
            file_name = almanac_name
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M")
        phi = float(request.form["latitude"])
        lam = float(request.form["longitude"])
        h = float(request.form["height"])
        observ_pos = [phi, lam, h]
        mask = request.form["mask"]

        res = make_response(redirect(url_for("dane")))
        res.set_cookie("file_name", value=file_name)
        res.set_cookie("mask", value=mask)
        res.set_cookie("observer_pos", f"{observ_pos}")
        res.set_cookie("start_date", f"{start_date}")
        return res
    else:
        return render_template("index.html")


@app.route("/wyniki", methods=["POST", "GET"])
def dane() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    """ elewacja """
    sat = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    era = sat.interval
    start_date = sat.start_date
    sat.satellites_coordinates()
    satellites = sat.show_elevation_of_satellites()

    dates = [start_date + i * era for i in range(97)]

    satellites_zipped = list(zip(*satellites))

    ids = [int(i) for i in sat.satellites_ids]
    satellites_names = []
    p = inflect.engine()  # numbers to names
    for i in range(len(ids)):
        satellites_names.append(p.number_to_words(ids[i]))

    data = pd.DataFrame(satellites_zipped, index=dates, columns=satellites_names)
    fig1 = px.line(data, x=data.index, y=satellites_names)
    fig1.update_layout(
        title="Satellite Elevation",
        xaxis_title="Date and Time",
        yaxis={"title": "Elevation", "range": (mask, 90)},
        height=700
    )
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("graphs.html", graph1JSON=graph1JSON)


@app.route("/widoczne", methods=["POST", "GET"])
def widoczne() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    visible_satellites = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    visible_satellites.interval = timedelta(minutes=15)
    visible_satellites.satellites_coordinates()
    visible_satellites_data = visible_satellites.show_visible_satellites()
    dates_visible = [i for i in range(1, 97)]
    data_visible = pd.DataFrame(
        visible_satellites_data, index=dates_visible, columns=["visible satellites"]
    )
    fig2 = px.bar(data_visible, x=data_visible.index, y=["visible satellites"])
    fig2.update_layout(
        title="Visible Satellites",
        xaxis_title="Date and Time",
        yaxis_title="Number of visible satellites",
        height=700
    )
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("widoczne.html", graph2JSON=graph2JSON)


@app.route("/dop", methods=["POST", "GET"])
def dop() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    sat_DOP = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    sat_DOP.satellites_coordinates_reversed()

    DOP_zipped = list(zip(*sat_DOP.DOP))
    DOP_names = ["GDOP", "PDOP", "TDOP", "HDOP", "VDOP"]
    data = pd.DataFrame(DOP_zipped, columns=DOP_names)
    fig3 = px.line(data, x=data.index, y=DOP_names)
    fig3.update_layout(title="DOP chart", xaxis_title="Date and Time", yaxis_title="DOP", height=700)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dop.html", graph3JSON=graph3JSON)


@app.route("/skyplot", methods=["POST", "GET"])
def skyplot() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    sat_skyplot = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    sat_skyplot.satellites_coordinates_skyplot()

    sat_positions = sat_skyplot.show_skyplot_positions()
    fig4 = plot_skyplot(sat_positions)
    fig4.update_layout(title="Skyplot - satellites positions", height=700)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("skyplot.html", graph4JSON=graph4JSON)


@app.route("/groundtrack", methods=["POST", "GET"])
def groundtrack() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    sat = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    sat.satellites_coordinates()

    fig5 = go.Figure()
    for i in range(len(sat.satellites_phi_lambda)):
        lat_iterated = sat.satellites_phi_lambda[i][0]
        lon_iterated = sat.satellites_phi_lambda[i][1]
        fig5.add_trace(
            go.Scattergeo(
                lon=lon_iterated, lat=lat_iterated, mode="lines", name=f"{i + 1}"
            )
        )
    fig5.update_layout(title="Satellites Groundtrack", height=700)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("groundtrack.html", graph5JSON=graph5JSON)


@app.route("/global", methods=["POST", "GET"])
def global_satellites() -> render_template:
    file_name = request.cookies.get("file_name")
    mask = int(request.cookies.get("mask"))
    observer_pos = ast.literal_eval(request.cookies.get("observer_pos"))
    start_date = request.cookies.get("start_date")
    start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

    sat = Satellites(
        file_name=file_name, start_date=start_date, mask=mask, observer_pos=observer_pos
    )
    sat.satellites_coordinates()

    fig6 = go.Figure()
    for i in range(len(sat.satellites_phi_lambda)):
        lat_iterated = sat.satellites_phi_lambda[i][0]
        lon_iterated = sat.satellites_phi_lambda[i][1]
        fig6.add_trace(
            go.Scattergeo(
                lon=lon_iterated, lat=lat_iterated, mode="lines", name=f"{i + 1}"
            )
        )
    fig6.update_layout(
        geo=dict(
            projection=dict(type="orthographic"),
            lonaxis=dict(showgrid=True, gridcolor="rgb(102, 102, 102)", gridwidth=0.5),
            lataxis=dict(showgrid=True, gridcolor="rgb(102, 102, 102)", gridwidth=0.5),
        )
    )
    fig6.update_layout(title="Global satellites visibility", height=700)
    graph6JSON = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("global_satellites.html", graph6JSON=graph6JSON)


if __name__ == "__main__":
    app.run()
