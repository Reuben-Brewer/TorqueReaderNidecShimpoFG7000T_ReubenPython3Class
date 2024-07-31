# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision C, 07/31/2024

Verified working on: Python 3.8 for Windows 10/11 64-bit and Raspberry Pi Buster (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

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
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import queue as Queue
##########################################

##########################################
from future.builtins import input as input
########################################## "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

#########################################################

##########################
import serial #___IMPORTANT: pip install pyserial (NOT pip install serial).
from serial.tools import list_ports
##########################

##########################
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
##########################

#########################################################

class TorqueReaderNidecShimpoFG7000T_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0 #unicorn

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0
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
        self.SerialRxBufferSize = 100
        self.SerialTxBufferSize = 100
        self.SerialPortNameCorrespondingToCorrectSerialNumber = "default"
        self.MainThread_TxMessageToSend_Queue = Queue.Queue()
        self.SerialStrToTx_LAST_SENT = ""
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.ReadingModeString_AcceptableValuesList = ["RealTime_CUR",                  #CUR Current mode (real time mode) for primary reading
                                                       "PeakTension_PT",                #PT Peak Tension mode for primary reading
                                                       "PeakCompression_PC",            #PC Peak Compression mode for primary reading
                                                       "PeakClockwise_PCW",             #PCW Peak Clockwise mode for primary reading
                                                       "PeakCounterClockwise_PCCW"]     #PCCW Peak Counter-clockwise mode for primary reading

        self.TorqueReadingUnits_AcceptableValuesList = ["N.m", "N.cm", "N.mm", "kgf.cm", "lbf.ft", "lbf.in"]

        #self.SamplesPerSecond_AcceptableValuesList = [0, 2, 5, 10, 25, 50, 125, 250] #Note: n = 1 = yields 50 times per second.
        #self.AutoShutoffTimeIntegerMinutes0to30_AcceptableValuesList = range(0, 30) #0 = disabled
        #self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_AcceptableValuesList = range(0, 10) #0 = disabled

        #self.ReadingModeString_NeedsToBeChangedFlag = 0
        #self.SamplesPerSecond_NeedsToBeChangedFlag = 0
        #self.AutoShutoffTimeIntegerMinutes0to30_NeedsToBeChangedFlag = 0
        #self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_NeedsToBeChangedFlag = 0

        self.TimeBetweenSendingSettingCommands = 0.010
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread_2 = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

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

        '''
        self.ResetLatchedAlarms_EventNeedsToBeFiredFlag = 0
        self.ResetLatchedAlarms_EventHasHappenedFlag = 0
        '''

        #self.ListCurrentSettingsAndStatus_EventNeedsToBeFiredFlag = 0

        #self.DataStream_State = 1
        #self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 0

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
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

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
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
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
        if "DesiredSerialNumber_USBtoSerialConverter" in setup_dict:
            self.DesiredSerialNumber_USBtoSerialConverter = setup_dict["DesiredSerialNumber_USBtoSerialConverter"]

        else:
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ERROR, must initialize object with 'DesiredSerialNumber_USBtoSerialConverter' argument.")
            return

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: DesiredSerialNumber_USBtoSerialConverter: " + str(self.DesiredSerialNumber_USBtoSerialConverter))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UpdateSetupDictParameters(setup_dict)
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromMainThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                             ("TorqueDerivative", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.TorqueDerivative_ExponentialSmoothingFilterLambda)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
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
        '''
        self.SetAutoShutoffTimeIntegerMinutes0to30(ShutoffTimeIntegerMinutes=self.AutoShutoffTimeIntegerMinutes0to30)
        time.sleep(self.TimeBetweenSendingSettingCommands)

        self.SetReadingMode(self.ReadingModeString)
        time.sleep(self.TimeBetweenSendingSettingCommands)

        self.SetDataOutputStreamNoUnitsOrUnits0or1(UnitsOrUnits0or1=1)
        time.sleep(self.TimeBetweenSendingSettingCommands)

        self.SetSamplesPerSecond(self.SamplesPerSecond)
        time.sleep(self.TimeBetweenSendingSettingCommands)

        self.SaveCurrentSettingsToMemory()
        time.sleep(self.TimeBetweenSendingSettingCommands)
        '''
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
        self.MainThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.25)
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
    def __del__(self):
        pass
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateSetupDictParameters(self, setup_dict):

        '''
        #########################################################
        #########################################################
        if "ReadingModeString" in setup_dict:
            self.ReadingModeString = str(setup_dict["ReadingModeString"])

            if self.ReadingModeString not in self.ReadingModeString_AcceptableValuesList:
                self.ReadingModeString = "RealTime_CUR"
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ERROR, ReadingModeString must be in " + str(self.ReadingModeString_AcceptableValuesList))

        else:
            self.ReadingModeString = "RealTime_CUR"

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: ReadingModeString: " + str(self.ReadingModeString))

        self.ReadingModeString_NeedsToBeChangedFlag = 1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "AutoShutoffTimeIntegerMinutes0to30" in setup_dict:
            AutoShutoffTimeIntegerMinutes0to30_TEMP = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AutoShutoffTimeIntegerMinutes0to30", setup_dict["AutoShutoffTimeIntegerMinutes0to30"], 0.0, 30.0))

            if AutoShutoffTimeIntegerMinutes0to30_TEMP not in self.AutoShutoffTimeIntegerMinutes0to30_AcceptableValuesList:
                self.AutoShutoffTimeIntegerMinutes0to30 = 0  #disabled
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Error, AutoShutoffTimeIntegerMinutes0to30 must be in " + str(self.AutoShutoffTimeIntegerMinutes0to30_AcceptableValuesList))

            else:
                self.AutoShutoffTimeIntegerMinutes0to30 = AutoShutoffTimeIntegerMinutes0to30_TEMP

        else:
            self.AutoShutoffTimeIntegerMinutes0to30 = 0 #disabled

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: AutoShutoffTimeIntegerMinutes0to30: " + str(self.AutoShutoffTimeIntegerMinutes0to30))

        self.AutoShutoffTimeIntegerMinutes0to30_NeedsToBeChangedFlag = 1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "SamplesPerSecond" in setup_dict:
            SamplesPerSecond_TEMP = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("SamplesPerSecond", setup_dict["SamplesPerSecond"], 0.0, 250.0))

            if SamplesPerSecond_TEMP not in self.SamplesPerSecond_AcceptableValuesList:
                self.SamplesPerSecond = 250 #fastest
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Error, SamplesPerSecond must be in " + str(self.SamplesPerSecond_AcceptableValuesList))

            else:
                self.SamplesPerSecond = SamplesPerSecond_TEMP

        else:
            self.SamplesPerSecond = 250 #fastest

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: SamplesPerSecond: " + str(self.SamplesPerSecond))

        self.SamplesPerSecond_NeedsToBeChangedFlag = 1
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FilterExponent0to10ForNumberOfSamplesToBeAveraged" in setup_dict:
            FilterExponent0to10ForNumberOfSamplesToBeAveraged_TEMP = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FilterExponent0to10ForNumberOfSamplesToBeAveraged", setup_dict["FilterExponent0to10ForNumberOfSamplesToBeAveraged"], 0.0, 10.0))

            if FilterExponent0to10ForNumberOfSamplesToBeAveraged_TEMP not in self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_AcceptableValuesList:
                self.FilterExponent0to10ForNumberOfSamplesToBeAveraged = 0  #disabled
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: Error, FilterExponent0to10ForNumberOfSamplesToBeAveraged must be in " + str(self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_AcceptableValuesList))

            else:
                self.FilterExponent0to10ForNumberOfSamplesToBeAveraged = FilterExponent0to10ForNumberOfSamplesToBeAveraged_TEMP

        else:
            self.FilterExponent0to10ForNumberOfSamplesToBeAveraged = 0 #disabled

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: FilterExponent0to10ForNumberOfSamplesToBeAveraged: " + str(self.FilterExponent0to10ForNumberOfSamplesToBeAveraged))

        self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_NeedsToBeChangedFlag = 1
        #########################################################
        #########################################################
        '''

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "TorqueDerivative_ExponentialSmoothingFilterLambda" in setup_dict:
            self.TorqueDerivative_ExponentialSmoothingFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("TorqueDerivative_ExponentialSmoothingFilterLambda", setup_dict["TorqueDerivative_ExponentialSmoothingFilterLambda"], 0.0, 1.0)

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
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
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
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromMainThread", DataStreamingFrequency_CalculatedFromMainThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromMainThread = ResultsDict["DataStreamingFrequency_CalculatedFromMainThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
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

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("TorqueDerivative", MeasurementTorqueDerivative_NmPerSec_raw)]))
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
    def SendSerialStrToTx(self, SerialStrToTx):

        if self.SerialConnectedFlag == 1:

            try:

                #if SerialStrToTx[-1] != "\r":
                #    SerialStrToTx = SerialStrToTx + "\r"

                SerialStrToTx = SerialStrToTx

                self.SerialObject.write(SerialStrToTx.encode('utf-8'))

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

    '''
    ##########################################################################################################
    ##########################################################################################################
    def SetAutoShutoffTimeIntegerMinutes0to30(self, ShutoffTimeIntegerMinutes = 30):

        if self.SerialConnectedFlag == 1:
            try:

                if ShutoffTimeIntegerMinutes not in self.AutoShutoffTimeIntegerMinutes0to30_AcceptableValuesList:
                    ShutoffTimeIntegerMinutes = 0 #disabled
                    print("SetAutoShutoffTimeIntegerMinutes0to30: Error, ShutoffTimeIntegerMinutes must be an integer in " +str(self.AutoShutoffTimeIntegerMinutes0to30_AcceptableValuesList) + ", with 0 = disabled.")

                StringToTx = "AOFF" + str(int(ShutoffTimeIntegerMinutes)) + "\r\n" #AOFFn Auto-shutoff. n=0-30 minutes. 0=auto shutoff disabled
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetAutoShutoffTimeIntegerMinutes0to30, exceptions: %s" % exceptions)

        else:
            print("SetAutoShutoffTimeIntegerMinutes0to30: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SaveCurrentSettingsToMemory(self):

        if self.SerialConnectedFlag == 1:
            try:
                StringToTx = "SAVE" + "\r\n" #SAVE Save current settings in nonvolatile memory
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SaveCurrentSettingsToMemory, exceptions: %s" % exceptions)

        else:
            print("SaveCurrentSettingsToMemory: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ListCurrentSettingsAndStatus(self):

        if self.SerialConnectedFlag == 1:
            try:
                StringToTx = "LIST" + "\r\n" #List current settings and status
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ListCurrentSettingsAndStatus, exceptions: %s" % exceptions)

        else:
            print("ListCurrentSettingsAndStatus: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def SetReadingMode(self, ReadingModeString = "RealTime"):

        if self.SerialConnectedFlag == 1:
            try:

                if ReadingModeString not in self.ReadingModeString_AcceptableValuesList:
                    ReadingModeString = "RealTime_CUR"
                    print("SetReadingMode: Error, ReadingModeString must be contained within " + str(self.ReadingModeString_AcceptableValuesList))

                StringToTx = ReadingModeString.split("_")[1] + "\r\n" #Split apart single string into list based on "_".
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetReadingMode, exceptions: %s" % exceptions)

        else:
            print("SetReadingMode: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def SetDataOutputStreamNoUnitsOrUnits0or1(self, UnitsOrUnits0or1 = 1):

        if self.SerialConnectedFlag == 1:
            try:

                if UnitsOrUnits0or1 == 1:
                    StringToTx = "FULL" + "\r\n" #FULL: USB/RS-232 transmission with units
                else:
                    StringToTx = "NUM"  + "\r\n" #USB/RS-232 transmission without units (only numeric values)

                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetDataOutputStreamNoUnitsOrUnits0or1, exceptions: %s" % exceptions)

        else:
            print("SetDataOutputStreamNoUnitsOrUnits0or1: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## 
    ##########################################################################################################
    def SetSamplesPerSecond(self, SamplesPerSecond = 250):

        if self.SerialConnectedFlag == 1:
            try:

                if SamplesPerSecond not in self.SamplesPerSecond_AcceptableValuesList:
                    SamplesPerSecond = 250
                    print("SetSamplesPerSecond: Error, SamplesPerSecond must be contained within " + str(self.SamplesPerSecond_AcceptableValuesList))

                StringToTx = "AOUT" + str(int(SamplesPerSecond)) + "\r\n" #AOUTn Auto-transmit n times per second n=1,2,5,10,25,50,125,250. 0=disabled. Note: n = 1 = yields 50 times per second.
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetSamplesPerSecond, exceptions: %s" % exceptions)

        else:
            print("SetSamplesPerSecond: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################
    
    ########################################################################################################## 
    ##########################################################################################################
    def StopVariableStreaming(self):

        if self.SerialConnectedFlag == 1:
            try:

                self.StartVariableStreaming(0)

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
    def SetAveraging(self, AveragingEnabledBoolean0or1):

        if self.SerialConnectedFlag == 1:
            try:

                if AveragingEnabledBoolean0or1 not in [0, 1]:
                    print("SetAveraging: Error, AveragingEnabledBoolean0or1 must be 0 or 1.")
                    return

                if AveragingEnabledBoolean0or1 == 1:
                    ##########################################################################################################
                    StringToTx = "A" + "\r\n" #A: Enable Average mode
                    self.MainThread_TxMessageToSend_Queue.put(StringToTx)


                    #AM Select Average mode (if enabled) for primary reading
                    #ATn Average time. n=0.1-300.0 seconds
                    #DELn Initial delay. n=0.1-300.0 seconds
                    #TRFn Trigger Torque. n=value (+ for compression/clockwise, - for tension/counterclockwise)
              
                    ##########################################################################################################

                else:
                    ##########################################################################################################
                    StringToTx = "AD" + "\r\n" #AD: Disable Average mode
                    self.MainThread_TxMessageToSend_Queue.put(StringToTx)
                    ##########################################################################################################

                self.SetAveraging_EventHasHappenedFlag = 1

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetAveraging, exceptions: %s" % exceptions)

        else:
            print("SetAveraging: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetFilterExponent0to10ForNumberOfSamplesToBeAveraged(self, FilterDisplayedOrCurrentReadings0or1, FilterExponent0to10ForNumberOfSamplesToBeAveraged = 0):

        if self.SerialConnectedFlag == 1:
            try:

                if FilterDisplayedOrCurrentReadings0or1 not in [0, 1]:
                    print("SetFilterExponent0to10ForNumberOfSamplesToBeAveraged: Error, FilterDisplayedOrCurrentReadings0or1 must be in [0, 1].")
                    return

                if FilterExponent0to10ForNumberOfSamplesToBeAveraged not in self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_AcceptableValuesList:
                    print("SetFilterExponent0to10ForNumberOfSamplesToBeAveraged: Error, AveragingEnabledBoolean0or1 must be in " + str(self.FilterExponent0to10ForNumberOfSamplesToBeAveraged_AcceptableValuesList))
                    return


                if FilterDisplayedOrCurrentReadings0or1 == 1:
                    ##########################################################################################################
                    StringToTx = "FLTC" + str(int(FilterExponent0to10ForNumberOfSamplesToBeAveraged))  + "\r\n" #Digital filter for displayed readings, n= 0-10, filter = 2exp(n), ex: n=0= no filter, n=10=1024 samples averaged
                    self.MainThread_TxMessageToSend_Queue.put(StringToTx)
                    ##########################################################################################################

                else:
                    ##########################################################################################################
                    StringToTx = "FLTP" + str(int(FilterExponent0to10ForNumberOfSamplesToBeAveraged))  + "\r\n" #Digital filter for displayed readings, n= 0-10, filter = 2exp(n), ex: n=0= no filter, n=10=1024 samples averaged
                    self.MainThread_TxMessageToSend_Queue.put(StringToTx)
                    ##########################################################################################################

                self.SetFilterExponent0to10ForNumberOfSamplesToBeAveraged_EventHasHappenedFlag = 1

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("SetFilterExponent0to10ForNumberOfSamplesToBeAveraged, exceptions: %s" % exceptions)

        else:
            print("SetFilterExponent0to10ForNumberOfSamplesToBeAveraged: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################
    '''

    ########################################################################################################## 
    ##########################################################################################################
    def ResetPeak(self):

        if self.SerialConnectedFlag == 1:
            try:

                StringToTx = "CLR" + "\r\n" #CLR: Clear peaks
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                self.ResetPeak_EventHasHappenedFlag = 1

                #self.ResetLatchedAlarms()

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
    def ResetTare(self):

        if self.SerialConnectedFlag == 1:
            try:
                
                StringToTx = "Z" + "\r\n" #Z: Zero display and perform the CLR function

                self.ResetTare_EventHasHappenedFlag = 1
                
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ResetTare, exceptions: %s" % exceptions)

        else:
            print("ResetTare: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    '''
    ##########################################################################################################
    ##########################################################################################################
    def ResetLatchedAlarms(self):

        if self.SerialConnectedFlag == 1:
            try:
                
                StringToTx = "*1C2" + "\r"

                self.ResetLatchedAlarms_EventHasHappenedFlag = 1
                
                self.MainThread_TxMessageToSend_Queue.put(StringToTx)

                return 1

            except:
                exceptions = sys.exc_info()[0]
                print("ResetLatchedAlarms, exceptions: %s" % exceptions)

        else:
            print("ResetLatchedAlarms: Error, SerialConnectedFlag = 0, cannot issue command.")
            return 0
    ##########################################################################################################
    ##########################################################################################################
    '''

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
                ConvertedValue_LBFft = ConvertedValue_Nm/1.355817952
                ConvertedValue_LBFin = ConvertedValue_Nm/0.112984429

            else:
                self.MyPrint_WithoutLogFile("ConvertTorqueToAllUnits: InputUnits not recognized. Input value: " + str(InputValue) + ", InputUnits: " + str(InputUnits))

            if TorquePerSecondFlag == 0:
                ConvertedValuesDict = dict([("N.m", ConvertedValue_Nm),
                                            ("N.cm", ConvertedValue_Ncm),
                                            ("N.mm", ConvertedValue_Nmm),
                                            ("kgf.cm", ConvertedValue_KGFcm),
                                            ("lbf.ft", ConvertedValue_LBFft),
                                            ("lbf.in", ConvertedValue_LBFin)])
            else:
                ConvertedValuesDict = dict([("N.m.PerSec", ConvertedValue_Nm),
                                            ("N.cm.PerSec", ConvertedValue_Ncm),
                                            ("N.mm.PerSec", ConvertedValue_Nmm),
                                            ("kgf.cm.PerSec", ConvertedValue_KGFcm),
                                            ("lbf.ft.PerSec", ConvertedValue_LBFft),
                                            ("lbf.in.PerSec", ConvertedValue_LBFin)])

            return ConvertedValuesDict
            ##########################################################################################################


        except:
            exceptions = sys.exc_info()[0]
            self.MyPrint_WithoutLogFile("ConvertTorqueToAllUnits InputValue: " + str(InputValue) + ", InputUnits: " + str(InputUnits) + ", exceptions: %s" % exceptions)

            return dict([("N.m", ConvertedValue_Nm),
                                        ("N.cm", ConvertedValue_Ncm),
                                        ("N.mm", ConvertedValue_Nmm),
                                        ("kgf.cm", ConvertedValue_KGFcm),
                                        ("lbf.ft", ConvertedValue_LBFft),
                                        ("lbf.in", ConvertedValue_LBFin)])

            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                self.SendSerialStrToTx("?")
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
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

                        self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromMainThread
                        self.MostRecentDataDict["MostRecentMessage_Raw"] = RxMessageString
                        self.MostRecentDataDict["MostRecentMessage_SplitIntoList"] = RxMessageStringList
                        self.MostRecentDataDict["MostRecentMessage_LengthOfSplitIntoList"] = len(RxMessageStringList)


                        ##########################################
                        MeasurementTorque = RxMessageStringList[0]
                        MeasurementUnits = RxMessageStringList[1]
                        ##########################################

                        ##########################################
                        self.MostRecentDataDict["MeasurementUnits"] = MeasurementUnits

                        self.MostRecentDataDict["MeasurementTorque_DictOfConvertedValues"] = self.ConvertTorqueToAllUnits(float(MeasurementTorque), MeasurementUnits)

                        self.CurrentMeasurementTorque_Nm = self.MostRecentDataDict["MeasurementTorque_DictOfConvertedValues"]["N.m"]

                        self.MostRecentDataDict["MeasurementTorqueDerivative_DictOfConvertedValues"] = self.CalculateMeasurementTorqueDerivative()

                        self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromMainThread"] = self.DataStreamingFrequency_CalculatedFromMainThread

                        self.MostRecentDataDict["ResetPeak_EventHasHappenedFlag"] = self.ResetPeak_EventHasHappenedFlag
                        self.MostRecentDataDict["ResetTare_EventHasHappenedFlag"] = self.ResetTare_EventHasHappenedFlag
                        self.MostRecentDataDict["TorqueDerivative_ExponentialSmoothingFilterLambda"] = self.TorqueDerivative_ExponentialSmoothingFilterLambda

                        self.LastMeasurementTorque_Nm = self.CurrentMeasurementTorque_Nm
                        ##########################################

                        ##########################################################################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("MainThread, message receiving section, Exceptions: %s" % exceptions)
                        traceback.print_exc()
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, MainThread, Inner Exceptions: %s" % exceptions)
                traceback.print_exc()

            ########################################################################################################## These should be outside of the queue and heartbeat
            ##########################################################################################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread_Filtered()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                if self.MainThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
            ###############################################
            ###############################################
            ###############################################

        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")
        self.MainThread_StillRunningFlag = 0
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
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for TorqueReaderNidecShimpoFG7000T_ReubenPython3Class object.")

        #################################################
        #################################################
        self.root = parent
        self.parent = parent
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

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=0, column=1, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ButtonsFrame = Frame(self.myFrame)
        self.ButtonsFrame.grid(row = 1, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 2)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetPeak_Button = Button(self.ButtonsFrame, text="Reset Peak", state="normal", width=15, command=lambda: self.ResetPeak_Button_Response())
        self.ResetPeak_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ResetTare_Button = Button(self.ButtonsFrame, text="Reset Tare", state="normal", width=20, command=lambda: self.ResetTare_Button_Response())
        self.ResetTare_Button.grid(row=0, column=1, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        '''
        #################################################
        #################################################
        self.ResetLatchedAlarms_Button = Button(self.ButtonsFrame, text="Reset Alarms", state="normal", width=20, command=lambda: self.ResetLatchedAlarms_Button_Response())
        self.ResetLatchedAlarms_Button.grid(row=0, column=2, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################
        '''

        '''
        #################################################
        #################################################
        self.ListCurrentSettingsAndStatus_Button = Button(self.ButtonsFrame, text="List Settings", state="normal", width=20, command=lambda: self.ListCurrentSettingsAndStatus_Button_Response())
        self.ListCurrentSettingsAndStatus_Button.grid(row=0, column=2, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ToggleDataStreamOnOrOff_Button = Button(self.ButtonsFrame, text="Toggle Data", state="normal", width=15, command=lambda: self.ToggleDataStreamOnOrOff_Button_Response())
        self.ToggleDataStreamOnOrOff_Button.grid(row=1, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################
        '''

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
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

    '''
    ##########################################################################################################
    ##########################################################################################################
    def ResetLatchedAlarms_Button_Response(self):

        self.ResetLatchedAlarms_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ResetLatchedAlarms_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################
    '''

    '''
    ##########################################################################################################
    ##########################################################################################################
    def ListCurrentSettingsAndStatus_Button_Response(self):

        self.ListCurrentSettingsAndStatus_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ListCurrentSettingsAndStatus_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ToggleDataStreamOnOrOff_Button_Response(self):

        self.ToggleDataStreamOnOrOff_EventNeedsToBeFiredFlag = 1

        #self.MyPrint_WithoutLogFile("ToggleDataStreamOnOrOff_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################
    '''

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

                    '''
                    #######################################################
                    self.ToggleDataStreamOnOrOff_Button["text"] = "Data Stream\n" + str(self.DataStream_State)

                    if self.DataStream_State == 1:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightGreenColor
                    else:
                        self.ToggleDataStreamOnOrOff_Button["bg"] = self.TKinter_LightRedColor
                    #######################################################
                    '''

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

    ##########################################################################################################
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

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
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
    ##########################################################################################################
    ##########################################################################################################
