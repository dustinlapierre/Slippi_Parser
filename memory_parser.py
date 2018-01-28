import os
import win32file
import win32con
import time
from ast import literal_eval
import struct

import translator
import structures

#Windows filesystem watcher code written by Tim Golden
#Parser written by Dustin Lapierre

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}
# Thanks to Claudio Grondi for the correct set of numbers
FILE_LIST_DIRECTORY = 0x0001
clear = lambda: os.system('cls')

path_to_watch = "."
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)
full_filename = ""
while 1:
    #
    # ReadDirectoryChangesW takes a previously-created
    # handle to a directory, a buffer size for results,
    # a flag to indicate whether to watch subtrees and
    # a filter of what changes to notify.
    #
    # NB Tim Juchcinski reports that he needed to up
    # the buffer size to be sure of picking up all
    # events when a large number of files were
    # deleted at once.
    #
    results = win32file.ReadDirectoryChangesW (
        hDir,
        1024,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
         win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
         win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
         win32con.FILE_NOTIFY_CHANGE_SIZE |
         win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
         win32con.FILE_NOTIFY_CHANGE_SECURITY,
        None,
        None
      )

    #watch for file creations and updates within the current folder
    #when the Slippi file updates, read the changes
    #parse melee data from changes
    #update display with data from newest frame
    for action, file in results:
        full_filename = os.path.join (path_to_watch, file)
        #watch for file creation flag then save fd
        if(ACTIONS.get(action, "Unknown") == "Created"):
            break;
        else:
            full_filename = ""
    if(full_filename != ""):
        break;

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
    post_frame_data.x_pos = hex_to_float(data[9:13])
    post_frame_data.y_pos = hex_to_float(data[13:17])
    post_frame_data.facing_direction = hex_to_float(data[17:21])
    post_frame_data.percent = hex_to_float(data[21:25])
    post_frame_data.shield_size = hex_to_float(data[25:29])
    post_frame_data.last_attack_landed = hex_to_int([data[29]])
    post_frame_data.current_combo_count = hex_to_int([data[30]])
    post_frame_data.last_hit_by = hex_to_int([data[31]])
    post_frame_data.stocks_remaining = hex_to_int([data[32]])

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

def print_frame():
    print("Frame: ", post_frame_data.frame_number)
    print("Player: ", post_frame_data.player_index)
    print("Character: ", translator.internal_character_id[post_frame_data.internal_character_ID])
    if(post_frame_data.action_state in translator.action_state_id):
        print("Action: ", translator.action_state_id[post_frame_data.action_state])
    elif(post_frame_data.action_state > 324):
        if(translator.internal_character_id[post_frame_data.internal_character_ID] == "Fox"):
            if(post_frame_data.action_state in translator.fox_special_action_id):
                print("Action: ", translator.fox_special_action_id[post_frame_data.action_state])
        else:
            print("Action: ", post_frame_data.action_state)
    print("X: ", post_frame_data.x_pos)
    print("Y: ", post_frame_data.y_pos)
    print("Direction: ", post_frame_data.facing_direction)
    print("Percent: ", post_frame_data.percent)
    print("Shield Size: ", post_frame_data.shield_size)
    print("Combo: ", post_frame_data.current_combo_count)
    print("Stocks: ", post_frame_data.stocks_remaining)

#data holders
#variable values will be updated each time one of these
#commands are encountered in the replay file
game_start_data = structures.game_start_event()
pre_frame_data = structures.pre_frame_event()
post_frame_data = structures.post_frame_event()
game_end_data = structures.game_end_event()

#live parse the newly created file
with open(full_filename, "rb") as replay:
    #skip init routine
    replay.seek(30)
    #game start
    data = []
    while(len(data) < 320):
        position = replay.tell()
        byte = replay.read(1)
        if(not byte):
            time.sleep(1/120)
            replay.seek(position)
        else:
            data.append(hex(ord(byte)))

    parse_game_start(data)

    #frame update
    command = ""
    flag = 0
    players = 0
    frames = 0
    while(flag != 1):
        #read command byte
        while(1):
            position = replay.tell()
            byte = replay.read(1)
            if(not byte):
                time.sleep(1/120)
                replay.seek(position)
            else:
                command = hex(ord(byte))
                break;

        if(command == structures.PRE_FRAME_UPDATE):
            data = read_frame(replay, 58)
            parse_pre_frame(data)
        elif(command == structures.POST_FRAME_UPDATE):
            data = read_frame(replay, 33)
            parse_post_frame(data)
            if(players < 2):
                print_frame()
                players += 1
            frames += 1
        elif(command == structures.GAME_END):
            flag = 1

        if(frames > 29):
            players = 0
            frames = 0
            clear()
            print("Stage: ", translator.stage_index[game_start_data.stage])
            print()
    replay.close()
