from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import datetime, timedelta

import inflect
import pandas as pd
import json
import plotly
import plotly.express as px

from main import Satellites

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        phi = float(request.form['latitude'])
        lam = float(request.form['longitude'])
        h = float(request.form['height'])
        observ_pos = list(Satellites.phi_lamda_to_xyz(phi, lam, h))
        mask = int(request.form['mask'])

        # return redirect(url_for('dane', file_name='almanac.yuma.week0150.589824.txt', start_date=start_date, mask=mask, observer_pos=observ_pos))
        return redirect(url_for('dane', start_date=start_date, mask=mask, observer_pos=observ_pos))
        # return redirect(url_for('dane'))
    else:
        return render_template('index.html')


@app.route('/wyniki<start_date><mask><observer_pos>', methods=['POST', 'GET'])
def dane(start_date, mask, observer_pos):

    file_name = 'almanac.yuma.week0150.589824.txt'
    """ elewacja """
    sat = Satellites(file_name=file_name, start_date=datetime(year=2022, month=2, day=25), mask=10, observer_pos=[50,20,100])
    era = sat.interval
    start_date = sat.start_date
    sat.satellites_coordinates()
    satellites = sat.show_elevation_of_satellites()

    dates = [start_date + i*era for i in range(97)]

    satellites_zipped = list(zip(*satellites))

    ids = [int(i) for i in sat.satellites_ids]
    satellites_names = []
    p = inflect.engine()  # numbers to names
    for i in range(len(ids)):
        satellites_names.append(p.number_to_words(ids[i]))

    data = pd.DataFrame(satellites_zipped, index=dates, columns=satellites_names)
    print(data)
    fig1 = px.line(data, x=data.index, y=satellites_names)
    fig1.update_layout(title='Wykres elewacji satelit', xaxis_title='Era', yaxis_title='Wartość elewacji')
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    """ widoczne satelity """
    visible_satellites = Satellites(file_name=file_name, start_date=datetime(year=2022, month=2, day=25), mask=10,
                     observer_pos=[50, 20, 100])
    visible_satellites.interval = timedelta(hours=1)
    visible_satellites.satellites_coordinates()
    visible_satellites_data = visible_satellites.show_visible_satellites()
    dates_visible = [i for i in range(1, 25)]

    data_visible = pd.DataFrame(visible_satellites_data, index=dates_visible, columns=['visible satellites'])
    print(data_visible)
    fig2 = px.bar(data_visible, x=data_visible.index, y=['visible satellites'])
    fig2.update_layout(title='Wykres widocznych satelit', xaxis_title='Era', yaxis_title='Liczba widocznych satelit')
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('graphs.html', graph1JSON=graph1JSON, graph2JSON=graph2JSON)


if __name__ == '__main__':
    app.run()
