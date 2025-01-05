import time
import board
from adafruit_seesaw.seesaw import Seesaw
import subprocess, sys, time, kintone, iotutils
from iotutils import getCurrentTimeStamp

sdomain = "puffball"
appId = "15"
token = "lhcB3VcaBOMR3TyK29S7VpDb8RagfI3BIi7LJKO4"

i2c_bus = board.I2C()
interval = 600
ss = Seesaw(i2c_bus, addr=0x36)

while True:
    try:
        moisture = float(ss.moisture_read())
        temp = float(ss.get_temp())

        print(f"temp: {temp}°C, moisture: {moisture}")
    
        payload = {"app": appId,
                   "record": {"temperature": {"value": temp},
                              "moisture": {"value": moisture} }}

        recordId = kintone.uploadRecord(subDomain=sdomain,
                                        apiToken=token,
                                        record=payload)
    
        if recordId is None:
            sys.exit()
        time.sleep(interval)
    except KeyboardInterrupt:
        break
