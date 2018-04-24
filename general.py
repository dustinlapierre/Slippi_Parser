from random import randint, randrange
from structures import *
from ast import literal_eval
import struct
import time

#pick between two things
def choose(option1, option2):
    choice = randint(0, 1)
    if(choice == 0):
        return option1
    return option2

#select randomly from a list
def choose_list(choice_list):
    random_index = randrange(0, len(choice_list))
    return choice_list[random_index]

def flatten(x, min, max):
    return ((x-min) / (max-min))

#constructs hex string from list of bytes
#returns int conversion
def hex_to_int(hexlist):
    final = "0x"
    for value in hexlist:
        if(len(value[2:]) == 1):
            final += "0"
        final += value[2:]
    return int(literal_eval(final))

#constructs hex string from list of bytes
#returns float conversion
def hex_to_float(hexlist):
    final = ""
    for value in hexlist:
        if(len(value[2:]) == 1):
            final += "0"
        final += value[2:]
    return struct.unpack('!f', bytes.fromhex(final))[0]

#read a given length of bytes from replay
def read_frame(replay, length):
    data = []
    while(len(data) < length):
        position = replay.tell()
        byte = replay.read(1)
        if(not byte):
            time.sleep(1/120)
            replay.seek(position)
        else:
            data.append(hex(ord(byte)))
    return data
