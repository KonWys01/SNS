from flask import Flask, render_template, request, redirect, url_for
from datetime import  datetime

from main import Satellites

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        mask = float(request.form['mask'])

        sat = Satellites(file_name='almanac.yuma.week0150.589824.txt', start_date=start_date, end_date=end_date, mask=mask)
        # # sat.set_start_end_dates(datetime(year=2022, month=2, day=25), datetime(year=2022, month=2, day=25))
        sat.satellites_coordinates()
        return redirect(url_for('dane', start=start_date, end=end_date, m=mask))
    else:
        return render_template('index.html')


@app.route('/<start><end><m>')
def dane(start, end, m):
    return f'<p>{start} {end} {m}</p>'


if __name__ == '__main__':
    app.run()
