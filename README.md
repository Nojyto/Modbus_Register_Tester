# Modbus register testing

Dependencies listed in [requirements file](requirements.txt) (Python 3.10.6 was used) (Dependencies can be install with **pip install requirements.txt**)

## Device setup before running
The device that is to be tested should have enabled: modbus, ssh and remote access on both of the services.

## Configuration file example
Configuration file consists of:
    -settings section where the required data of the devices is stored
    -tests section where all modbus tests are stored. Each test consists of the modbus address the amount of addresses the data type of the holdig register and the shell command which will be used to get the equivalent data as the modbus register.

```json
{
    {
    "settings": {
        "model": "RUTX11",
        "ssh" :{
            "ip": "192.168.1.1",
            "port": 22,
            "user": "****",
            "pasw": "*********"
        },
        "modbus" :{
            "ip": "192.168.1.1",
            "port": 502,
            "id": 1
        }
    },
    "tests": {
        "System uptime": {
            "adr": 1,
            "cc": 2,
            "rpr": "uint32 (s)",
            "cmnd": "uptime | cut -d ',' -f 1 | cut -c 15-"
        },
        "Mobile signal strength (RSSI in dBm)": {
            "adr": 3,
            "cc": 2,
            "rpr": "int32",
            "cmnd": "gsmctl -q | grep RSSI | cut -c 7-"
        },
        "System temperature (in 0.1 °C)": {
            "adr": 5,
            "cc": 2,
            "rpr": "int32",
            "cmnd": "gsmctl -c"
        },
                ...
```

## Instructions

Executing the program with the help flag (-h) will result in the fallowing output
```
usage: main.py [-h] [-i CONFIGPATH] [-o OUTPUTPATH]

options:
  -h, --help            show this help message and exit
  -i CONFIGPATH, --input CONFIGPATH
                        Specifies path of config.json file.
  -o OUTPUTPATH, --output OUTPUTPATH
                        Specify output directory.
```

Program can be run without additional flags assuming the config.json file is provided beside the main.py file.

The program's shows intermediate results and errors in the console. After finishing all the tests the results are save into the specified file (by default: output/{DeviceName}-{Time}.csv)