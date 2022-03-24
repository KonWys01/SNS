from flask import Flask, render_template

from main import Satellites

app = Flask(__name__)


@app.route('/')
def hello_world():
    sat = Satellites(file_name='almanac.yuma.week0150.589824.txt')
    # sat.set_start_end_dates(datetime(year=2022, month=2, day=25), datetime(year=2022, month=2, day=25))
    sat.satellites_coordinates()
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
