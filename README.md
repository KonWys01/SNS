
# Satellite Navigation System

App that calculates positions of satellites based on given date and coordinates of observer.

## Features

* Home - Input date and coordinates of observer
* Elevation - Elevations of all satellites within 24 hours
* Visible - Chart of amount of visible satellites in given time
* DOP - Dilution Of Precision of satellites
* Skyplot - Map of positions of visible satellites
* Groundtrack - 2D map of Earth with satellites' paths
* Global Groundtrack - 3D map of Earth with satellites' paths


## Demo

![](https://github.com/KonWys01/SNS/blob/main/Demo.gif)

## Libraries

* Flask
* Plotly
* NumPy
* pandas

Project done in Python 3.9


## Installation

To setup the project create virtualenv and install dependencies

```bash
  python3.9 -m venv env
  source env/bin/activate
  pip install -r requirements.txt
```


## Deployment

To deploy this project run
```bash
  python app.py
```

App should respond of default address being:
<pre>
  <a href="http://localhost:5000">localhost:5000</a>
</pre>
