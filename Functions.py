import ctypes
from ctypes import *
import ErrorCodes
from advance_example import uFR
import datetime
#################################################################
def getCardInfo():

    sak = c_ubyte(0)
    uid = (c_ubyte*10)()
    card_len = c_ubyte(0)
    c = "CARD UID -> " # string that will be used for printing out UID

    getCardFunc = uFR.GetCardIdEx
    getCardFunc.argtypes = [POINTER(c_ubyte), (c_ubyte*10), POINTER(c_ubyte)]
    status = getCardFunc(byref(sak), uid, byref(card_len))
    if status == 0:
        for x in range(7):
            c += '%0.2x' % uid[x] + ':'
        print(c.upper()[:-1])
    else:
        print("Getting card info failed.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

def getReaderTime():

    time = (c_ubyte*6)()
    getTimeFunc = uFR.GetReaderTime
    getTimeFunc.argtypes = [(c_ubyte*6)]
    status = getTimeFunc(time)
    if status == 0:
        print("Currently set reader time is:")
        print("Year   - 20%02d" % time[0])
        print("Month  - %02d" % time[1])
        print("Day    - %02d" % time[2])
        print("Hour   - %02d" % time[3])
        print("Minute - %02d" % time[4])
        print("Second - %02d" % time[5])
    else:
        print("Could not get reader time.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

#################################################################

def setReaderTime():
    print("Set reader time options:")
    print("   (1) - Set current PC time")
    print("   (2) - Set reader time manually")
    choice = input()
    
    if choice == "1":
        print("Enter reader password(8 characters, e.g 11111111):")
        pwd_str = input()
        if len(pwd_str) != 8:
            print("Password must be 8 characters long. Try again:")
            pwd_str = input()
            if len(pwd_str) != 8:
                print("Authentication failed. Returning to main...")
                return
        pwd_arr = (c_ubyte*8)()
        pwd_arr = pwd_str.encode('utf-8')
        pwd = (c_ubyte*8)()
        for x in range(8):
            pwd[x] = pwd_arr[x]

        pc_time = datetime.datetime.now()
        set_year = c_ubyte(pc_time.year-2000)
        set_month = c_ubyte(pc_time.month)
        set_day = c_ubyte(pc_time.day)
        set_hour = c_ubyte(pc_time.hour)
        set_minute = c_ubyte(pc_time.minute)
        set_second = c_ubyte(pc_time.second)

        to_set = (c_ubyte*6)()
        to_set[0] = set_year
        to_set[1] = set_month
        to_set[2] = set_day
        to_set[3] = set_hour
        to_set[4] = set_minute
        to_set[5] = set_second

        setTimeFunc = uFR.SetReaderTime
        setTimeFunc.argtypes = [(c_ubyte*8), (c_ubyte*6)]
        status = setTimeFunc(pwd, to_set)
        if status == 0:
            print("Successfully set reader time.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        else:
            print("Could not set reader time.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    
    elif choice == "2":
        print("Enter reader password(8 characters, e.g 11111111):")
        pwd_str = input()
        if len(pwd_str) != 8:
            print("Password must be 8 characters long. Try again:")
            pwd_str = input()
            if len(pwd_str) != 8:
                print("Authentication failed. Returning to main...")
                return
        pwd_arr = (c_ubyte*8)()
        pwd_arr = pwd_str.encode('utf-8')
        pwd = (c_ubyte*8)()
        for x in range(8):
            pwd[x] = pwd_arr[x]

        print("Enter Year you wish to set(1 byte, e.g 19 - 2019. 18 - 2018 etc...): ")
        input_year = input()
        print("Enter Month you wish to set(1 byte, e.g 1 - January, 5 - May etc..): ")
        input_month = input()
        print("Enter Day you wish to set (1 byte, 1-31):")
        input_day = input()
        print("Enter Hour you wish to set (1 byte, 0-23):")
        input_hour = input()
        print("Enter Minute you wish to set (1 byte, 0-59):")
        input_minute = input()
        print("Enter Second you wish to set (1 byte, 0-59):")
        input_second = input()

        to_set = (c_ubyte*6)() 
        to_set[0] = c_ubyte(int(input_year))
        to_set[1] = c_ubyte(int(input_month))
        to_set[2] = c_ubyte(int(input_day))
        to_set[3] = c_ubyte(int(input_hour))
        to_set[4] = c_ubyte(int(input_minute))
        to_set[5] = c_ubyte(int(input_second))

        setTimeFunc = uFR.SetReaderTime
        setTimeFunc.argtypes = [(c_ubyte*8), (c_ubyte*6)]
        status = setTimeFunc(pwd, to_set)
        if status == 0:
            print("Successfully set reader time.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        else:
            print("Could not set reader time.")
            print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
        
    else:
        print("Invalid selection. Returning to main...")

#################################################################


def readerEEPROMRead():
    
    print("Enter EEPROM address from which you wish to start reading:")
    address = input()
    address = int(address) 
    print("Enter how many bytes to read:")
    length = input()
    length = int(length)

    readDataFunc = uFR.ReaderEepromRead
    readDataFunc.argtypes = [(c_ubyte*length), c_uint32, c_uint32]
    data = (c_ubyte*length)()

    status = readDataFunc(data, c_uint32(address), c_uint32(length))
    c = "DATA: \n"
    if status == 0:
        print("EEPROM data succesfully read.")
        for x in range(length):
            if x != 0:
                if x%32 == 0:
                    c+="\n"
            c +=  '%0.2x' % data[x] + " "
               
        print(c.upper()[:-1])
    
    else:
        print("Could not read EEPROM data.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
#################################################################

def readerEEPROMWrite():
    print("Enter EEPROM address from which you wish to start writing:")
    addr_str = input()
    if addr_str == "":
        print("You must enter EEPROM address. Try again:")
        addr_str =  input()
        if addr_str == "":
            print("Invalid input. Returning to main...")
            return
    address = c_uint32(int(addr_str))
    
    print("Enter data you wish to write into EEPROM:")
    data_str = input()
    data_length = len(data_str)
    if data_length > 256 or data_length < 0:
        print("Maximum length of data written can be 128 bytes. Try again:")
        data_str = input()
        if data_length > 256 or data_length < 0:
            print("Invalid input. Returning to main...")
            return
    tmp_data = data_str.encode('utf-8')
    short_len = int(data_length/2) # nr of bytes needed for storing converted input
    data = (c_ubyte*short_len)()
    for x in range(0, data_length, 2):
        temp = int(tmp_data[x:x+2], 16)
        y = int(x/2)
        data[y] = temp

    print("Enter reader password(8 characters, e.g 11111111):")
    pwd_str = input()
    if len(pwd_str) != 8:
        print("Password must be 8 characters long. Try again:")
        pwd_str = input()
        if len(pwd_str) != 8:
            print("Authentication failed. Returning to main...")
            return
    pwd_arr = (c_ubyte*8)()
    pwd_arr = pwd_str.encode('utf-8')
    pwd = (c_ubyte*8)()
    for x in range(8):
        pwd[x] = pwd_arr[x]
    writeDataFunc = uFR.ReaderEepromWrite
    writeDataFunc.argtypes = [(c_ubyte*short_len), c_uint32, c_uint32, (c_ubyte*8)]
    status = writeDataFunc(data, address, short_len, pwd)
    if status == 0:
        print("EEPROM data succesfully written:")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Could not write EEPROM data.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])

#################################################################

def changeReaderPassword():

    print("Enter old reader password(8 characters):")
    old_pw_str = input()
    if len(old_pw_str) != 8:
        print("Password must be 8 characters long. Try again:")
        old_pw_str = input()
        if len(old_pw_str) != 8:
            print("Authentication failed. Returning to main...")
            return

    old_pw_arr = (c_ubyte*8)()
    old_pw_arr = old_pw_str.encode('utf-8')
    old_pwd = (c_ubyte*8)()
    for x in range(8):
        old_pwd[x] = old_pw_arr[x]

    print("Enter new reader password(8 characters):")
    new_pw_str = input()
    if len(new_pw_str) != 8:
        print("Password must be 8 characters long. Try again:")
        new_pw_str = input()
        if len(new_pw_str) != 8:
            print("Authentication failed. Returning to main...")
            return

    new_pw_arr = (c_ubyte*8)()
    new_pw_arr = new_pw_str.encode('utf-8')
    new_pwd = (c_ubyte*8)()
    for x in range(8):
        new_pwd[x] = new_pw_arr[x]

    changePassFunc = uFR.ChangeReaderPassword
    changePassFunc.argtypes = [(c_ubyte*8), (c_ubyte*8)]
    status = changePassFunc(old_pwd, new_pwd)
    if status == 0:
        print("Reader password succesfully changed.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
    else:
        print("Could not change reader password.")
        print("Status: " + ErrorCodes.UFCODER_ERROR_CODES[status])
