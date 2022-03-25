from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

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

        sat = Satellites(file_name='almanac.yuma.week0150.589824.txt', start_date=start_date, mask=mask, observer_pos=observ_pos)
        # # sat.set_start_end_dates(datetime(year=2022, month=2, day=25), datetime(year=2022, month=2, day=25))
        sat.satellites_coordinates()
        return redirect(url_for('dane', start=start_date, m=mask, pos=observ_pos))
    else:
        return render_template('index.html')


@app.route('/<start><m><pos>')
def dane(start, m, pos):
    return f'<p>{start}   {m}   {pos}</p>'


if __name__ == '__main__':
    app.run()
