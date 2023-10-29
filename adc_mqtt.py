import paho.mqtt.client as mqtt
import sys
import time
import serial
import math
import json
import re

def ProcessLine(Line):
    Fields = Line.split(',')
    Values = [0] * 12
    
    for Channel, Field in enumerate(Fields):
        Values[Channel] = float(Field)
                  
    return Values

def on_publish(client,userdata,result):             #create function for callback
    #print("data published \n")
    pass
    
def PublishValueToMQTT(mqtt, Channel, Value, ChannelInfo):
    JsonValue = {'title': ChannelInfo[0], 'raw': str(Value), 'value': "%.2f" % (ChannelInfo[1] * Value), 'unit': ChannelInfo[2]}
       
    res = mqttc.publish(sys.argv[3] + '/' + str(Channel), json.dumps(JsonValue))

    return res[0] == 0
    
    
if len(sys.argv) < 4:
    print ("Usage: python adc_mqtt.py <adc_device> <mqtt_broker> <mqtt_path> [<channel 0> ...]")
    quit()    
    
ser = serial.Serial()
ser.baudrate = 115200
ser.stopbits = 1
ser.bytesize = 8
ser.timeout = 0
ser.port = sys.argv[1]

ser.open()
Line = ''
Position = None

ChannelInfo = []
Channels = len(sys.argv) - 4
for Channel in range(Channels):
    Fields = sys.argv[Channel+4].split('/')
    Fields[0] = re.sub(r"(?<=\w)([A-Z])", r" \1", Fields[0])
    Fields[1] = float(Fields[1])
    ChannelInfo.append(Fields)

while True:
    # Do incoming characters
    Byte = ser.read(1)
    
    if len(Byte) > 0:
        Character = chr(Byte[0])

        if len(Line) > 256:
            Line = ''
        elif Character != '\r':
            if Character == '\n':
                # print(Line)
                Values = ProcessLine(Line)
                
                mqttc = mqtt.Client("the_pit")
                
                mqttc.on_publish = on_publish    
                  
                mqttc.connect(sys.argv[2], 1883)
                
                for Channel in range(Channels):
                    PublishValueToMQTT(mqtt, Channel, Values[Channel], ChannelInfo[Channel]) 
                                   
                mqttc.disconnect()
    
                Line = ''
                time.sleep(0.01)
            else:
                Line = Line + Character
    else:
        time.sleep(0.01)
    
