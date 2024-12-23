#!/usr/bin/env python3
import pydbus
import time
import sys
import asyncio
from datetime import datetime
from gi.repository import GLib
from plotter import convertBytetoDec, plot, init
# return codes
# 0: OK
# 1: connection failed
# 2: reading value failed


dev_id = '00:80:E1:26:64:F1'

uuid_numberSavedActData = '00002b45-0000-1000-8000-00805f9b34fb'
uuid_savedActData = '00002ad3-0000-1000-8000-00805f9b34fb'


def getCharacteristicPath(dev_path, uuid):
    mng_objs = mngr.GetManagedObjects()
    for path in mng_objs:
        chr_uuid = mng_objs[path].get(
            'org.bluez.GattCharacteristic1', {}).get('UUID')
        # print(chr_uuid)
        if path.startswith(dev_path) and chr_uuid == uuid:
            return path


def getNumberOfData():

    numberSavedActData_chr_path = getCharacteristicPath(
        device._path, uuid_numberSavedActData)
    numberSavedActData_chr = bus.get(
        bluez_service, numberSavedActData_chr_path)
    got_numberSavedActData = numberSavedActData_chr.ReadValue({})
    numberSavedActData = 0
    numberSavedActData = got_numberSavedActData[0] << 8
    numberSavedActData += got_numberSavedActData[1]
    return numberSavedActData


def readData(numberSavedActData):

    savedActData_chr_path = getCharacteristicPath(
        device._path, uuid_savedActData)
    savedActData_chr = bus.get(bluez_service, savedActData_chr_path)
    for i in range(numberSavedActData):
        ByteArray = savedActData_chr.ReadValue({})
        print(ByteArray)
        hexArray = bytes(ByteArray).hex()
        print(hexArray)

        if (numberSavedActData > 0):

            print(ByteArray[4])
            print(ByteArray[5])
            print(ByteArray[6])
            print(ByteArray[7])
            print(ByteArray[8])
            print(ByteArray[9])

            convertBytetoDec(
                ByteArray[4], ByteArray[5], ByteArray[6], ByteArray[7], ByteArray[8], ByteArray[9])
            plot()

        hoursStart = ByteArray[3]
        minutesStart = ByteArray[4]
        secondsStart = ByteArray[5]

        hoursEnd = ByteArray[9]
        minutesEnd = ByteArray[10]
        secondsEnd = ByteArray[11]

        datetimeStart_str = f"{hoursStart:02d}:{minutesStart:02d}:{secondsStart:02d}"

        dateformat_str = '%H:%M:%S'
        datetimeStart_object = datetime.strptime(
            datetimeStart_str, dateformat_str)
        timestampStart = round(datetime.timestamp(datetimeStart_object) * 1000)

        datetimeEnd_str = f"{hoursEnd:02d}:{minutesEnd:02d}:{secondsEnd:02d}"
        datetimeEnd_object = datetime.strptime(datetimeEnd_str, dateformat_str)
        timestampEnd = round(datetime.timestamp(datetimeEnd_object) * 1000)

        data2save = (dev_id + "_" + str(timestampStart) +
                     "_" + str(timestampEnd))

        print("data to be saved = ", data2save)

        print("datetimeStart_object = ", datetimeStart_object)
        print("datetimeEnd_object = ", datetimeEnd_object)
        print("i =: ", i)


def getData():
    print("in function getData")
    numberSavedActData = getNumberOfData()
    print(numberSavedActData)
    if numberSavedActData != 0:
        print("Found Data")
        readData(numberSavedActData)

    else:
        print("No data")
    return True


# M A I N
# DBus object paths
bluez_service = 'org.bluez'
adapter_path = '/org/bluez/hci0'
# device_path is org/bluez/hci0/dev_00_80_E1_26_44_8F for Motion 1
device_path = f"{adapter_path}/dev_{dev_id.replace(':', '_')}"

# Setup DBus, adapter and device objects
bus = pydbus.SystemBus()
adapter = bus.get(bluez_service, adapter_path)
mngr = bus.get(bluez_service, '/')

try:
    device = bus.get(bluez_service, device_path)

    print('Device found')
except:
    print("Device not found, trying discovery.")
    try:
        adapter.StartDiscovery()
        time.sleep(0.5)
        device = bus.get(bluez_service, device_path)
    except:
        print("Device not found!")
        sys.exit(1)

# Connect to device (assume device has already been paired via bluetoothctl)
try:
    device.Connect()
    # print(device.ServicesResolved)
    print("Device is connected.")
except:
    print("Connection failed!")
    sys.exit(1)


# Wait to resolve services from device
while not device.ServicesResolved:
    print('Service not resolved')
    time.sleep(0.5)

init()
# Read number of saved activity data
GLib.timeout_add(2000, getData)

mainloop = GLib.MainLoop()
try:
    mainloop.run()
except KeyboardInterrupt:
    mainloop.quit()
