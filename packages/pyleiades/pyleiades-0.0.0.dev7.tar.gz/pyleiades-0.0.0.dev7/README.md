# *pyleiades*
[![Build Status](https://travis-ci.org/mitchnegus/pyleiades.svg?branch=master)](https://travis-ci.org/mitchnegus/pyleiades)

## Python Library for EIA Data Examination & Exhibition

###### A tool for creating visuals from historical energy data (e.g. the EIA monthly energy review).
 
This tool is designed to provide insightful, aesthetic and more flexible visualizations of the Energy Information Administration (EIA) monthly energy review datasets.
The datasets contain information about the sources of energy Americans have relied on for power since the middle of the 20th century. 
The datasets begin in 1949 with annual energy production, consumption, import, and export values, and extend up until the present. 
Monthly energy datapoints are reported starting in 1973.

The basic energy sources are reported in the following groups:  

###### Fossil Fuels
* Coal
* Natural Gas
* Petroleum

###### Renewables
* Wind
* Solar
* Hydroelectric
* Geothermal
* Biomass

###### Nuclear
* Fission

The data is published monthly on the [EIA's website](https://www.eia.gov/totalenergy/data/monthly/), and as of March 31st, 2019 records were provided up through December 2018. This package also includes data up to date through the end of 2018, though more recent data can be downloaded using an included script. 

All reported values are in units of quadrillion british thermal units (1.0E15 BTU). Be aware that the datasets may provide [more precision](https://www.eia.gov/totalenergy/data/monthly/dataunits.php) than is published in the PDF reports.

## Installation

_pyleiades_ is hosted through the Python Package Index (PyPI) and can be easily installed using pip.
From the command line, run

```
$ pip install pyleiades
```

The module requires a recent version of Python 3 (3.6 or greater), pandas, and matplotlib, among others.
If you run into trouble running the package, try using the Anaconda environment provided in this repo.
Install the environment using the command

```
$ conda env create -f environment.yml
```

and activate the environment by issuing the command

```
$ conda activate pyleiades
```

## Updating

An archive of EIA Monthly Energy Review datasets is kept in the `pyleiades` data repository. 
This may not include the most up to date information, and so the package comes with a script to update the available data.
Once the package is installed, run 

```
$ update_eia_data.py
```

from the command line to download the most recent data from the EIA website. 

## Using the API

The API is built around two main object types—the `Energy` and `Visual` classes.

### The `Energy` object

To access the EIA data directly for a certain energy type, use the `Energy` class.
For example, the energy consumption data for all renewable energy sources can be accessed with:

```
>>> from pyleiades import Energy
>>> renewables = Energy('renewable')
```

The resulting `renewables` object stores the complete consumption history within the `energy_data` dataframe attribute.

```
>>> renewables.energy_data
     date_code      value
6220    194913   2.973984
6221    195013   2.977718
6222    195113   2.958464
6223    195213   2.940181
...
```

The `date_code` column gives the reporting date (in the format `YYYYMM`, where the month code 13 indicates a yearly total) and the `value` column gives the consumption amounts (in QBTU) for each date. 
In the example above, the first four entries of the `energy_data` dataframe are the renewable energy yearly consumption totals for 1949 through 1952.

Energy consumption values are the default, however the `Energy` objects can also be used to access production, import and export statistics.
The type of statistic can be selected using the `stat_type` keyword argument.

```
>>> renewables = Energy('renewable', stat_type='production')
>>> renewables.energy_data
     date_code     value
6220    194913  1.549262
6221    195013  1.562307
6222    195113  1.534669
6223    195213  1.474369
```

Perhaps more interesting than the complete history, however, are more sophisticated features of the data, like interval specific totals and extremes.

Using the `totals` method of an `Energy` object allows the data to be totaled at a specified interval—either monthly, yearly, or cumulatively.

```
>>> renewables.totals('monthly')
           value
  date
197301  0.403981
197302  0.360900
197303  0.400161
197304  0.380470
```

Notice that here the monthly data only goes back as far as 1973 (though the `energy_data` attribute showed yearly data for renewable energy dating back to 1949). 
By default, the `totals` method selects the entire range of available data. 
This  behavior can be overriden by providing start and end dates for some interval as keyword arguments.
To only get monthly renewable energy data from 2000 to 2010, this would be:

```
>>> renewables.totals(freq='monthly', start_date='200001', end_date='200912')
           value
  date
200001  0.505523
200002  0.498993
200003  0.558474
200004  0.567147
```

To get extremes over a dataset interval, use the `maxima` or `minima` methods.

### The `Visual` object

A `Visual` allows the package to create plots of several energy types. 
The initialization parameters for a `Visual` are similar to those for an `Energy` object. 
A `Visual` can accept a single energy type or a list of energy types, optionally followed by a type of statistic (consumption by default).

```
visual = Visual(['coal', 'nuclear', 'renewable'])
```

This visual object's methods can then be used to generate any of a variety of visuals. 
The syntax is again similar to that of the `Energy` object, however it includes a subject argument corresponding to a method of the `Energy` object.
Here's an example that generates a line graph of energy totals:

```
visual.linegraph(subject='totals', freq='monthly', start_date='1970')
```

![visual comparing coal, nuclear, and renewable energy consumption since 1970](pyleiades/fig/demo-plot.png)

Run the very simple installed script `pyleiades-demo.py` to see the package in action.