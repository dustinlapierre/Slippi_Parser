from structures import *
from ast import literal_eval
import struct
import time

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

#parser for game start event data
def parse_game_start(data):
    game_start_data.version.append(hex_to_int([data[0]]))
    game_start_data.version.append(hex_to_int([data[1]]))
    game_start_data.version.append(hex_to_int([data[2]]))
    game_start_data.version.append(hex_to_int([data[3]]))
    game_start_data.game_info_block = data[4:11]
    game_start_data.is_teams = hex_to_int([data[11]])
    game_start_data.stage = hex_to_int(data[18:20])
    game_start_data.character_ID_port1 = hex_to_int([data[100]])
    game_start_data.character_ID_port2 = hex_to_int([data[136]])
    game_start_data.character_ID_port3 = hex_to_int([data[172]])
    game_start_data.character_ID_port4 = hex_to_int([data[208]])
    game_start_data.player_type_port1 = hex_to_int([data[101]])
    game_start_data.player_type_port2 = hex_to_int([data[137]])
    game_start_data.player_type_port3 = hex_to_int([data[173]])
    game_start_data.player_type_port4 = hex_to_int([data[209]])
    game_start_data.character_color_port1 = hex_to_int([data[103]])
    game_start_data.character_color_port2 = hex_to_int([data[139]])
    game_start_data.character_color_port3 = hex_to_int([data[175]])
    game_start_data.character_color_port4 = hex_to_int([data[211]])
    game_start_data.team_ID_port1 = hex_to_int([data[109]])
    game_start_data.team_ID_port2 = hex_to_int([data[145]])
    game_start_data.team_ID_port3 = hex_to_int([data[181]])
    game_start_data.team_ID_port4 = hex_to_int([data[217]])
    game_start_data.random_seed = hex_to_int(data[316:])

#parser for pre frame update event data
def parse_pre_frame(data):
    #parse all values
    pre_frame_data.frame_number = hex_to_int(data[0:4])
    pre_frame_data.player_index = hex_to_int([data[4]])
    pre_frame_data.is_follower = hex_to_int([data[5]])
    pre_frame_data.random_seed = hex_to_int(data[6:10])
    pre_frame_data.action_state = hex_to_int(data[10:12])
    pre_frame_data.x_pos = hex_to_float(data[12:16])
    pre_frame_data.y_pos = hex_to_float(data[16:20])
    pre_frame_data.facing_direction = hex_to_float(data[20:24])
    pre_frame_data.joystick_x = hex_to_float(data[24:28])
    pre_frame_data.joystick_y = hex_to_float(data[28:32])
    pre_frame_data.c_stick_x = hex_to_float(data[32:36])
    pre_frame_data.c_stick_y = hex_to_float(data[36:40])
    pre_frame_data.trigger = hex_to_float(data[40:44])
    pre_frame_data.buttons = hex_to_int(data[44:48])
    pre_frame_data.physical_buttons = hex_to_int(data[48:50])
    pre_frame_data.physical_l = hex_to_float(data[50:54])
    pre_frame_data.physical_r = hex_to_float(data[54:])

#parser for post frame update event data
def parse_post_frame(data):
    #parse all values
    post_frame_data.frame_number = hex_to_int(data[0:4])
    post_frame_data.player_index = hex_to_int([data[4]])
    post_frame_data.is_follower = hex_to_int([data[5]])
    post_frame_data.internal_character_ID = hex_to_int([data[6]])
    post_frame_data.action_state = hex_to_int(data[7:9])
    x = hex_to_float(data[9:13])
    if(x <= 0.1 and x >= -0.1):
        x = 0
    post_frame_data.x_pos = round(x, 2)
    y = hex_to_float(data[13:17])
    if(y <= 0.1 and y >= -0.1):
        y = 0
    post_frame_data.y_pos = round(y, 2)
    post_frame_data.facing_direction = hex_to_float(data[17:21])
    post_frame_data.percent = hex_to_float(data[21:25])
    post_frame_data.shield_size = hex_to_float(data[25:29])
    post_frame_data.last_attack_landed = hex_to_int([data[29]])
    post_frame_data.current_combo_count = hex_to_int([data[30]])
    post_frame_data.last_hit_by = hex_to_int([data[31]])
    post_frame_data.stocks_remaining = hex_to_int([data[32]])
