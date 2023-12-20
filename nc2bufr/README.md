# Converting UASDC netCDF to BUFR - uas2bufr.py

Python code to transform Uncrewed Aircraft Systems(UAS) data from netCDF into the WMO BUFR format. This is the code that will be used to convert each UASDC netCDF file to the final BUFR format. It is not necessary for individual providers to practice the BUFR conversion, but it is recommended, as this validates your netCDF format. If you do not wish to test on your own, please submit netCDF files to Pekka Rossi for testing. 

# Installation

## Python Environment Setup for ECCODES, NetCDF and ECMWF Libraries

This document provides step-by-step instructions for setting up a Python environment on a Unix/Linux system for working with ECCODES, NetCDF and ECMWF libraries. We'll be using Python 3.10 and creating a virtual environment via pip to manage our dependencies.

### Prerequisites

- Unix/Linux-based operating system
- Python 3.10

## Steps

1. **Installing Python 3.10 Virtual Environment**

   Ensure Python 3.10 is installed on your system. If not, you can install it using your distribution's package manager. For Ubuntu, use the following command:

   ```
   sudo apt install python3.10-venv
   ```

2. **Creating a Virtual Environment**

   A virtual environment allows you to manage Python dependencies separately for different projects. Create a virtual environment using the following command:

   ```
   python3 -m venv env
   ```

   This command creates a new directory `env` in your current directory, which contains a local Python installation.

3. **Activating the Virtual Environment**

   Before installing any packages, activate the virtual environment:

   ```
   source env/bin/activate
   ```

   Once activated, your command prompt will change, usually showing the name of the virtual environment (in this case, `env`).

4. **Installing Required Packages**

   With your virtual environment active, install the necessary Python packages using `pip`, the Python package installer.
   
   - **ecmwflibs**: A Python interface to the ECMWF libraries. Note that either of these versions will work, so proceed which the successful version.

     ```
     pip install ecmwflibs==0.5.3
     ``` 
     **OR** 
     ```
     pip install ecmwflibs==0.5.5
     ```

   - **numpy**: A fundamental package for scientific computing in Python.

     ```
     pip install numpy==1.26.2
     ```

   - **netCDF4**: A Python interface to the netCDF C library.

     ```
     pip install netCDF4==1.6.5
     ```

   - **eccodes**: A package for decoding and encoding meteorological data formats.

     ```
     pip install eccodes==1.6.1
     ```

5. **Confirming Installation**

   After installation, you can verify that the packages are installed correctly by using `pip list` or trying to import them in a Python interpreter.

6. **Exiting the Virtual Environment**

   Once you are done working in the virtual environment, you can deactivate it by running:

   ```
   deactivate
   ```

## Notes

- Always activate the virtual environment (`source env/bin/activate`) in your terminal before working on your project.
- If you open a new terminal window or tab, you need to activate the virtual environment again for that session.
- Your virtual environment (`env`) is local to the project directory. Keep this in mind if you work with multiple Python projects.

# Running
Convert data from file input_netcdf_filename to BUFR. The same filename will be used to output the file to BUFR.

`python3 uas2bufr.py input_netcdf`

**Example of running a python code to convert sample netCDF file in github**  

`python3 uas2bufr.py UASDC_operatorID_airframeID_20230327025804Z.nc`

# Copyright and license
(C) Copyright 2005- ECMWF.

This software is licensed under the terms of the Apache Licence Version 2.0 which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

In applying this licence, ECMWF does not waive the privileges and immunities granted to it by virtue of its status as an intergovernmental organisation nor does it submit to any jurisdiction.

# Contact
[Marijana Crepulja](https://github.com/marijanacrepulja)
