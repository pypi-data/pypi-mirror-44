<h1 align="center"> Divvy Data</h1>
<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img alt="MIT" src="https://img.shields.io/github/license/chrisluedtke/divvy-data.svg"></a>
  <a href="https://travis-ci.org/maxhumber/sausagelink"><img alt="Travis" src="https://img.shields.io/travis/com/chrisluedtke/divvy-data.svg"></a>
  <a href="https://pypi.python.org/pypi/sausagelink"><img alt="PyPI" src="https://img.shields.io/pypi/v/divvy-data.svg"></a>
</p>

## About

Divvy Data is a package to access historical and live Chicago bikeshare data.

I used this data to blog about [Chicago  biking and data visualization](https://chrisluedtke.github.io/divvy-data.html). See my analysis notebook on [nbviewer](https://nbviewer.jupyter.org/github/chrisluedtke/divvy-data-analysis/blob/master/notebook.ipynb).

![Divvy Data Animation](img/divvy_day.gif)

## Set up

Fork/clone the repository or pip install the `divvydata` package:
```
pip install -i https://test.pypi.org/simple/ divvy-data
pip install git+https://github.com/chrisluedtke/divvy-data.git
```

## Usage
### Historical Data
```python
import divvydata

# gather historical data over all years
rides, stations = divvydata.get_historical_data(
    years=[str(yr) for yr in range(2013,2019)],
    rides=True,
    stations=True
)
```

### Live Data
```python
import divvydata

sf = divvydata.StationsFeed()
df = sf.monitor_event_history(runtime_sec=60)  # also saves to sf.event_history attribute

# filter to stations that received interactions
df = df.loc[df['id'].duplicated(keep=False)]
```

### Data Usage Limitations

This package does not host or directly provide data, except as cited in analysis notebooks. When using Divvy data, follow [Divvy's Data License Agreement](https://www.divvybikes.com/data-license-agreement).
