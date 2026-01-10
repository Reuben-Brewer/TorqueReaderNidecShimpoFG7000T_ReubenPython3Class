# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 01/09/2026

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
##########################################

##########################################
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
import queue as Queue
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

##########################################
import serial #___IMPORTANT: pip install pyserial (NOT pip install serial).
from serial.tools import list_ports
##########################################

##########################################
global ftd2xx_IMPORTED_FLAG
ftd2xx_IMPORTED_FLAG = 0
try:
    import ftd2xx #https://pypi.org/project/ftd2xx/ 'pip install ftd2xx', current version is 1.3.1 as of 05/06/22. For SetAllFTDIdevicesLatencyTimer function
    ftd2xx_IMPORTED_FLAG = 1

except:
    exceptions = sys.exc_info()[0]
    print("**********")
    print("********** TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ERROR, failed to import ftdtxx, Exceptions: %s" % exceptions + " ********** ")
    print("**********")
##########################################

##########################################################################################################
##########################################################################################################

class TorqueReaderNidecShimpoFG7000T_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        print("#################### TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0 #unicorn

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.DedicatedTxThread_StillRunningFlag = 0
        self.DedicatedRxThread_StillRunningFlag = 0
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.SerialObject = serial.Serial()
        self.SerialConnectedFlag = 0
        self.SerialBaudRate = 38400
        self.SerialTimeoutSeconds = 0.5
        self.SerialParity = serial.PARITY_NONE
        self.SerialStopBits = serial.STOPBITS_ONE
        self.SerialByteSize = serial.EIGHTBITS
        self.SerialRxBufferSize = 100 #Haven't set this based on anything, need to measure
        self.SerialTxBufferSize = 100 #Haven't set this based on anything, need to measure
        self.SerialPortNameCorrespondingToCorrectSerialNumber = "default"
        self.DedicatedTxThread_TxMessageStringToSend_Queue = Queue.Queue()
        self.DedicatedTxThread_TxMessageBytearrayToSend_Queue = Queue.Queue()
        self.SerialStrToTx_LAST_SENT = ""
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.TorqueReadingUnits_AcceptableValuesList = ["N.m", "N.cm", "kgf.cm", "lbf.ft", "lbf.in"]  #On 11/13/24, it appeared that "kgf.m" and "N.mm" are not commandable even though they appear in the data-sheet.

        self.TorqueReadingUnits_DefaultUnits = "N.m"

        self.SamplesPerSecond_AcceptableValuesList = [10, 20, 50, 100]

        self.TimeBetweenSendingSettingCommands = 0.010
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromDedicatedTxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedTxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = -11111.0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0

        self.CurrentTime_CalculateMeasurementTorqueDerivative = -11111.0
        self.LastTime_CalculateMeasurementTorqueDerivative = -11111.0
        self.DataStreamingDeltaT_CalculateMeasurementTorqueDerivative = -11111.0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentMeasurementTorque_Nm = -11111.0
        self.LastMeasurementTorque_Nm = -11111.0
        
        self.ResetPeak_EventNeedsToBeFiredFlag = 0
        self.ResetPeak_EventHasHappenedFlag = 0

        self.ResetTare_EventNeedsToBeFiredFlag = 0
        self.ResetTare_EventHasHappenedFlag = 0

        self.DataStream_State = 1
        self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 0

        self.ToggleUnits_EventNeedsToBeFiredFlag = 0
        self.ToggleUnits_EventCounter = 0

        self.FlushSerial_EventNeedsToBeFiredFlag = 0

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber_USBtoSerialConverter" in SetupDict:
            self.DesiredSerialNumber_USBtoSerialConverter = SetupDict["DesiredSerialNumber_USBtoSerialConverter"]

        else:
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ERROR, must initialize object with 'DesiredSerialNumber_USBtoSerialConverter' argument.")
            return

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: DesiredSerialNumber_USBtoSerialConverter: " + str(self.DesiredSerialNumber_USBtoSerialConverter))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UpdateSetupDictParameters(SetupDict)
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                            ("DataStreamingFrequency_CalculatedFromDedicatedRxThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                            ("TorqueDerivative", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.TorqueDerivative_ExponentialSmoothingFilterLambda)]))])

        self.LowPassFilterForDictsOfLists_SetupDict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_Object = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_SetupDict)
        self.LowPassFilterForDictsOfLists_OPEN_FLAG = self.LowPassFilterForDictsOfLists_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LowPassFilterForDictsOfLists_OPEN_FLAG != 1:
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_Object.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            if ftd2xx_IMPORTED_FLAG == 1:
                self.SetAllFTDIdevicesLatencyTimer()
            #########################################################

            #########################################################
            self.FindAssignAndOpenSerialPort()
            #########################################################

            #########################################################
            if self.SerialConnectedFlag != 1:
                return
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedRxThread_ThreadingObject = threading.Thread(target=self.DedicatedRxThread, args=())
        self.DedicatedRxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedTxThread_ThreadingObject = threading.Thread(target=self.DedicatedTxThread, args=())
        self.DedicatedTxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateSetupDictParameters(self, SetupDict):

        #########################################################
        #########################################################
        if "SamplesPerSecond" in SetupDict:
            SamplesPerSecond_TEMP = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("SamplesPerSecond", SetupDict["SamplesPerSecond"], 0.0, 250.0))

            if SamplesPerSecond_TEMP not in self.SamplesPerSecond_AcceptableValuesList:
                self.SamplesPerSecond = 250 #fastest
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Error, SamplesPerSecond must be in " + str(self.SamplesPerSecond_AcceptableValuesList))

            else:
                self.SamplesPerSecond = SamplesPerSecond_TEMP

        else:
            self.SamplesPerSecond = 100

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: SamplesPerSecond: " + str(self.SamplesPerSecond))

        self.SamplesPerSecond_NeedsToBeChangedFlag = 1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedTxThread_TimeToSleepEachLoop" in SetupDict:
            self.DedicatedTxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedTxThread_TimeToSleepEachLoop", SetupDict["DedicatedTxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedTxThread_TimeToSleepEachLoop = 0.005

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: DedicatedTxThread_TimeToSleepEachLoop: " + str(self.DedicatedTxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedRxThread_TimeToSleepEachLoop" in SetupDict:
            self.DedicatedRxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedRxThread_TimeToSleepEachLoop", SetupDict["DedicatedRxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedRxThread_TimeToSleepEachLoop = 0.005

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: DedicatedRxThread_TimeToSleepEachLoop: " + str(self.DedicatedRxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "TorqueDerivative_ExponentialSmoothingFilterLambda" in SetupDict:
            self.TorqueDerivative_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TorqueDerivative_ExponentialSmoothingFilterLambda", SetupDict["TorqueDerivative_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

        else:
            self.TorqueDerivative_ExponentialSmoothingFilterLambda = 0.95 #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: TorqueDerivative_ExponentialSmoothingFilterLambda: " + str(self.TorqueDerivative_ExponentialSmoothingFilterLambda))
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetAllFTDIdevicesLatencyTimer(self, FTDI_LatencyTimer_ToBeSet = 1):

        FTDI_LatencyTimer_ToBeSet = self.LimitNumber_IntOutputOnly(1, 16, FTDI_LatencyTimer_ToBeSet)

        FTDI_DeviceList = ftd2xx.listDevices()
        print("FTDI_DeviceList: " + str(FTDI_DeviceList))

        if FTDI_DeviceList != None:

            for Index, FTDI_SerialNumber in enumerate(FTDI_DeviceList):

                #################################
                try:
                    if sys.version_info[0] < 3: #Python 2
                        FTDI_SerialNumber = str(FTDI_SerialNumber)
                    else:
                        FTDI_SerialNumber = FTDI_SerialNumber.decode('utf-8')

                    FTDI_Object = ftd2xx.open(Index)
                    FTDI_DeviceInfo = FTDI_Object.getDeviceInfo()

                    '''
                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          ", DeviceInfo: " +
                          str(FTDI_DeviceInfo))
                    '''

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not open FTDI device, Exceptions: %s" % exceptions)
                #################################

                #################################
                try:
                    FTDI_Object.setLatencyTimer(FTDI_LatencyTimer_ToBeSet)
                    time.sleep(0.005)

                    FTDI_LatencyTimer_ReceivedFromDevice = FTDI_Object.getLatencyTimer()
                    FTDI_Object.close()

                    if FTDI_LatencyTimer_ReceivedFromDevice == FTDI_LatencyTimer_ToBeSet:
                        SuccessString = "succeeded!"
                    else:
                        SuccessString = "failed!"

                    print("FTDI device with serial number " +
                          str(FTDI_SerialNumber) +
                          " commanded setLatencyTimer(" +
                          str(FTDI_LatencyTimer_ToBeSet) +
                          "), and getLatencyTimer() returned: " +
                          str(FTDI_LatencyTimer_ReceivedFromDevice) +
                          ", so command " +
                          SuccessString)

                except:
                    exceptions = sys.exc_info()[0]
                    print("FTDI device with serial number " + str(FTDI_SerialNumber) + ", could not set/get Latency Timer, Exceptions: %s" % exceptions)
                #################################

        else:
            print("SetAllFTDIdevicesLatencyTimer ERROR: FTDI_DeviceList is empty, cannot proceed.")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FindAssignAndOpenSerialPort(self):
        self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Finding all serial ports...")

        ##############
        SerialNumberToCheckAgainst = str(self.DesiredSerialNumber_USBtoSerialConverter)
        if self.my_platform == "linux" or self.my_platform == "pi":
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst[:-1] #The serial number gets truncated by one digit in linux
        else:
            SerialNumberToCheckAgainst = SerialNumberToCheckAgainst
        ##############

        ##############
        SerialPortsAvailable_ListPortInfoObjetsList = serial.tools.list_ports.comports()
        ##############

        ###########################################################################
        SerialNumberFoundFlag = 0
        for SerialPort_ListPortInfoObjet in SerialPortsAvailable_ListPortInfoObjetsList:

            SerialPortName = SerialPort_ListPortInfoObjet[0]
            Description = SerialPort_ListPortInfoObjet[1]
            VID_PID_SerialNumber_Info = SerialPort_ListPortInfoObjet[2]
            self.MyPrint_WithoutLogFile(SerialPortName + ", " + Description + ", " + VID_PID_SerialNumber_Info)

            if VID_PID_SerialNumber_Info.find(SerialNumberToCheckAgainst) != -1 and SerialNumberFoundFlag == 0: #Haven't found a match in a prior loop
                self.SerialPortNameCorrespondingToCorrectSerialNumber = SerialPortName
                SerialNumberFoundFlag = 1 #To ensure that we only get one device
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Found serial number " + SerialNumberToCheckAgainst + " on port " + self.SerialPortNameCorrespondingToCorrectSerialNumber)
                #WE DON'T BREAK AT THIS POINT BECAUSE WE WANT TO PRINT ALL SERIAL DEVICE NUMBERS WHEN PLUGGING IN A DEVICE WITH UNKNOWN SERIAL NUMBE RFOR THE FIRST TIME.
        ###########################################################################

        ###########################################################################
        if(self.SerialPortNameCorrespondingToCorrectSerialNumber != "default"): #We found a match

            try: #Will succeed as long as another program hasn't already opened the serial line.

                self.SerialObject = serial.Serial(self.SerialPortNameCorrespondingToCorrectSerialNumber, self.SerialBaudRate, timeout=self.SerialTimeoutSeconds, parity=self.SerialParity, stopbits=self.SerialStopBits, bytesize=self.SerialByteSize)
                self.SerialObject.set_buffer_size(rx_size=self.SerialRxBufferSize, tx_size=self.SerialTxBufferSize)
                self.SerialConnectedFlag = 1
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: Serial is connected and open on port: " + self.SerialPortNameCorrespondingToCorrectSerialNumber)

            except:
                self.SerialConnectedFlag = 0
                self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Serial is physically plugged in but IS IN USE BY ANOTHER PROGRAM.")

        else:
            self.SerialConnectedFlag = -1
            self.MyPrint_WithoutLogFile("FindAssignAndOpenSerialPort: ERROR: Could not find the serial device. IS IT PHYSICALLY PLUGGED IN?")
        ###########################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetTorqueReadingUnitsAcceptableValuesList(self):

        return list(self.TorqueReadingUnits_AcceptableValuesList)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedTxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread - self.LastTime_CalculatedFromDedicatedTxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedTxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedRxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread - self.LastTime_CalculatedFromDedicatedRxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedRxThread", DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedRxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CalculateMeasurementTorqueDerivative(self):

        try:
            self.CurrentTime_CalculateMeasurementTorqueDerivative = self.getPreciseSecondsTimeStampString()
            
            self.DataStreamingDeltaT_CalculateMeasurementTorqueDerivative = self.CurrentTime_CalculateMeasurementTorqueDerivative - self.LastTime_CalculateMeasurementTorqueDerivative

            ##########################################################################################################
            if self.DataStreamingDeltaT_CalculateMeasurementTorqueDerivative != 0.0:
                MeasurementTorqueDerivative_NmPerSec_raw = (self.CurrentMeasurementTorque_Nm - self.LastMeasurementTorque_Nm)/self.DataStreamingDeltaT_CalculateMeasurementTorqueDerivative

                ResultsDict = self.LowPassFilterForDictsOfLists_Object.AddDataDictFromExternalProgram(dict([("TorqueDerivative", MeasurementTorqueDerivative_NmPerSec_raw)]))
                MeasurementTorqueDerivative_NmPerSec_filtered = ResultsDict["TorqueDerivative"]["Filtered_MostRecentValuesList"][0]

                MeasurementTorqueDerivative_DictOfConvertedValues = self.ConvertTorqueToAllUnits(MeasurementTorqueDerivative_NmPerSec_filtered, "N.m", TorquePerSecondFlag=1)

                self.LastTime_CalculateMeasurementTorqueDerivative = self.CurrentTime_CalculateMeasurementTorqueDerivative

                return MeasurementTorqueDerivative_DictOfConvertedValues
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CalculateMeasurementTorqueDerivative, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertBytesObjectToString(self, InputBytesObject):

        try:
            if sys.version_info[0] < 3:  # Python 2
                OutputString = str(InputBytesObject)

            else:
                OutputString = InputBytesObject.decode('utf-8')

            return OutputString

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertBytesObjectToString, Exceptions: %s" % exceptions)
            #traceback.print_exc()
            return ""

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendSerialBytearrrayToTx(self, BytearrayToTx, PrintDebugFlag=0):

        if self.SerialConnectedFlag == 1:

            try:

                self.SerialObject.write(BytearrayToTx)

                if PrintDebugFlag == 1:
                    print("SendSerialBytearrrayToTx: ")
                    for ByteToSend in BytearrayToTx:
                        print(str(BytearrayToTx) + ", ")
                    print("\n")

                self.SerialStrToTx_LAST_SENT = str(BytearrayToTx)

                self.MostRecentDataDict["SerialStrToTx_LAST_SENT"] = self.SerialStrToTx_LAST_SENT

            except:
                exceptions = sys.exc_info()[0]
                print("SendSerialStrToTx, exceptions: %s" % exceptions)

        else:
            print("SendSerialStrToTx: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SendSerialStrToTx(self, SerialStrToTx, PrintDebugFlag=0):

        if self.SerialConnectedFlag == 1:

            try:

                SerialStrToTx = SerialStrToTx

                self.SerialObject.write(SerialStrToTx.encode('utf-8'))

                if PrintDebugFlag == 1:

                    print("SendSerialStrToTx: " + str(SerialStrToTx.encode('utf-8')))
                    for ByteToPrint in SerialStrToTx.encode('utf-8'):
                        print(", " + str(ByteToPrint))

                self.SerialStrToTx_LAST_SENT = SerialStrToTx

                self.MostRecentDataDict["SerialStrToTx_LAST_SENT"] = self.SerialStrToTx_LAST_SENT

            except:
                exceptions = sys.exc_info()[0]
                print("SendSerialStrToTx, exceptions: %s" % exceptions)

        else:
            print("SendSerialStrToTx: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def SetUnits(self, UnitsToSet = "N.m", SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=0):

        if self.SerialConnectedFlag == 1:
            try:

                ##########################################################################################################
                if UnitsToSet not in self.TorqueReadingUnits_AcceptableValuesList:
                    UnitsToSet = "N.m"
                    print("SetUnits: Error, UnitsToSet must be contained within " + str(self.UnitsToSet_AcceptableValuesList))
                ##########################################################################################################

                ##########################################################################################################
                if UnitsToSet == "N.m":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x01])
                ##########################################################################################################

                ##########################################################################################################
                if UnitsToSet == "N.cm":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x02])
                ##########################################################################################################

                '''
                ########################################################################################################## On 11/13/24, it appeared that "kgf.m" are not commandable even though they appear in the data-sheet.
                if UnitsToSet == "kgf.m":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x03])
                ##########################################################################################################
                '''

                ##########################################################################################################
                if UnitsToSet == "kgf.cm":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x04])
                ##########################################################################################################

                ##########################################################################################################
                if UnitsToSet == "lbf.ft":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x05])
                ##########################################################################################################

                ##########################################################################################################
                if UnitsToSet == "lbf.in":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x06])
                ##########################################################################################################

                '''
                ########################################################################################################## On 11/13/24, it appeared that "N.mm" are not commandable even though they appear in the data-sheet.
                if UnitsToSet == "N.mm":
                    BytearrayToTx = bytearray([0x53, 0x50, 0x07])
                ##########################################################################################################
                '''

                ##########################################################################################################
                if SendSerialMessageImmediatelyFlag == 0:
                    self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.put(BytearrayToTx)
                else:
                    self.SendSerialBytearrrayToTx(BytearrayToTx, PrintDebugFlag=0)
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("SetUnits event fired, setting units to " + str(UnitsToSet))
                ##########################################################################################################

                ##########################################################################################################
                return 1
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("SetUnits, exceptions: %s" % exceptions)
                traceback.print_exc()

        else:
            print("SetUnits: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def StartVariableStreaming(self, SamplesPerSecond = 100, SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=0):

        if self.SerialConnectedFlag == 1:
            try:

                ##########################################################################################################
                if SamplesPerSecond not in self.SamplesPerSecond_AcceptableValuesList:
                    SamplesPerSecond = 100
                    print("StartVariableStreaming: Error, SamplesPerSecond must be contained within " + str(self.SamplesPerSecond_AcceptableValuesList))
                ##########################################################################################################

                ##########################################################################################################
                if SamplesPerSecond == 10:
                    BytearrayToTx = bytearray([0x3F, 0x43, 0x02])
                ##########################################################################################################

                ##########################################################################################################
                if SamplesPerSecond == 20:
                    BytearrayToTx = bytearray([0x3F, 0x43, 0x03])
                ##########################################################################################################

                ##########################################################################################################
                if SamplesPerSecond == 50:
                    BytearrayToTx = bytearray([0x3F, 0x43, 0x04])
                ##########################################################################################################

                ##########################################################################################################
                if SamplesPerSecond == 100:
                    BytearrayToTx = bytearray([0x3F, 0x43, 0x05])
                ##########################################################################################################

                ##########################################################################################################
                if SendSerialMessageImmediatelyFlag == 0:
                    self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.put(BytearrayToTx)
                else:
                    self.SendSerialBytearrrayToTx(BytearrayToTx, PrintDebugFlag=0)
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("StartVariableStreaming event fired!")
                ##########################################################################################################

                ##########################################################################################################
                return 1
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("StartVariableStreaming, exceptions: %s" % exceptions)

        else:
            print("StartVariableStreaming: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def StopVariableStreaming(self, SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=0):

        if self.SerialConnectedFlag == 1:
            try:

                ##########################################################################################################
                BytearrayToTx = bytearray([0x3F, 0x43, 0xFF])

                if SendSerialMessageImmediatelyFlag == 0:
                    self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.put(BytearrayToTx)
                else:
                    self.SendSerialBytearrrayToTx(BytearrayToTx, PrintDebugFlag=0)
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("StopVariableStreaming event fired!")
                ##########################################################################################################

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("StopVariableStreaming, exceptions: %s" % exceptions)

        else:
            print("StopVariableStreaming: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def ResetPeak(self, SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=1):

        if self.SerialConnectedFlag == 1:
            try:

                StringToTx = "CLR" + "\r\n" #CLR: Clear peaks

                if SendSerialMessageImmediatelyFlag == 0:
                    self.DedicatedTxThread_TxMessageStringToSend_Queue.put(StringToTx)
                else:
                    self.SendSerialStrToTx(StringToTx, PrintDebugFlag=0)

                self.ResetPeak_EventHasHappenedFlag = 1

                if PrintDebugFlag == 1:
                    print("ResetPeak event fired!")

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ResetPeak, exceptions: %s" % exceptions)

        else:
            print("ResetPeak: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTare(self, SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=1):

        if self.SerialConnectedFlag == 1:
            try:

                ##########################################################################################################
                BytearrayToTx = bytearray([0x50, 0x5A, 0x00])

                if SendSerialMessageImmediatelyFlag == 0:
                    self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.put(BytearrayToTx)
                else:
                    self.SendSerialBytearrrayToTx(BytearrayToTx, PrintDebugFlag=0)

                self.ResetTare_EventHasHappenedFlag = 1
                ##########################################################################################################

                if PrintDebugFlag == 1:
                    print("ResetTare event fired!")

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ResetTare, exceptions: %s" % exceptions)

        else:
            print("ResetTare: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FlushSerial(self, PrintDebugFlag=1):

        if self.SerialConnectedFlag == 1:
            try:

                ##########################################################################################################
                self.SerialObject.reset_input_buffer()
                ##########################################################################################################

                if PrintDebugFlag == 1:
                    print("FlushSerial event fired!")

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("FlushSerial, exceptions: %s" % exceptions)

        else:
            print("FlushSerial: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertTorqueToAllUnits(self, InputValue, InputUnits, TorquePerSecondFlag = 0):

        try:

            ##########################################################################################################
            ConvertedValue_Nm = -11111.0
            ConvertedValue_Ncm = -11111.0
            ConvertedValue_Nmm = -11111.0
            ConvertedValue_KGFcm = -11111.0
            ConvertedValue_LBFft = -11111.0
            ConvertedValue_LBFin = -11111.0

            InputValue = float(InputValue)
            InputUnits = str(InputUnits)

            if InputUnits == "N.m":
                ConvertedValue_Nm = InputValue*1.0

            elif InputUnits == "N.cm":
                ConvertedValue_Nm = InputValue*0.010

            elif InputUnits == "N.mm":
                ConvertedValue_Nm = InputValue*0.010 #IT'S ONLY A FIRMWARE BUG IN THE SHIMPO THAT SAYS N-MM WHEN IT'S ACTUALLY N-CM.

            elif InputUnits == "kgf.cm":
                ConvertedValue_Nm = InputValue*0.0980665

            elif InputUnits == "kgf.m":
                ConvertedValue_Nm = InputValue*0.980665

            elif InputUnits == "lbf.ft":
                ConvertedValue_Nm = InputValue * 1.355817952

            elif InputUnits == "lbf.in":
                ConvertedValue_Nm = InputValue * 0.112984429

            else:
                ConvertedValue_Nm = -11111.0

            ##########################################################################################################

            ##########################################################################################################
            if InputUnits in self.TorqueReadingUnits_AcceptableValuesList:
                ConvertedValue_Nm = ConvertedValue_Nm/1.0
                ConvertedValue_Ncm = ConvertedValue_Nm/0.010
                ConvertedValue_Nmm = ConvertedValue_Nm / 0.010 #IT'S ONLY A FIRMWARE BUG IN THE SHIMPO THAT SAYS N-MM WHEN IT'S ACTUALLY N-CM.
                ConvertedValue_KGFcm = ConvertedValue_Nm/0.0980665
                ConvertedValue_KGFm = ConvertedValue_Nm/9.80665002863885
                ConvertedValue_LBFft = ConvertedValue_Nm/1.355817952
                ConvertedValue_LBFin = ConvertedValue_Nm/0.112984429

            else:
                self.MyPrint_WithoutLogFile("ConvertTorqueToAllUnits: InputUnits not recognized. Input value: " + str(InputValue) + ", InputUnits: " + str(InputUnits))

            if TorquePerSecondFlag == 0:
                ConvertedValuesDict = dict([("N.m", ConvertedValue_Nm),
                                            ("N.cm", ConvertedValue_Ncm),
                                            ("N.mm", ConvertedValue_Nmm),
                                            ("kgf.cm", ConvertedValue_KGFcm),
                                            ("kgf.m", ConvertedValue_KGFm),
                                            ("lbf.ft", ConvertedValue_LBFft),
                                            ("lbf.in", ConvertedValue_LBFin)])
            else:
                ConvertedValuesDict = dict([("N.m.PerSec", ConvertedValue_Nm),
                                            ("N.cm.PerSec", ConvertedValue_Ncm),
                                            ("N.mm.PerSec", ConvertedValue_Nmm),
                                            ("kgf.cm.PerSec", ConvertedValue_KGFcm),
                                            ("kgf.m.PerSec", ConvertedValue_KGFm),
                                            ("lbf.ft.PerSec", ConvertedValue_LBFft),
                                            ("lbf.in.PerSec", ConvertedValue_LBFin)])

            return ConvertedValuesDict
            ##########################################################################################################


        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("ConvertTorqueToAllUnits InputValue: " + str(InputValue) + ", InputUnits: " + str(InputUnits) + ", exceptions: %s" % exceptions)

            if TorquePerSecondFlag == 0:

                return dict([("N.m", ConvertedValue_Nm),
                            ("N.cm", ConvertedValue_Ncm),
                            ("N.mm", ConvertedValue_Nmm),
                            ("kgf.cm", ConvertedValue_KGFcm),
                            ("kgf.m", ConvertedValue_KGFm),
                            ("lbf.ft", ConvertedValue_LBFft),
                            ("lbf.in", ConvertedValue_LBFin)])

            else:
                return dict([("N.m.PerSec", ConvertedValue_Nm),
                            ("N.cm.PerSec", ConvertedValue_Ncm),
                            ("N.mm.PerSec", ConvertedValue_Nmm),
                            ("kgf.cm.PerSec", ConvertedValue_KGFcm),
                            ("kgf.m.PerSec", ConvertedValue_KGFm),
                            ("lbf.ft.PerSec", ConvertedValue_LBFft),
                            ("lbf.in.PerSec", ConvertedValue_LBFin)])

            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedTxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedTxThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 1

        self.SetUnits(self.TorqueReadingUnits_DefaultUnits, SendSerialMessageImmediatelyFlag=1, PrintDebugFlag=0)
        time.sleep(self.TimeBetweenSendingSettingCommands)
        self.StartVariableStreaming(100, SendSerialMessageImmediatelyFlag=1, PrintDebugFlag=0)
        time.sleep(self.TimeBetweenSendingSettingCommands)

        self.StartingTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            try:
                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedTxThread
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                '''
                ##########################################################################################################
                if self.TorqueReadingUnits_DefaultUnitsHaveBeenSetFlag == 0:

                    for Counter in range(0, 5):
                        self.SetUnits(self.TorqueReadingUnits_DefaultUnits, SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=1)

                    self.TorqueReadingUnits_DefaultUnitsHaveBeenSetFlag = 1
                ##########################################################################################################
                '''

                ##########################################################################################################
                if self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag == 1:

                    if self.DataStream_State == 1:
                        self.DataStream_State = 0
                        self.StopVariableStreaming(PrintDebugFlag=1)
                    else:
                        self.DataStream_State = 1
                        self.StartVariableStreaming(self.SamplesPerSecond, PrintDebugFlag=1)

                    self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if self.ToggleUnits_EventNeedsToBeFiredFlag == 1:
                    self.SetUnits(self.TorqueReadingUnits_AcceptableValuesList[self.ToggleUnits_EventCounter], SendSerialMessageImmediatelyFlag=0, PrintDebugFlag=1)

                    self.ToggleUnits_EventCounter = self.ToggleUnits_EventCounter + 1

                    if self.ToggleUnits_EventCounter == len(self.TorqueReadingUnits_AcceptableValuesList):
                        self.ToggleUnits_EventCounter = 0

                    self.ToggleUnits_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if self.ResetPeak_EventNeedsToBeFiredFlag == 1:
                    self.ResetPeak()
                    self.ResetPeak_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if self.ResetTare_EventNeedsToBeFiredFlag == 1:
                    self.ResetTare()
                    self.ResetTare_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if self.FlushSerial_EventNeedsToBeFiredFlag == 1:
                    self.FlushSerial(PrintDebugFlag=1)
                    self.FlushSerial_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.DedicatedTxThread_TxMessageStringToSend_Queue.qsize() > 0:

                    ##########################################################################################################
                    TxDataToWrite = self.DedicatedTxThread_TxMessageStringToSend_Queue.get()

                    self.SendSerialStrToTx(TxDataToWrite, PrintDebugFlag=1)

                    time.sleep(self.TimeBetweenSendingSettingCommands)
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.qsize() > 0:

                    ##########################################################################################################
                    TxDataToWrite = self.DedicatedTxThread_TxMessageBytearrayToSend_Queue.get()

                    self.SendSerialBytearrrayToTx(TxDataToWrite, PrintDebugFlag=0)

                    time.sleep(self.TimeBetweenSendingSettingCommands)
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_DedicatedTxThread_Filtered()

                if self.DedicatedTxThread_TimeToSleepEachLoop > 0.0:
                    if self.DedicatedTxThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, DedicatedTxThread, Inner Exceptions: %s" % exceptions)
                traceback.print_exc()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedTxThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedRxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedRxThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedRxThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ###########################################################################################################
                ##########################################################################################################
                RxMessage = self.SerialObject.read_until(b'\r') #Example of what we should expect: " -0.0045 N.m",
                RxMessageString = self.ConvertBytesObjectToString(RxMessage)
                RxMessageString = RxMessageString.replace("\r", "")
                RxMessageStringList = RxMessageString.split(" ")  # Split apart single string into list based on a space (" ").
                RxMessageStringList = list(filter(None, RxMessageStringList))  # Remove list elements that are empty

                ##########################################################################################################
                if self.PrintAllReceivedSerialMessageForDebuggingFlag == 1:
                    print("RxMessage: " + str(RxMessage) + ", Type = " + str(type(RxMessageStringList)) + ", Len = " + str(len(RxMessageStringList)) + ", Message = " + str(RxMessageStringList))
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if len(RxMessageString) > 0:

                    try:

                        ##########################################
                        self.UpdateFrequencyCalculation_DedicatedRxThread_Filtered()
                        ##########################################

                        ##########################################
                        self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                        self.MostRecentDataDict["MostRecentMessage_Raw"] = RxMessageString
                        self.MostRecentDataDict["MostRecentMessage_SplitIntoList"] = RxMessageStringList
                        self.MostRecentDataDict["MostRecentMessage_LengthOfSplitIntoList"] = len(RxMessageStringList)
                        ##########################################
                        
                        ##########################################
                        MeasurementTorque = RxMessageStringList[0]
                        MeasurementUnits = RxMessageStringList[1]
                        ##########################################

                        ##########################################
                        self.MostRecentDataDict["MeasurementUnits"] = MeasurementUnits

                        self.MostRecentDataDict["MeasurementTorque_DictOfConvertedValues"] = self.ConvertTorqueToAllUnits(float(MeasurementTorque), MeasurementUnits)

                        self.CurrentMeasurementTorque_Nm = self.MostRecentDataDict["MeasurementTorque_DictOfConvertedValues"]["N.m"]

                        self.MostRecentDataDict["MeasurementTorqueDerivative_DictOfConvertedValues"] = self.CalculateMeasurementTorqueDerivative()

                        self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread
                        self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedTxThread

                        self.MostRecentDataDict["ResetPeak_EventHasHappenedFlag"] = self.ResetPeak_EventHasHappenedFlag
                        self.MostRecentDataDict["ResetTare_EventHasHappenedFlag"] = self.ResetTare_EventHasHappenedFlag
                        self.MostRecentDataDict["TorqueDerivative_ExponentialSmoothingFilterLambda"] = self.TorqueDerivative_ExponentialSmoothingFilterLambda

                        self.LastMeasurementTorque_Nm = self.CurrentMeasurementTorque_Nm
                        ##########################################

                        ##########################################################################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("DedicatedRxThread, message receiving section, Exceptions: %s" % exceptions)
                        #traceback.print_exc()
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                    if self.DedicatedRxThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedRxThread, Exceptions: %s" % exceptions)
                #traceback.print_exc()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, CreateGUIobjects event fired.")

        #################################################
        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################
        #################################################

        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################

        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                        "\nUSBtoSerialConverter Serial Number: " + str(self.DesiredSerialNumber_USBtoSerialConverter)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ButtonsFrame = Frame(self.myFrame)
        self.ButtonsFrame.grid(row = 1, column = 0, padx=self.GUI_PADX, pady=self.GUI_PADY, rowspan = 1, columnspan = 2)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetPeak_Button = Button(self.ButtonsFrame, text="Reset Peak", state="normal", width=15, command=lambda: self.ResetPeak_Button_Response())
        self.ResetPeak_Button.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetTare_Button = Button(self.ButtonsFrame, text="Reset Tare", state="normal", width=20, command=lambda: self.ResetTare_Button_Response())
        self.ResetTare_Button.grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ToggleDataStreamOnOrOff_Button = Button(self.ButtonsFrame, text="Toggle Data", state="normal", width=15, command=lambda: self.ToggleDataStreamOnOrOff_Button_Response())
        self.ToggleDataStreamOnOrOff_Button.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ToggleUnits_Button = Button(self.ButtonsFrame, text="Toggle Units", state="normal", width=15, command=lambda: self.ToggleUnits_Button_Response())
        self.ToggleUnits_Button.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.FlushSerial_Button = Button(self.ButtonsFrame, text="Flush Serial", state="normal", width=20, command=lambda: self.FlushSerial_Button_Response())
        self.FlushSerial_Button.grid(row=3, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    '''
    ##########################################################################################################
    ##########################################################################################################
    def EnabledState_Button_Response(self):

        self.MyPrint_WithoutLogFile("EnabledState_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopInAllModes_Button_Response(self):

        self.MyPrint_WithoutLogFile("StopInAllModes_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################
    '''

    ##########################################################################################################
    ##########################################################################################################
    def ResetPeak_Button_Response(self):

        self.ResetPeak_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ResetPeak_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetTare_Button_Response(self):

        self.ResetTare_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ResetTare_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ToggleDataStreamOnOrOff_Button_Response(self):

        self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ToggleDataStreamOnOrOff_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ToggleUnits_Button_Response(self):

        self.ToggleUnits_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ToggleUnits_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FlushSerial_Button_Response(self):

        self.FlushSerial_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("FlushSerial_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 5,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 3)
                    #######################################################

                    #######################################################
                    self.ToggleDataStreamOnOrOff_Button["text"] = "Data Stream\n" + str(self.DataStream_State)

                    if self.DataStream_State == 1:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightGreenColor
                    else:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightRedColor
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################