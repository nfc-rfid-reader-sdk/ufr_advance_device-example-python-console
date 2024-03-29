import ctypes
from ctypes import *
import sys
import platform
#import os
#import array
import ErrorCodes
from Functions import *
##########################################################################
# dll loading

if sys.platform.startswith('win'):
    from ctypes import windll
    import msvcrt
    # used for specifying lib for OS version, 32/64bit
    if platform.architecture()[0] == '32bit':
        uFR = ctypes.windll.LoadLibrary(
            "ufr-lib//windows//x86//uFCoder-x86.dll")
    elif platform.architecture()[0] == '64bit':
        uFR = ctypes.windll.LoadLibrary(
            "ufr-lib//windows//x86_64//uFCoder-x86_64.dll")
elif sys.platform.startswith('linux'):
    # used for specifying lib for OS version, 32/64bit
    if platform.architecture()[0] == '32bit':
        uFR = cdll.LoadLibrary("ufr-lib//linux//x86//libuFCoder-x86.so")
    elif platform.architecture()[0] == '64bit':
        uFR = cdll.LoadLibrary("ufr-lib//linux//x86_64//libuFCoder-x86_64.so")

elif sys.platform.startswith('darwin'):
    uFR = cdll.LoadLibrary("ufr-lib//macos//x86_64//libuFCoder-x86_64.dylib")
##########################################################################

def usage():
    print(" +------------------------------------------------+")
    print(" |        uFR Advance RTC/EEPROM example          |")
    print(" +------------------------------------------------+")
    print(" --------------------------------------------------")
    print("  (1) - Get card info")
    print("  (2) - Get reader time")
    print("  (3) - Set reader time")
    print("  (4) - Reader EEPROM read")
    print("  (5) - Reader EEPROM write")
    print("  (6) - Change reader password")
    print(" --------------------------------------------------")

##########################################################################

def menu(option):
    
    if str(option) == "1":
        getCardInfo()
    elif str(option) == "2":
        getReaderTime()
    elif str(option) == "3":
        setReaderTime()
    elif str(option) == "4":
        readerEEPROMRead()
    elif str(option) == "5":
        readerEEPROMWrite()
    elif str(option) == "6":
        changeReaderPassword()
    else:
        usage()

    print(" --------------------------------------------------")

##########################################################################

def ReaderOpenEx(reader_type, port_name, port_interface, arg):
    openReader = uFR.ReaderOpenEx
    openReader.argtypes = (c_uint32, c_char_p, c_uint32, c_void_p)
    openReader.restype = c_uint
    b = c_char_p(port_name.encode('utf-8'))
    return openReader(reader_type, b, port_interface, arg)

##########################################################################

def ReaderOpen():
    openReader = uFR.ReaderOpen
    return openReader()

##########################################################################

def ReaderUISignal(light, sound):
    uiSignal = uFR.ReaderUISignal
    uiSignal.argtypes = (c_ubyte, c_ubyte)
    uiSignal.restype = c_uint
    uiSignal(light, sound)

##########################################################################

def ReaderClose():
    func = uFR.ReaderClose
    return func()

##########################################################################


if __name__ == '__main__':

    # For opening uFR Nano Online UDP mode use:
    # status = ReaderOpenEx(0, "ip_address:port_number", 85, 0)
    #
    # For opening uFR Nano Online TCP/IP mode use:
    # status = ReaderOpenEx(0, "ip address:port_number", 84, 0)
    #
    # For opening uFR Nano Online without reset/RTS on ESP32 - transparent mode 115200 use:
    # status = ReaderOpenEx(2, 0, 0, "UNIT_OPEN_RESET_DISABLE")

    print("---------------------------------------------------")
    print("https://www.d-logic.net/nfc-rfid-reader-sdk/")
    print("---------------------------------------------------")
    print("uFR Advance console example application version 1.0")
    print("---------------------------------------------------")

    print("Select reader opening mode:")
    print("1. Simple reader open")
    print("2. Advanced reader open")
    mode = input()
    if mode != "":
        mode = int(mode)
    else:
        print("You must select reader port open mode. Try again:")
        mode = input()
    if mode == 1:
        status = ReaderOpen()
    elif mode == 2:
        print("Enter reader type:")
        reader_type = input()
        reader_type = int(reader_type)

        print("Enter port name:")
        port_name = input()

        print("Enter port interface:")
        port_interface = input()

        print("Enter additional argument:")
        arg = input()

        if port_interface == "U":
            port_interface = 85
        elif port_interface == "T":
            port_interface = 84
        else:
            port_interface = int(port_interface)

        status = ReaderOpenEx(reader_type, port_name, port_interface, arg)
        # for uFR online example:
        # status = ReaderOpenEx(0, "192.168.1.101:8881", 85, 0)
        #status = ReaderOpenEx(0,"192.168.1.108",85,0)

    else:
        print("Invalid selection")
        print("Press ENTER to quit")
        input()
        sys.exit(1)

    if status == 0:
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Result: Port successfully opened")
        print("---------------------------------------------")
        #ReaderUISignal(1, 1)
    else:
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        print("Result: Port not opened")
        print("---------------------------------------------")
        print("Press ENTER to quit")
        input()
        sys.exit(1)
    key = str()

    usage()
    if sys.platform.startswith('win'):
        print("press ESC and hit enter to exit.")
    else:
        print("press ESC and hit enter to exit.")

    while key != '\x1b':
        if sys.platform.startswith('win'):
            key = msvcrt.getwch()
        else:
            key = input()
        menu(key)
    ReaderClose()
