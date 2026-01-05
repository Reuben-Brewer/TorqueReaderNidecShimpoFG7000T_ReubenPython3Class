# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 01/05/2026

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
from CSVdataLogger_ReubenPython3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from TorqueReaderNidecShimpoFG7000T_ReubenPython3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import math
import traceback
import collections
import keyboard
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

##########################################################################################################
##########################################################################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        return ""
        # traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCalNmackInterval_Milliseconds
    global USE_GUI_FLAG

    global TorqueReaderNidecShimpoFG7000T_NumberOfSensors
    global TorqueReaderNidecShimpoFG7000T_ListOfObjects
    global TorqueReaderNidecShimpoFG7000T_OPEN_FLAG
    global SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG
    global TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts
    global TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:

        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1 and SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG == 1:
                for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                    TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels[Index]["text"]  = ConvertDictToProperlyFormattedStringForPrinting(TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index], NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
            #########################################################

            #########################################################
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1 and SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG == 1:
                for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                    TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].GUI_update_clock()
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCalNmackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG
    global CSVdataLogger_MostRecentDict_IsSavingFlag

    print("ExitProgram_Callback event fired!")

    if CSVdataLogger_MostRecentDict_IsSavingFlag == 0:
        EXIT_PROGRAM_FLAG = 1
    else:
        print("ExitProgram_Callback, ERROR! Still saving data.")
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCalNmackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    global TorqueReaderNidecShimpoFG7000T_NumberOfSensors
    global TorqueReaderNidecShimpoFG7000T_ListOfObjects
    global TorqueReaderNidecShimpoFG7000T_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_TorqueReaderNidecShimpoFG7000T
    global Tab_MyPrint
    global Tab_CSVdataLogger

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_TorqueReaderNidecShimpoFG7000T = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_TorqueReaderNidecShimpoFG7000T, text='   Torque   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_TorqueReaderNidecShimpoFG7000T = root
        Tab_MyPrint = root
        Tab_CSVdataLogger = root
        #################################################

    ##########################################################################################################

    #################################################
    #################################################
    global TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels
    TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels = []
    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
        TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels.append(Label(Tab_MainControls, text="TorqueReaderNidecShimpoFG7000T_MostRecentDict_Label", width=120, font=("Helvetica", 10)))
        TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfLabels[Index].grid(row=Index, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    ButtonsFrame = Frame(Tab_MainControls)
    ButtonsFrame.grid(row = Index + 1, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 1)
    #################################################
    #################################################

    #################################################
    #################################################
    ResetPeak_Button = Button(ButtonsFrame, text="Reset Peak", state="normal", width=15, command=lambda: ResetPeak_Button_Response())
    ResetPeak_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    ResetTare_Button = Button(ButtonsFrame, text="Reset Tare", state="normal", width=20, command=lambda: ResetTare_Button_Response())
    ResetTare_Button.grid(row=0, column=1, padx=10, pady=10, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1:
        for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
            TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].CreateGUIobjects(TkinterParent=Tab_TorqueReaderNidecShimpoFG7000T)
    #################################################
    #################################################

    #################################################
    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.CreateGUIobjects(TkinterParent=Tab_CSVdataLogger)
    #################################################
    #################################################

    #################################################
    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the calNmack function for when the window's closed.
    root.title("test_program_for_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCalNmackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetPeak_Button_Response():
    global ResetPeak_EventNeedsToBeFiredFlag

    ResetPeak_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ResetTare_Button_Response():
    global ResetTare_EventNeedsToBeFiredFlag

    ResetTare_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_TorqueReaderNidecShimpoFG7000T_FLAG
    USE_TorqueReaderNidecShimpoFG7000T_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG
    SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_TorqueReaderNidecShimpoFG7000T
    global GUI_COLUMN_TorqueReaderNidecShimpoFG7000T
    global GUI_PADX_TorqueReaderNidecShimpoFG7000T
    global GUI_PADY_TorqueReaderNidecShimpoFG7000T
    global GUI_ROWSPAN_TorqueReaderNidecShimpoFG7000T
    global GUI_COLUMNSPAN_TorqueReaderNidecShimpoFG7000T
    GUI_ROW_TorqueReaderNidecShimpoFG7000T = 0

    GUI_COLUMN_TorqueReaderNidecShimpoFG7000T = 0
    GUI_PADX_TorqueReaderNidecShimpoFG7000T = 1
    GUI_PADY_TorqueReaderNidecShimpoFG7000T = 1
    GUI_ROWSPAN_TorqueReaderNidecShimpoFG7000T = 1
    GUI_COLUMNSPAN_TorqueReaderNidecShimpoFG7000T = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 2

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 3

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_TorqueReaderNidecShimpoFG7000T
    global Tab_MyPrint

    global GUI_RootAfterCalNmackInterval_Milliseconds
    GUI_RootAfterCalNmackInterval_Milliseconds = 30

    global ResetPeak_EventNeedsToBeFiredFlag
    ResetPeak_EventNeedsToBeFiredFlag = 0

    global ResetTare_EventNeedsToBeFiredFlag
    ResetTare_EventNeedsToBeFiredFlag = 0

    global SumOfTorquesFromAllSensors_Nm
    SumOfTorquesFromAllSensors_Nm = 0

    global SumOfTorqueDerivativesFromAllSensors_Nm
    SumOfTorqueDerivativesFromAllSensors_Nm = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global TorqueReaderNidecShimpoFG7000T_ListOfObjects
    TorqueReaderNidecShimpoFG7000T_ListOfObjects = list()

    global TorqueReaderNidecShimpoFG7000T_OPEN_FLAG
    TorqueReaderNidecShimpoFG7000T_OPEN_FLAG = 0

    global TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList
    TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList = ["FT79OUSHA"]

    global TorqueReaderNidecShimpoFG7000T_NumberOfSensors
    TorqueReaderNidecShimpoFG7000T_NumberOfSensors = len(TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList)

    global TorqueReaderNidecShimpoFG7000T_OPEN_FLAG_ListOfFlags
    TorqueReaderNidecShimpoFG7000T_OPEN_FLAG_ListOfFlags = [0]*TorqueReaderNidecShimpoFG7000T_NumberOfSensors

    #################################################
    global TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts
    TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts = list()

    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
        TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts.append(dict())
    #################################################

    global TorqueReadingUnits_AcceptableValuesList
    TorqueReadingUnits_AcceptableValuesList = ["N.m", "N.cm", "kgf.cm", "lbf.ft", "lbf.in"]

    global TorqueReadingUnits_AcceptableValuesList_ListCounter
    TorqueReadingUnits_AcceptableValuesList_ListCounter = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_Object

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_MostRecentDict_IsSavingFlag
    CSVdataLogger_MostRecentDict_IsSavingFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):

        global TorqueReaderNidecShimpoFG7000T_GUIparametersDict
        TorqueReaderNidecShimpoFG7000T_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_TorqueReaderNidecShimpoFG7000T_FLAG),
                                                                ("EnableInternal_MyPrint_Flag", 0),
                                                                ("NumberOfPrintLines", 10),
                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                ("GUI_ROW", GUI_ROW_TorqueReaderNidecShimpoFG7000T + Index),
                                                                ("GUI_COLUMN", GUI_COLUMN_TorqueReaderNidecShimpoFG7000T),
                                                                ("GUI_PADX", GUI_PADX_TorqueReaderNidecShimpoFG7000T),
                                                                ("GUI_PADY", GUI_PADY_TorqueReaderNidecShimpoFG7000T),
                                                                ("GUI_ROWSPAN", GUI_ROWSPAN_TorqueReaderNidecShimpoFG7000T),
                                                                ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_TorqueReaderNidecShimpoFG7000T)])

        global TorqueReaderNidecShimpoFG7000T_SetupDict
        TorqueReaderNidecShimpoFG7000T_SetupDict = dict([("GUIparametersDict", TorqueReaderNidecShimpoFG7000T_GUIparametersDict),
                                                        ("DesiredSerialNumber_USBtoSerialConverter", TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList[Index]),
                                                        ("NameToDisplay_UserSet", "TorqueReaderNidecShimpoFG7000T: Sensor " + TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList[Index]),
                                                        ("DedicatedTxThread_TimeToSleepEachLoop", 0.008),
                                                        ("DedicatedRxThread_TimeToSleepEachLoop", 0.008),
                                                        ("TorqueDerivative_ExponentialSmoothingFilterLambda", 0.95)])

        if USE_TorqueReaderNidecShimpoFG7000T_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
            try:
                TorqueReaderNidecShimpoFG7000T_ListOfObjects.append(TorqueReaderNidecShimpoFG7000T_ReubenPython3Class(TorqueReaderNidecShimpoFG7000T_SetupDict))
                TorqueReaderNidecShimpoFG7000T_OPEN_FLAG_ListOfFlags[Index] = TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].OBJECT_CREATED_SUCCESSFULLY_FLAG

            except:
                exceptions = sys.exc_info()[0]
                print("TorqueReaderNidecShimpoFG7000T_ReubenPython3ClassObject __init__ on SerialNumber" + TorqueReaderNidecShimpoFG7000T_DevicesToReadSerialNumbersList[Index] + ", exceptions: %s" % exceptions)
                traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    TorqueReaderNidecShimpoFG7000T_OPEN_FLAG = 1
    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
        for IndividualFlag in TorqueReaderNidecShimpoFG7000T_OPEN_FLAG_ListOfFlags:
            if IndividualFlag != 1:
                TorqueReaderNidecShimpoFG7000T_OPEN_FLAG = 0
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_TorqueReaderNidecShimpoFG7000T_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG != 1:
                print("Failed to open TorqueReaderNidecShimpoFG7000T_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global CSVdataLogger_GUIparametersDict
    CSVdataLogger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                            ("EnableInternal_MyPrint_Flag", 1),
                                            ("NumberOfPrintLines", 10),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                            ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                            ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                            ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    #################################################
    CSVdataLogger_SetupDict_VariableNamesForHeaderList = ["Time (S)",
                                                         "SumOfTorquesFromAllSensors (Nm)"]
    #################################################

    #################################################
    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
        CSVdataLogger_SetupDict_VariableNamesForHeaderList.append("Torque " + str(Index) + " (Nm)")
    #################################################

    #################################################
    CSVdataLogger_SetupDict_VariableNamesForHeaderList.append("SumOfTorqueDerivativesFromAllSensors (Nm/s)")
    #################################################

    #################################################
    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
        CSVdataLogger_SetupDict_VariableNamesForHeaderList.append("TorqueDerivative " + str(Index) + " (Nm/s)")
    #################################################

    #################################################
    print("CSVdataLogger_SetupDict_VariableNamesForHeaderList: " + str(CSVdataLogger_SetupDict_VariableNamesForHeaderList))
    #################################################

    global CSVdataLogger_SetupDict
    CSVdataLogger_SetupDict = dict([("GUIparametersDict", CSVdataLogger_GUIparametersDict),
                                    ("NameToDisplay_UserSet", "CSVdataLogger"),
                                    ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                    ("FileNamePrefix", "CSV_file_"),
                                    ("VariableNamesForHeaderList", CSVdataLogger_SetupDict_VariableNamesForHeaderList),
                                    ("MainThread_TimeToSleepEachLoop", 0.002),
                                    ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_Object = CSVdataLogger_ReubenPython3Class(CSVdataLogger_SetupDict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_GUIparametersDict
    MyPrint_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_SetupDict
    MyPrint_SetupDict = dict([("NumberOfPrintLines", 10),
                            ("WidthOfPrintingLabel", 200),
                            ("PrintToConsoleFlag", 1),
                            ("LogFileNameFullPath", os.path.join(os.getcwd(), "TestLog.txt")),
                            ("GUIparametersDict", MyPrint_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_NameList
    MyPlotterPureTkinterStandAloneProcess_NameList = ["SumOfTorquesFromAllSensors_Nm", "SumOfTorqueDerivativesFromAllSensors_Nm", "Channel2", "Channel3", "Channel4", "Channel5"]

    global MyPlotterPureTkinterStandAloneProcess_ColorList
    MyPlotterPureTkinterStandAloneProcess_ColorList = ["Red", "Green", "Blue", "Black", "Purple", "Orange"]

    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("GraphCanvasWidth", 900),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "My plotting example!"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])

    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", MyPlotterPureTkinterStandAloneProcess_NameList),
                                                                                                        ("MarkerSizeList", [2]*6),
                                                                                                        ("LineWidthList", [2]*6),
                                                                                                        ("IncludeInXaxisAutoscaleCalculationList", [1]*6),
                                                                                                        ("IncludeInYaxisAutoscaleCalculationList", [1]*6),
                                                                                                        ("ColorList", MyPlotterPureTkinterStandAloneProcess_ColorList)])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 100),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 5.0),
                                                            ("Y_min", -5.0),
                                                            ("Y_max", 5.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("GraphNumberOfLeadingZeros", 0),
                                                            ("GraphNumberOfDecimalPlaces", 3),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder")),
                                                            ("KeepPlotterWindowAlwaysOnTopFlag", 0),
                                                            ("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", 0),
                                                            ("AllowResizingOfWindowFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_TorqueReaderNidecShimpoFG7000T = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    LoopCounter = 0
    TorqueReadingUnits_AcceptableValuesList_ListCounter = 0
    print("Starting main loop 'test_program_for_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    while(EXIT_PROGRAM_FLAG == 0):

        try:
            ###################################################
            ###################################################
            ###################################################
            CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
            ###################################################
            ###################################################
            ###################################################

            ################################################### GET's
            ###################################################
            ###################################################
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1:

                SumOfTorquesFromAllSensors_Nm = 0
                SumOfTorqueDerivativesFromAllSensors_NmPerSec = 0

                for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                    TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index] = TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].GetMostRecentDataDict()
                    #print("TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[ " + str(Index) + "]: " + str(TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]))

                    try:
                        if "MeasurementTorque_DictOfConvertedValues" in TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index] and "MeasurementTorqueDerivative_DictOfConvertedValues" in TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]:
                            SumOfTorquesFromAllSensors_Nm = SumOfTorquesFromAllSensors_Nm + TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]["MeasurementTorque_DictOfConvertedValues"]["N.m"]
                            SumOfTorqueDerivativesFromAllSensors_NmPerSec = SumOfTorqueDerivativesFromAllSensors_NmPerSec + TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]["MeasurementTorqueDerivative_DictOfConvertedValues"]["N.m.PerSec"]

                            #print("SumOfTorquesFromAllSensors_Nm: " + str(SumOfTorquesFromAllSensors_Nm) + ", SumOfTorqueDerivativesFromAllSensors_NmPerSec: " + str(SumOfTorqueDerivativesFromAllSensors_NmPerSec))
                    except:
                        pass
            ###################################################
            ###################################################
            ###################################################

            ################################################### SET's
            ###################################################
            ###################################################
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1:

                ##########################################################################################################
                if ResetPeak_EventNeedsToBeFiredFlag == 1:

                    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                        TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].ResetPeak()

                    ResetPeak_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if ResetTare_EventNeedsToBeFiredFlag == 1:

                    for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                        TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].ResetTare()

                    ResetTare_EventNeedsToBeFiredFlag = 0
                ##########################################################################################################

                ##########################################################################################################
                if LoopCounter == 1000:
                    LoopCounter = 0

                    #TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].SetUnits(TorqueReadingUnits_AcceptableValuesList[TorqueReadingUnits_AcceptableValuesList_ListCounter], PrintDebugFlag=1)

                    TorqueReadingUnits_AcceptableValuesList_ListCounter = TorqueReadingUnits_AcceptableValuesList_ListCounter + 1
                    if TorqueReadingUnits_AcceptableValuesList_ListCounter == len(TorqueReadingUnits_AcceptableValuesList):
                        TorqueReadingUnits_AcceptableValuesList_ListCounter = 0

                else:
                    LoopCounter = LoopCounter + 1
                ##########################################################################################################

            ###################################################
            ###################################################
            ###################################################

            #################################################### SET's
            ####################################################
            ####################################################
            if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

                ####################################################
                ####################################################
                ListToWrite = []
                ListToWrite.append(CurrentTime_MainLoopThread)
                ListToWrite.append(SumOfTorquesFromAllSensors_Nm)

                ####################################################
                for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                    try:
                        if "MeasurementTorque_DictOfConvertedValues" in TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]:
                            ListToWrite.append(TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]["MeasurementTorque_DictOfConvertedValues"]["N.m"])
                    except:
                        pass
                ####################################################

                ListToWrite.append(SumOfTorqueDerivativesFromAllSensors_NmPerSec)

                ####################################################
                for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
                    try:
                        if "MeasurementTorque_DictOfConvertedValues" in TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]:
                            ListToWrite.append(TorqueReaderNidecShimpoFG7000T_MostRecentDict_ListOfDicts[Index]["MeasurementTorqueDerivative_DictOfConvertedValues"]["N.m.PerSec"])
                    except:
                        pass
                ####################################################

                ####################################################
                ####################################################

                CSVdataLogger_Object.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
            ####################################################
            ####################################################
            ####################################################

            #################################################### SET's
            ####################################################
            ###################################################
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

                ####################################################
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:

                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(MyPlotterPureTkinterStandAloneProcess_NameList[0:2],
                                                                                                            [CurrentTime_MainLoopThread]*2,
                                                                                                            [SumOfTorquesFromAllSensors_Nm, SumOfTorqueDerivativesFromAllSensors_NmPerSec])


                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                ####################################################

            ####################################################
            ####################################################
            ###################################################

            time.sleep(1.0/90.0)

        except:
            exceptions = sys.exc_info()[0]
            print("test_program_for_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_TorqueReaderNidecShimpoFG7000T_ReubenPython3Class.")

    #################################################
    if TorqueReaderNidecShimpoFG7000T_OPEN_FLAG == 1:
        for Index in range(0, TorqueReaderNidecShimpoFG7000T_NumberOfSensors):
            TorqueReaderNidecShimpoFG7000T_ListOfObjects[Index].ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################