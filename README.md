Teqc EasyGUI
====
Teqc EasyGUI is an application for editing, analyzing and visualizing data obtained from GNSS receivers based on following open-source programs:
* teqc made by UNAVCO, available on the website https://www.unavco.org/software/data-processing/teqc/teqc.html
* teqcplot.py made by Stuart K. Wier, available on the website http://www.westernexplorers.us/GNSSplotters/Teqcplot_Documentation.txt

Teqc EasyGUI splices functionality of this two programs in a simple and easy-to-use graphical user interface with addition of few new functions. Please keep in mind that this version of software has not been tested well, so you might experience some issues with usage. I will be grateful for any messages about errors in the application. 

Requirements
====
In order to run Teqc EasyGUI you need to have Python 3.7.0 or higher installed on your computer, as well as following packages:
* matplotlib
* numpy

It is best to install these packages through default package installer for Python - pip. To do that you type in command line:
```
pip install numpy
pip install matplotlib
```

Or just:
```
pip install -r requirements.txt
```
As complete list of required packages is provided in the file requirements.txt.

Teqc EasyGUI has been written for Windows users, though I think it is possible to run it on other platforms. In order to do that you just need to replace the teqc executable file teqc.exe with file executable on your platform available on teqc website.

Features
====
For further explanations I refer you to teqc documentation:
* https://www.unavco.org/software/data-processing/teqc/tutorial/tutorial.html
* https://www.unavco.org/software/data-processing/teqc/doc/UNAVCO_Teqc_Tutorial.pdf

First thing you should do to get started is open file you want to work with. Application is able to recognise and proceess files that teqc enables. It contain native binary files from various GNSS receivers as well as RINEX version 2. The thing that this function actually does is saving path to the file in a variable.

In Teqc EasyGUI you can:
* perform editing of a file:
  * convert binary format files into RINEX observation or navigation files 
  * merge multiple RINEX files into one (keep in mind that obserations have to be in chronological order)
  * change start time and time period of observation
  * change interval of observations - decimate data (note that inserted value has to be higher than the native interval value of observations
  * modify RINEX header - all textboxes works independently and modification of satellite system also reduces observations only to that system
* analyze data contained in file:
  * display metadata of file
  * display detected file format
  * quality check of a file
  * summary of observations in a file
  * limit diplayed informations to specified satellite system
* visualize data from quality check:
  * choose number of satellite vehicles to draw plot
  * choose additional file for visualisation in Compact3 format (*.dxx, *.mxx, *.ixx, *.snx, where x is channel number)
  * draw four diffrent plots 
  * display position of observation on Google Maps
  
License
====
This project is distributed under the GNU General Public License.