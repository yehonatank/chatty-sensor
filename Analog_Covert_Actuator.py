from pymodbus.client.sync import ModbusTcpClient
import time


class AnalogCovertActuator():
    def __init__(self, BIT_NUMBER = 0, RESOLUTION = 3):
        self.BIT_NUMBER = BIT_NUMBER
        self.client = ModbusTcpClient('127.0.0.1')
        self.encoded_message = []
        self.last_value = ''
        self.last_time = ''
        self.RESOLUTION = RESOLUTION

    def meausre_time(self):
        return self.last_time

    def set_value(self, value=0):
        self.last_time = int(str(time.time()).split('.')[1][:self.RESOLUTION]) % 2
        self.client.write_register(self.BIT_NUMBER, value)
        if self.last_value != '' and self.last_value != value and self.last_value==0:
            # print ("Covert Actuator: \t", str(time.time()).split('.')[1][:3])
            self.encoded_message.append( str(time.time()).split('.')[1][:self.RESOLUTION] )
        self.last_value = value

    def __del__(self):
        self.client.close()
        # print ("Covert Actuator: \t" + '\t'.join(self.encoded_message))



