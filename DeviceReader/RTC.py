import pydbus
import time
from datetime import datetime
from gi.repository import GLib
import sys
import paho.mqtt.client as mqtt


dev_id = '00:80:E1:27:BE:19'
uuid_rtc = '00002b91-0000-1000-8000-00805f9b34fb'

# mqttBroker = "localhost"
# mqtt_topic = "RTC_datetime"
# client_id = "datetimeRTC"

print("device id = ", dev_id)


def get_characteristic_path(dev_path, uuid):
    mng_objs = mngr.GetManagedObjects()
    for path in mng_objs:
        chr_uuid = mng_objs[path].get(
            'org.bluez.GattCharacteristic1', {}).get('UUID')
        if path.startswith(dev_path) and chr_uuid == uuid:
            return path


def Get_BCD_Code(input):
    bcd_2 = input % 10
    bcd_1 = int((input / 10)) << 4
    return (bcd_1 | bcd_2)


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
# next line will fail, if there is no active connection to the device
# method adapter.StartDiscovery() must be called first
try:
    device = bus.get(bluez_service, device_path)

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
    print("Device is connected.")
except:
    print("Connection failed!")
    sys.exit(1)

# Wait to resolve services from device
while not device.ServicesResolved:
    time.sleep(0.5)


# Get datetime
now = datetime.now()
print("datetime = ", now)
# print("Type of now: ", type(now))


# Set as BCD
# year = int(now.strftime("%Y")) - 2000
# month = int(now.strftime("%m"))
# date = int(now.strftime("%d"))
# hours = int(now.strftime("%H"))
# minutes = int(now.strftime("%M"))
# seconds = int(now.strftime("%S"))
# print("datetime_int: ", year, month, date, hours, minutes, seconds)
# year_bcd = Get_BCD_Code(year)
# month_bcd = Get_BCD_Code(month)
# date_bcd = Get_BCD_Code(date)
# hours_bcd = Get_BCD_Code(hours)
# minutes_bcd = Get_BCD_Code(minutes)
# seconds_bcd = Get_BCD_Code(seconds)
# value2set = [date_bcd, month_bcd, year_bcd, hours_bcd, minutes_bcd, seconds_bcd]

# Set as Binary
year = int(now.strftime("%Y")) - 2000
month = int(now.strftime("%m"))
date = int(now.strftime("%d"))
hours = int(now.strftime("%H"))
minutes = int(now.strftime("%M"))
seconds = int(now.strftime("%S"))
print("datetime_int: ", year, month, date, hours, minutes, seconds)
value2set = [date, month, year, hours, minutes, seconds]

print("value2set: ", value2set)

# Set RTC
try:
    rtc_chr_path = get_characteristic_path(device._path, uuid_rtc)
    rtc_chr = bus.get(bluez_service, rtc_chr_path)
    rtc_chr.WriteValue(value2set, {})
    print("RTC set.")
except:
    print("Setting RTC failed!")
    sys.exit(2)

datetime_RTC = now.strftime("%d.%m.%Y %H:%M:%S")
# client = mqtt.Client(client_id)
# client.connect(mqttBroker, port=1883)
# client.publish(mqtt_topic, datetime_RTC, qos=1)

sys.exit()
