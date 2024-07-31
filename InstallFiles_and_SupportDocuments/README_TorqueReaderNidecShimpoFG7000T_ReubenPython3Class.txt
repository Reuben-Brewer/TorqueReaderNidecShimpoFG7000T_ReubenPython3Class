###########################

TorqueReaderNidecShimpoFG7000T_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) to control/read torque data from the Nidec-Shimpo/Seals-USA FG-7000T Torque Reader.

http://shimpoinstruments.com/product/FG-7000T

https://www.shimpo-direct.com/product/shimpo-fg-7000t-2-portable-torque-gauge-5-n-m

Now owned by Seals-USA: https://seals-usa.com/productlist/torque-product/torque-products/fg-7000t-digital-torque-gauge

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision C, 07/31/2024

Verified working on:

Python 3.8.

Windows 10/11 64-bit

Raspberry Pi Buster

(may work on Mac in non-GUI mode, but haven't tested yet)

Note For test_program_for_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class.py:

1. The specific sensors that will be used (and, hence, the number of sensors) is set by the variable "TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList".

2a. In Windows, you can get each sensor's USB-serial-device serial number by following the instructions in the USBserialDevice_GettingSerialNumberInWindows.png screenshot in this folder.

3. In Windows, you can manually set the latency timer for each sensor by following the instructions in the USBserialDevice_SettingLatencyTimerManuallyInWindows.png screenshot in this folder.

Note for ExcelPlot_CSVdataLogger_ReubenPython3Code__TorqueReaderNidecShimpoFG7000T:

1. This file is currently configured for 1 sensors, plotting only their sum. These details can be changed in the function "CreateExcelChart".

Note for the serial ports on the device:

#####

1. The USB-B port is actually a USB-serial output, and it works at seemingly any baud (9600, 19200, 38400, 1Mbps, 4Mbps, etc.)
Unfortunately, there's no latency-timer setting available in this Microsoft 10.0.22621.3672 driver.

#####

#####

2. The Mini-Din 8-pin port requires an Nidec-Shimpo FG-7RS232CBL cable (female-ended) --> RS232-USB converter cable.

2a. The Cable Creations CD0485 "USB2.0 to RS232 DB 9Pin Female Serial Cable, FTDI-FT232RNL" cable + gender-changer did *NOT* work. QUESTION: Is it the gender-changer that makes the Cable Creations not work?

2b. The StarTech ICUSB232V2 "USB to RS232 DB9 Serial Adapter Cable M/M" worked at 38400 baud.
Unfortunately, there's *NO* latency-timer setting available in this Prolific 3.9.6.2 driver.
USB\VID_067B&PID_2303\9&18D49067&0&4

2c. The Adafruit P18 "USB/Serial Converter - FT232RL" worked at 38400 baud.
The FTDI driver allows for adjusting the latency_timer. Worked *GREAT*.

2d. The FTDI "USB232R-10-BULK" (Digikey 768-1013-ND) worked at 38400 baud.
The FTDI driver allows for adjusting the latency_timer. Worked *GREAT*.

#####

###########################

###########################

Reader settings (consult the manual for more information):

###########################

########################### Python module installation instructions, all OS's

############

TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, ListOfModuleDependencies: ['ftd2xx', 'future.builtins', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'serial', 'serial.tools']

TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, ListOfModuleDependencies_TestProgram: []

TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['numpy']

TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, ListOfModuleDependencies_All:['ftd2xx', 'future.builtins', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'serial', 'serial.tools']

pip install psutil

pip install pyserial (NOT pip install serial).

pip install ftd2xx, ##https://pypi.org/project/ftd2xx/ #version 1.3.3 as of 11/08/23. For SetAllFTDIdevicesLatencyTimer function.

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class.py

<NEED TO FILL IN>

pip install pywin32         #version 305.1 11/8/23

pip install xlsxwriter      #version 3.1.9 as of 11/08/2023. Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

pip install xlutils         #version 2.0.0 as of 11/8/23

pip install xlwt            #version 1.3.0 as of 11/8/23

############

###########################

