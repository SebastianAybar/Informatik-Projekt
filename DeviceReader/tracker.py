#!/usr/bin/env python3
import pydbus
import time
import sys
from plotter import convertBytetoDec
from datetime import datetime
from gi.repository import GLib
import paho.mqtt.client as mqtt
import json


# Get Configuration from json file
with open('DeviceReader/config.json', 'r') as file:
    data = json.load(file)

# Fill variables with the data given from the json
dev_id = data['dev_id']
uuid_numberSavedActData = data['uuid_numberSavedActData']
uuid_savedActData = data['uuid_savedActData']

mqttBroker = data['mqttBroker']
mqtt_topic = data['mqtt_topic']
client_id = data['client_id']
uuid_rtc = data['uuid_rtc']


def getCharacteristicPath(dev_path, uuid):
    mng_objs = mngr.GetManagedObjects()
    for path in mng_objs:
        chr_uuid = mng_objs[path].get(
            'org.bluez.GattCharacteristic1', {}).get('UUID')
        # print(chr_uuid)
        if path.startswith(dev_path) and chr_uuid == uuid:
            return path


def getNumberOfData():
    try:
        numberSavedActData_chr_path = getCharacteristicPath(
            device._path, uuid_numberSavedActData)
        numberSavedActData_chr = bus.get(
            bluez_service, numberSavedActData_chr_path)
        got_numberSavedActData = numberSavedActData_chr.ReadValue({})
        numberSavedActData = 0
        numberSavedActData = got_numberSavedActData[0] << 8
        numberSavedActData += got_numberSavedActData[1]
        return numberSavedActData
    except:
        print("Device is disconnected")


def readData(numberSavedActData):
    savedActData_chr_path = getCharacteristicPath(
        device._path, uuid_savedActData)
    savedActData_chr = bus.get(bluez_service, savedActData_chr_path)
    for i in range(numberSavedActData):
        got_savedActData = savedActData_chr.ReadValue({})

        yearStart = got_savedActData[0]
        if yearStart == 0:
            yearStart = 10
        monthStart = got_savedActData[1]
        dateStart = got_savedActData[2]
        hoursStart = got_savedActData[3]
        minutesStart = got_savedActData[4]
        secondsStart = got_savedActData[5]

        yearEnd = got_savedActData[6]
        if yearEnd == 0:
            yearEnd = 10
        monthEnd = got_savedActData[7]
        dateEnd = got_savedActData[8]
        hoursEnd = got_savedActData[9]
        minutesEnd = got_savedActData[10]
        secondsEnd = got_savedActData[11]

        posture = got_savedActData[12]
        shortTermActivityLevel = got_savedActData[13]
        longTermActivityLevel = got_savedActData[14]
        stepCounter = got_savedActData[15] << 24
        stepCounter += got_savedActData[16] << 16
        stepCounter += got_savedActData[17] << 8
        stepCounter += got_savedActData[18]
        jumps = got_savedActData[19] << 8
        jumps += got_savedActData[20]
        runs = got_savedActData[21] << 8
        runs += got_savedActData[22]
        walkingSteps = got_savedActData[23] << 8
        walkingSteps += got_savedActData[24]
        situps = got_savedActData[25] << 8
        situps += got_savedActData[26]
        squats = got_savedActData[27] << 8
        squats += got_savedActData[28]
        pushups = got_savedActData[29] << 8
        pushups += got_savedActData[30]
        averageSpeed = got_savedActData[31] << 24
        averageSpeed += got_savedActData[32] << 16
        averageSpeed += got_savedActData[33] << 8
        averageSpeed += got_savedActData[34]

        # In order to have always four digits in the strings of jumps, runs, walking steps and three in squats, situps and pushups
        jumps_ones = jumps % 10
        jumps_tens = int(((jumps - jumps_ones) % 100) / 10)
        jumps_hundreds = int(
            ((jumps - jumps_ones - jumps_tens * 10) % 1000) / 100)
        jumps_thousands = int(
            ((jumps - jumps_ones - jumps_tens * 10 - jumps_hundreds * 100) % 10000) / 1000)

        runs_ones = runs % 10
        runs_tens = int(((runs - runs_ones) % 100) / 10)
        runs_hundreds = int(((runs - runs_ones - runs_tens * 10) % 1000) / 100)
        runs_thousands = int(
            ((runs - runs_ones - runs_tens * 10 - runs_hundreds * 100) % 10000) / 1000)

        walking_steps_ones = walkingSteps % 10
        walking_steps_tens = int(
            ((walkingSteps - walking_steps_ones) % 100) / 10)
        walking_steps_hundreds = int(
            ((walkingSteps - walking_steps_ones - walking_steps_tens * 10) % 1000) / 100)
        walking_steps_thousands = int(
            ((walkingSteps - walking_steps_ones - walking_steps_tens * 10 - walking_steps_hundreds * 100) % 10000) / 1000)

        squats_ones = squats % 10
        squats_tens = int(((squats - squats_ones) % 100) / 10)
        squats_hundreds = int(
            ((squats - squats_ones - squats_tens * 10) % 1000) / 100)

        situps_ones = situps % 10
        situps_tens = int(((situps - situps_ones) % 100) / 10)
        situps_hundreds = int(
            ((situps - situps_ones - situps_tens * 10) % 1000) / 100)

        pushups_ones = pushups % 10
        pushups_tens = int(((pushups - pushups_ones) % 100) / 10)
        pushups_hundreds = int(
            ((pushups - pushups_ones - pushups_tens * 10) % 1000) / 100)

        averageSpeed_ones = averageSpeed % 10
        averageSpeed_tens = int(
            ((averageSpeed - averageSpeed_ones) % 100) / 10)
        averageSpeed_hundreds = int(
            ((averageSpeed - averageSpeed_ones - averageSpeed_tens * 10) % 1000) / 100)
        averageSpeed_thousands = int(
            ((averageSpeed - averageSpeed_ones - averageSpeed_tens * 10 - averageSpeed_hundreds * 100) % 10000) / 1000)

        datetimeStart_str = str(yearStart) + "/" + str(monthStart) + "/" + str(
            dateStart) + " " + str(hoursStart) + ":" + str(minutesStart) + ":" + str(secondsStart)
#        print("datetimeStart_str = ", datetimeStart_str)
        datetimeStart_object = datetime.strptime(
            datetimeStart_str, '%y/%m/%d %H:%M:%S')
#        print("datetimeStart_object = ", datetimeStart_object)
        timestampStart = round(datetime.timestamp(datetimeStart_object) * 1000)
#        print("timestampStart = ", timestampStart)

        datetimeEnd_str = str(yearEnd) + "/" + str(monthEnd) + "/" + str(
            dateEnd) + " " + str(hoursEnd) + ":" + str(minutesEnd) + ":" + str(secondsEnd)
        datetimeEnd_object = datetime.strptime(
            datetimeEnd_str, '%y/%m/%d %H:%M:%S')
        timestampEnd = round(datetime.timestamp(datetimeEnd_object) * 1000)

        data2save = (dev_id + "_" + str(timestampStart) + "_" + str(timestampEnd)
                     + "_" + str(posture) + "_" + str(shortTermActivityLevel) +
                     "_" + str(longTermActivityLevel)
                     + "_" + str(jumps_thousands) + str(jumps_hundreds) +
                     str(jumps_tens) + str(jumps_ones)
                     + "_" + str(runs_thousands) + str(runs_hundreds) +
                     str(runs_tens) + str(runs_ones)
                     + "_" + str(walking_steps_thousands) + str(walking_steps_hundreds) +
                     str(walking_steps_tens) + str(walking_steps_ones)
                     + "_" + str(squats_hundreds) +
                     str(squats_tens) + str(squats_ones)
                     + "_" + str(situps_hundreds) +
                     str(situps_tens) + str(situps_ones)
                     + "_" + str(pushups_hundreds) +
                     str(pushups_tens) + str(pushups_ones)
                     + "_" + str(averageSpeed_thousands) + str(averageSpeed_hundreds) +
                     str(averageSpeed_tens) + str(averageSpeed_ones)
                     + "_" + str(stepCounter))

        print("data to be saved = ", data2save)
        print("datetimeStart_object = ", datetimeStart_object)
        print("datetimeEnd_object = ", datetimeEnd_object)

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
        client.connect(mqttBroker, port=1883)
        client.publish(mqtt_topic, data2save, qos=1)


def getData():
    numberSavedActData = getNumberOfData()
    print(numberSavedActData)
    if numberSavedActData != 0:
        readData(numberSavedActData)

    else:
        print("No data")
    return True


def setRTC():
    now = datetime.now()
    year = int(now.strftime("%Y")) - 2000
    month = int(now.strftime("%m"))
    date = int(now.strftime("%d"))
    hours = int(now.strftime("%H"))
    minutes = int(now.strftime("%M"))
    seconds = int(now.strftime("%S"))
    value2set = [date, month, year, hours, minutes, seconds]

    rtc_chr_path = getCharacteristicPath(device._path, uuid_rtc)
    rtc_chr = bus.get(bluez_service, rtc_chr_path)
    rtc_chr.WriteValue(value2set, {})
    print("RTC set.")


# Programm Start
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

except:
    print("Device not found, trying discovery.")
    while True:
        # print(adapter.StartDiscovery())
        if adapter.StartDiscovery():
            device = bus.get(bluez_service, device_path)
        else:
            time.sleep(0.5)
            adapter.StopDiscovery()


# Connect to device (assume device has already been paired via bluetoothctl)
try:
    device.Connect()
    # print(device.ServicesResolved)
    print("Device is connected.")
except:
    print("Waiting for Device.")
    while True:
        device.Connect()
        print("Device is connected.")


# Wait to resolve services from device
while not device.ServicesResolved:
    print('Service not resolved')
    time.sleep(0.5)


setRTC()
# Read number of saved activity data
GLib.timeout_add(2000, getData)

mainloop = GLib.MainLoop()
try:
    mainloop.run()
except KeyboardInterrupt:
    mainloop.quit()
except:
    print("Device is disconnected")
