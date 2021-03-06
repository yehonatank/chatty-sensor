from pymodbus.client.sync import ModbusTcpClient
import time
import random

COVERT_MESSAGE = '000100100011010001010111100010010101110011101111'


class ChattySensor():
    def __init__(self, BIT_NUMBER = 0,RESOLUTION = 3):
        self.BIT_NUMBER = BIT_NUMBER
        self.client = ModbusTcpClient('127.0.0.1')
        self.encoded_message = []
        self.last_value = ''
        self.delayed_time = 0
        self.data = ''
        self.index = 0
        self.RESOLUTION = RESOLUTION


    def get_data(self):
        return self.data

    def next_bit(self):
        self.index = self.index + 1
        self.index = self.index % len(COVERT_MESSAGE)

    def get_measure(self):
        if random.randint(0, 3) == 0:
            return True

        result = self.client.read_discrete_inputs(self.BIT_NUMBER,1)
        current_value = result.bits[0]
        if self.last_value != '' and self.last_value == True and current_value==False:
            current_time = int(str(time.time()).split('.')[1][:self.RESOLUTION])
            if int(COVERT_MESSAGE[self.index]) == current_time%2:
                delta_time = int(str(time.time()).split('.')[1][:3]) - self.delayed_time
                self.data = "\t".join(["Chatty Sensor:", str(current_time), COVERT_MESSAGE[self.index],str(delta_time) ])
                self.encoded_message.append( str(time.time()).split('.')[1][:self.RESOLUTION])
                self.last_value = current_value
            else:
                current_value = self.last_value
                self.delayed_time = int(str(time.time()).split('.')[1][:3])
        else:
            self.delayed_time = int(str(time.time()).split('.')[1][:3])
            self.last_value = current_value

        return current_value

    def __del__(self):
        self.client.close()
        # print ("Covert Sensor: \t" + '\t'.join(self.encoded_message))


