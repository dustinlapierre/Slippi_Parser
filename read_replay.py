#Python Melee .slp parser
#Copyright Dustin Lapierre 12/24/2017

from ast import literal_eval
import struct

#TODO separate structures and parsers into different files

#command bytes
EVENT_PAYLOADS = "0x35"
GAME_START = "0x36"
PRE_FRAME_UPDATE = "0x37"
POST_FRAME_UPDATE = "0x38"
GAME_END = "0x39"

#event data holders
class game_start_event:
    command_byte = GAME_START
    version = [] #major.minor.build.revision
    game_info_block = [] #not sure what this is
    is_teams = 0
    stage = 0
    character_ID_port1 = 0
    character_ID_port2 = 0
    character_ID_port3 = 0
    character_ID_port4 = 0
    player_type_port1 = 0
    player_type_port2 = 0
    player_type_port3 = 0
    player_type_port4 = 0
    character_color_port1 = 0
    character_color_port2 = 0
    character_color_port3 = 0
    character_color_port4 = 0
    team_ID_port1 = 0
    team_ID_port2 = 0
    team_ID_port3 = 0
    team_ID_port4 = 0
    random_seed = 0

class pre_frame_event:
    command_byte = PRE_FRAME_UPDATE
    frame_number = 0
    player_index = 0 #port is this +1
    is_follower = 0
    random_seed = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 0.0
    joystick_x = 0.0
    joystick_y = 0.0
    c_stick_x = 0.0
    c_stick_y = 0.0
    trigger = 0.0
    buttons = 0
    physical_buttons = 0
    physical_l = 0.0
    physical_r = 0.0

class post_frame_event:
    command_byte = PRE_FRAME_UPDATE
    frame_number = 0
    player_index = 0
    is_follower = 0
    character_ID = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 0.0
    percent = 0.0
    shield_size = 0.0
    last_attack_landed = 0
    current_combo_count = 0
    last_hit_by = 0
    stocks_remaining = 0

class game_end_event:
    command_byte = GAME_END
    game_end_method = 0

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

#returns dictionary of all commnds and their given size
def parse_sizes(data):
    sizes = {}
    i = 2
    while(i < len(data)):
        sizes[data[i]] = hex_to_int(data[i+1:i+3])
        i += 3
    return sizes

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
    post_frame_data.character_ID = hex_to_int([data[6]])
    post_frame_data.action_state = hex_to_int(data[7:9])
    post_frame_data.x_pos = hex_to_float(data[9:13])
    post_frame_data.y_pos = hex_to_float(data[13:17])
    post_frame_data.facing_direction = hex_to_float(data[17:21])
    post_frame_data.percent = hex_to_float(data[21:25])
    post_frame_data.shield_size = hex_to_float(data[25:29])
    post_frame_data.last_attack_landed = hex_to_int([data[29]])
    post_frame_data.current_combo_count = hex_to_int([data[30]])
    post_frame_data.last_hit_by = hex_to_int([data[31]])
    post_frame_data.stocks_remaining = hex_to_int([data[32]])

#parser for game end event data
def parse_game_end(data):
    #parse all values
    game_end_data.game_end_method = hex_to_int([data[0]])

#parse the next command and call the proper handler
#returns 1 if successful, 0 on error
def parse_next(file, dict):
    #read command byte
    command = hex(ord(file.read(1)))
    data = []
    if(dict.get(command) != None):
        #parse command
        for i in range(0, dict[command]):
            byte = hex(ord(file.read(1)))
            data.append(byte)
    else:
        print("ERROR: Unknown command or EOF reached")
        return 0
    #call proper parser for the data
    if(command == GAME_START):
        parse_game_start(data)
    elif(command == PRE_FRAME_UPDATE):
        parse_pre_frame(data)
    elif(command == POST_FRAME_UPDATE):
        parse_post_frame(data)
    elif(command == GAME_END):
        parse_game_end(data)
    return 1

#data holders
#variable values will be updated each time one of these
#commands are encountered in the replay file
game_start_data = game_start_event()
pre_frame_data = pre_frame_event()
post_frame_data = post_frame_event()
game_end_data = game_end_event()

#main method
full_filename = "Game_20171221T170535.slp"
with open(full_filename, "rb") as replay:
    #raw element read
    print("RAW ELEMENT: ", replay.read(11))
    data = []
    for i in range(0, 4):
        byte = hex(ord(replay.read(1)))
        data.append(byte)
    print("RAW ELEMENT SIZE:", hex_to_int(data))
    #Event payload size
    data = []
    for i in range(0, 2):
        byte = hex(ord(replay.read(1)))
        data.append(byte)
    event_payloads_size = hex_to_int([data[1]]) - 1
    print("EVENT PAYLOADS SIZE: ", event_payloads_size)
    #commands and payload sizes
    for i in range(0, event_payloads_size):
        byte = hex(ord(replay.read(1)))
        data.append(byte)
    sizes = parse_sizes(data)
    print("COMMAND AND SIZE: ", sizes)
    while(parse_next(replay, sizes)):
        #do stuff with this frame's data
        pass
    #print data from the last frame
    attrs = vars(game_start_data)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    attrs = vars(pre_frame_data)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    attrs = vars(post_frame_data)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    attrs = vars(game_end_data)
    print(', '.join("%s: %s" % item for item in attrs.items()))
    replay.close()
