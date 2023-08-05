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

All reported values are in units of quadrillion british thermal units (1.0E15 btu). Be aware that the datasets may provide [more precision](https://www.eia.gov/totalenergy/data/monthly/dataunits.php) than is published in the PDF reports.

## Installation

_pyleiades_ is hosted through the Python Package Index (PyPI) and can be easily installed using pip.
From the command line, run

```
pip install pyleiades
```

The module requires a recent version of python 3 (3.6 or greater), pandas, and matplotlib, among others.
If you run into trouble running the package, try using the Anaconda environment provided in this repo.
Install the environment using the command

```
conda env create -f environment.yml
```

and activate the environment by issuing the command

```
conda activate pyleiades
```

## Updating

An archive of EIA Monthly Energy Review datasets is kept in the `pyleiades` data repository. 
This may not include the most up to date information, and so the package comes with a script to update the available data.
Once the package is installed, run 

```
update_eia_data.py
```

from the command line to download the most recent data from the EIA website. 
