import os
import win32file
import win32con
import threading
from queue import Queue
import time
from ast import literal_eval
import struct

import LSTM
import translator
import structures
from analytics import *

import sys
sys.path.insert(0, 'GUI/')
from gui import GuiThreadStart

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

def post_frame_as_list():
    data = []
    data.append(post_frame_data.player_index)
    data.append(post_frame_data.action_state)
    data.append(post_frame_data.x_pos)
    data.append(post_frame_data.y_pos)
    data.append(post_frame_data.facing_direction)
    data.append(post_frame_data.percent)
    data.append(post_frame_data.shield_size)
    data.append(post_frame_data.stocks_remaining)
    return data

def LSTM_update(data_list):
    global commentary_cooldown
    commentary_cooldown -= 1
    #data_list: [stage, frame num, (player index, action, x, y, direction, percent, shield, stocks) x 2]
    update_analytics(player1_analytics, player2_analytics, data_list)

    #doesn't speak when on cooldown
    #gives people time to read or text to speach to talk
    if(commentary_cooldown <= 0):
        normalized_data_player1 = LSTM.normalize(data_list[3:7])
        normalized_data_player2 = LSTM.normalize(data_list[11:15])

        #LSTM dash dance check
        if(len(LSTM_batch1) < 120):
            LSTM_batch1.append(normalized_data_player1)
        else:
            pred = LSTM.make_prediction(LSTM_batch1)
            del LSTM_batch1[:]
            if(pred >= 0.85):
                print("Player 1 is trying to bait out a commit with that dash dance!")
                commentary_cooldown = 30
        if(len(LSTM_batch2) < 120):
            LSTM_batch2.append(normalized_data_player2)
        else:
            pred = LSTM.make_prediction(LSTM_batch2)
            del LSTM_batch2[:]
            if(pred >= 0.85):
                print("Player 2 is trying to bait out a commit with that dash dance!")
                commentary_cooldown = 30

        #shield pressure check
        if(commentary_cooldown <= 0):
            pressure = check_shield_pressure(data_list)
            if(pressure[0] == True):
                print("Great shield pressure coming from Player 1\nPlayer 2's shield is looking like a Skittle.")
                commentary_cooldown = 60
            elif(pressure[1] == True):
                print("Great shield pressure coming from Player 2\nPlayer 2's shield is looking like a Skittle.")
                commentary_cooldown = 60

        #character specific stuff
        if(commentary_cooldown <= 0):
            character_com = character_specific_commentary(player1_character, player2_character, player1_analytics, player2_analytics, data_list)
            if(character_com != "none"):
                print(character_com)
                commentary_cooldown = 60

        #taunt check
        if(commentary_cooldown <= 0):
            if(data_list[3] in range(264, 266)):
                print("Player 1 feeling themselves with that taunt.")
                player1_analytics.taunt_timer = 600
                commentary_cooldown = 120
            elif(data_list[11] in range(264, 266)):
                print("Player 2 feeling themselves with that taunt.")
                player2_analytics.taunt_timer = 600
                commentary_cooldown = 120

        #taunt to get bodied commentary
        if(commentary_cooldown <= 0):
            taunt_com = taunt_bodied_check(player1_analytics, player2_analytics, data_list)
            if(taunt_com != "none"):
                print(taunt_com)
                commentary_cooldown = 120

        #recovery commentary
        if(commentary_cooldown <= 0):
            if(player1_analytics.recovery_success != player1_analytics.recovery_success_last):
                print("Good recovery from Player 1.")
                commentary_cooldown = 60
            elif(player1_analytics.recovery_fail != player1_analytics.recovery_fail_last):
                print("Good edge guard from Player 2.")
                commentary_cooldown = 60
            if(player2_analytics.recovery_success != player2_analytics.recovery_success_last):
                print("Good recovery from Player 2.")
                commentary_cooldown = 60
            elif(player2_analytics.recovery_fail != player2_analytics.recovery_fail_last):
                print("Good edge guard from Player 1.")
                commentary_cooldown = 60

        #Print support commentary if cooldown reaches -300 (5 seconds with nothing said)
        if(commentary_cooldown <= -300):
            print(get_support_commentary(player1_analytics, player2_analytics, data_list))
            commentary_cooldown = 60

    update_analytics_frame_buffer(player1_analytics, player2_analytics, data_list)

def print_final_stats():
    print("Player 1 Stats ----------")
    print("Frames in stage control:", player1_analytics.stage_control)
    print("Frames above opponent:", player1_analytics.above_opponent)
    print("Frames offstage:", player1_analytics.time_offstage)
    print("Frames shielding:", player1_analytics.time_shielded)
    print("Successful blocks:", player1_analytics.block_success)
    print("Times hit:", player1_analytics.block_failed)
    print("Punishes:", player1_analytics.punish_amount)
    if(player2_analytics.block_failed != 0):
        print("Hits per punish:", (player2_analytics.block_failed/player1_analytics.punish_amount))
    if(player1_analytics.recovery_success != 0):
        print("Recovery %:", (player1_analytics.recovery_success/(player1_analytics.recovery_success+player1_analytics.recovery_fail))*100)
    if((player1_analytics.punish_amount + player2_analytics.punish_amount) != 0):
        print("Neutral Win %:", (player1_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))*100)
    if(player2_data[7] != 4):
        print("Openings Per Kill:", (player1_analytics.punish_amount/(4 - player2_data[7])))

    print("Player 2 Stats ----------")
    print("Frames in stage control:", player2_analytics.stage_control)
    print("Frames above opponent:", player2_analytics.above_opponent)
    print("Frames offstage:", player2_analytics.time_offstage)
    print("Frames shielding:", player2_analytics.time_shielded)
    print("Successful blocks:", player2_analytics.block_success)
    print("Times hit:", player2_analytics.block_failed)
    print("Punishes:", player2_analytics.punish_amount)
    if(player1_analytics.block_failed != 0):
        print("Hits per punish:", (player1_analytics.block_failed/player2_analytics.punish_amount))
    if(player2_analytics.recovery_success != 0):
        print("Recovery %:", (player2_analytics.recovery_success/(player2_analytics.recovery_success+player2_analytics.recovery_fail))*100)
    if((player1_analytics.punish_amount + player2_analytics.punish_amount) != 0):
        print("Neutral Win %:", (player2_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))*100)
    if(player1_data[7] != 4):
        print("Openings Per Kill:", (player2_analytics.punish_amount/(4 - player1_data[7])))

def print_to_gui(text):
    if(commentary_queue.empty()):
        commentary_queue.put(text)
        connection.join()

#data holders
#variable values will be updated each time one of these
#commands are encountered in the replay file
game_start_data = structures.game_start_event()
pre_frame_data = structures.pre_frame_event()
post_frame_data = structures.post_frame_event()
game_end_data = structures.game_end_event()
player1_analytics = player_analytics()
player2_analytics = player_analytics()
player1_character = ""
player2_character = ""
player1_data = []
player2_data = []
LSTM_batch1 = []
LSTM_batch2 = []
commentary_cooldown = 120

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
    player1_character = translator.external_character_id[game_start_data.character_ID_port1]
    player2_character = translator.external_character_id[game_start_data.character_ID_port2]

    #threading
    connection = Queue()
    commentary_queue = Queue()
    Gui_thread = threading.Thread(target=GuiThreadStart, args=
    (player1_character,
    player2_character,
    translator.stage_index[game_start_data.stage], connection, commentary_queue))
    Gui_thread.daemon = True
    Gui_thread.start()

    #intro context
    print("And the match begins!")
    print(player1_character, "vs.", player2_character, "on", translator.stage_index[game_start_data.stage])
    print(get_matchup_score(player1_character, player2_character))
    print_to_gui(get_matchup_score(player1_character, player2_character))

    #frame update
    command = ""
    flag = 0
    stocks = [0,0]
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

        #parse command
        if(command == structures.PRE_FRAME_UPDATE):
            data = read_frame(replay, 58)
            parse_pre_frame(data)
        elif(command == structures.POST_FRAME_UPDATE):
            data = read_frame(replay, 33)
            parse_post_frame(data)
            #copy data into player container
            if(post_frame_data.player_index == 0):
                player1_data = post_frame_as_list()
            else:
                player2_data = post_frame_as_list()
            #if both player's data stored, send frame to LSTM
            if(post_frame_data.player_index == 1):
                if(connection.empty() and stocks != [player1_data[7], player2_data[7]]):
                    stocks = [player1_data[7], player2_data[7]]
                    connection.put([player1_data[7], player2_data[7]])
                    connection.join()
                LSTM_update([game_start_data.stage] + [post_frame_data.frame_number] + player1_data + player2_data)
        elif(command == structures.GAME_END):
            data = read_frame(replay, 1)
            game_end_data.game_end_method = hex_to_int([data[0]])
            if(game_end_data.game_end_method == 3):
                if(player1_data[7] == 0):
                    print("Player 2 takes the game!")
                else:
                    print("Player 1 takes the game!")
            else:
                print("No Contest!")
            print_final_stats()
            flag = 1

    replay.close()
