# PyGeopack

A Python wrapper for Geopack-2008. This includes the T89, T96, T01 and 
TS05 (or is it TS04? I don't know...) magnetic field models for Earth's
magnetosphere. See https://ccmc.gsfc.nasa.gov/modelweb/magnetos/tsygan.html
and http://geo.phys.spbu.ru/~tsyganenko/modeling.html for more information.

NOTE: T01 doesn't currently work - there's a segmentation fault for some 
reason.

## Requirements

The following Python packages will be installed automatically:

* numpy
* PyFileIO
* RecarrayTools
* DateTimeTools
* kpindex

During the first import of the `PyGeopack` module, some C and Fortran 
needs compiling first, so the following will be needed:

* gcc
* make
* gfortran

## Installation

Firstly a couple of environment variables need setting up: `$KPDATA_PATH`
and `$GEOPACK_PATH`, which will point to the Kp index data and the 
Geopack data, respectively. This can be done by including the following 
in your `~/.bashrc` file, or by running it in the terminal before 
starting Python:

```
export KPDATA_PATH=/path/to/kp
export GEOPACK_PATH=/path/to/geopack/data
```
where both of those directories must be writable by the current user, 
unless the data already exist in them.

Then simply install using pip3:

```
pip3 install PyGeopack --user
```

or by downloading the latest release on GitHub and running:

```
pip3 install PyGeopack-0.0.9-py3-none-any.whl --user
```

## Post-install

After installation, the PyGeopack module will attempt to locate the 
OMNI data required for the models. If these data exist already in
`$GEOPACK_PATH` then it will load into memory. If they don't exist, then
the user will be prompted for authorisation to download the data, to 
allow the data download, press 'y', otherwise press 'n'. The data 
download and conversion may take a little while.




