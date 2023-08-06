xPlot Util
===================================

The program provides a GUI for the user to graph the data in different forms, normalize and fit it. First the user must
open a spec file by clicking on the browse button. Once the file has been open, the path will be displayed next to the
button. It's important for the PVvalue files of the particular spec file to be located in the same directory as the spec.
Since, only the PVvalues in the directory with scans in the spec file wlll be displayed in the QListWidget. The user will
then select a scan by double clicking on it, the program will automatically open the particular selected file. This
enables the user to start graphing the raw data, as well as do the Gaussian fit, normalize the data. The program allows
the user to graph the data obtained from both the Gaussian and Lattice fit, as well as to create a report from those fits.

Version
-------
0.1.2 - 07/10/2017

Getting Started
---------------
- The first step to building an environment to run xPlot Util is downloading Anaconda. Install the version that utilizes
Python 3.5. For further instructions on how to download Anaconda visit https://www.continuum.io/downloads
- Once Anaconda has been installed on your machine, through the terminal either using pip or conda. Please install the
following modules:
    - pyqt 5.6.0
    - matplotlib 2.0.2
    - numpy 1.13.0
    - spec2nexus 2017.522.1
    - future 0.16.0
    - scipy 0.19.0
    - peakutils 1.1.0

Built With
----------
- PyQt5/PySide: Creates the framework for the GUI.
- matplotlib: Creates frame work for the graphs.
- spec2nexus: Reads spec file.
- PeakUtils: Guesses the peak position

Installation
------------
There are two ways to download xPlotUtil. You can either use the git clone command or use the pip install command.

- For the git clone command use HTTPS or SSH, which I have provided below:
    - SSH: git@github.com:AdvancedPhotonSource/xPlotUtil.git
    - HTTPS: https://github.com/AdvancedPhotonSource/xPlotUtil.git

- For the pip command follow these steps:
    1. Download Anaconda with Python 2.7
    2. Open the terminal and make sure it has anaconda as its path. Then type the following command:
        - pip install xPlotUtil
    3. Once xPlotUtil has been installed type xPlotUtil.bat as a command. This will activate a script to download numpy
    and PyQt5.
    3. Once all the required modules have been downloaded simply type xPlotUtil as a command to start the GUI.

Author(s)
-------
Phaulo C. Escalante - CO-OP Student Technical at Argonne National Laboratory

License
-------
Copyright (c) UChicago Argonne, LLC. All rights reserved.
See LICENSE file.