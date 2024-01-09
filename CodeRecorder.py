#Work By Nerex
#https://github.com/nerexbcd/

import json
import broadlink
import os
from base64 import b64encode, b64decode

broadlink_device_ip = os.environ["broadlink_device_ip"]

base_json = {
    "minTemperature": 0,
    "maxTemperature": 0,
    "operationModes": [],
    "fanModes": [],
    "swingModes": [],
    "commands": {}
}

if (broadlink_device_ip == ""):
    print("broadlink_device_ip environment variable is not set")
    exit()

output_files = os.listdir('./output')

if (len(output_files) > 0):
    box_width = len(max(output_files, key=len))+4 
    box_width = 10 if box_width < 10 else box_width

    print("┏",(box_width-2)*"-","┓",sep="")

    for file in output_files:
        print("|",((box_width-2-len(file))//2)*" ",file,((box_width-2-len(file))//2)*" ","|", sep="")

    print("┗",(box_width-2)*"-","┛",sep="")
    print()
    selected = input("Select a file by order to record (0 for new)(ex:. 1 for first ...): ")
    selected_file = "" if selected == "0" else output_files[int(selected)-1]
else:
    selected_file = ""

if (selected_file == ""):
    device_code = input("Enter the Device Code: ")
    selected_file = device_code+".json"
    with open("./output/"+selected_file, "w") as file:
        json.dump(base_json , file)

device_json_path = "./output/"+selected_file
device = broadlink.hello(host=broadlink_device_ip)
device.auth()

with open(device_json_path) as file:
    device_json = json.load(file)

minTemperature = device_json['minTemperature']
maxTemperature = device_json['maxTemperature']
operationModes = device_json['operationModes']
fanModes = device_json['fanModes']
swingModes = device_json['swingModes']



print("Wainting for IR Command...")
device.enter_learning()
input("Press 'ENTER' After IR Command is sent to Broadlink Device")
ir_packet = device.check_data()
print('IR Packet Recived')
print(b64encode(ir_packet).decode('utf-8'))


