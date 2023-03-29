import os
import json
from datetime import datetime


def readConfig(fileName):
    if os.path.exists(fileName):
        with open(fileName, "r") as fRead:
            return json.load(fRead)
    else:
        return None


def getCurDate(format="%y%m%d%H%M"):
    return datetime.now().strftime(format)


def writeLog(path, deviceName, log):
    if path == "":
        path = os.path.join(os.path.abspath(''), "output")

    if not os.path.exists(path):
        os.makedirs(path)

    fileName = f"{deviceName}-{getCurDate()}.csv"
    filePath = os.path.join(path, fileName)

    with open(filePath, "w") as f:
        f.write("Modbus register information\n")
        f.write(f"Data name, Register Address, Number of Registers, Data type, Expected reponse(Modbus), Received response(SSH), Status\n")
        f.writelines(log)
    
    return (filePath, fileName)