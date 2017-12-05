# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
import time
import pycom

from network import LoRa
import socket
import struct

execfile('/flash/homewifi/homewifi.py')		# connect to wifi


lora = LoRa(mode=LoRa.LORA, frequency=925000000)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(False)
s.send(b'pysense hello')

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

print('pysense')
while True:
    pycom.rgbled(0x00007f)		# blue
    
    temp1 = mp.temperature()
    altitude = mp.altitude()
    mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    pressure = mpp.pressure()
    temp2 = si.temperature()
    humidity = si.humidity()
    light = lt.light()
    acceleration = li.acceleration()
    roll = li.roll()
    pitch = li.pitch()

    battery = py.read_battery_voltage()
    
    pycom.rgbled(0x007f00)		# green

    print('temp1 is:', temp1,)
    print('altitude is:', altitude,)
    print('pressure is:', pressure)
    print('temp2 is:', temp2)
    print('humidity is:', humidity)
    print('light is:', light)
    print('acceleration is:', acceleration)
    print('roll is:', roll)
    print('pitch is:', pitch)

    print('battery is:', battery)
    print()

    s.send(struct.pack('hh', int(temp2), int(humidity)))
    #s.send('pysense hello loop')
    time.sleep(10)
