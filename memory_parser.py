import threading
from queue import Queue
import time

import LSTM
import translator
from structures import *
from analytics import *
from commentary_statements import *
from parse_functions import *
from file_detection import watch_for_create

import sys
sys.path.insert(0, 'GUI/')
from gui import GuiThreadStart

#Written by Dustin Lapierre copyright 04/18/2018

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

def update_player_data(player_data):
    player_data.player_index = post_frame_data.player_index
    player_data.action_state = post_frame_data.action_state
    player_data.x_pos = post_frame_data.x_pos
    player_data.y_pos = post_frame_data.y_pos
    player_data.facing_direction = post_frame_data.facing_direction
    player_data.percent = post_frame_data.percent
    player_data.shield_size = post_frame_data.shield_size
    player_data.stocks_remaining = post_frame_data.stocks_remaining


def LSTM_update(data_list):
    global commentary_cooldown
    commentary_cooldown -= 1
    #data_list: [stage, frame num, (player index, action, x, y, direction, percent, shield, stocks) x 2]
    update_analytics()

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
            pressure = check_shield_pressure()
            if(pressure[0] == True):
                print("Great shield pressure coming from Player 1\nPlayer 2's shield is looking like a Skittle.")
                commentary_cooldown = 60
            elif(pressure[1] == True):
                print("Great shield pressure coming from Player 2\nPlayer 2's shield is looking like a Skittle.")
                commentary_cooldown = 60
        #character specific stuff
        if(commentary_cooldown <= 0):
            character_com = character_specific_commentary()
            if(character_com != None):
                print(character_com)
                commentary_cooldown = 60
        #taunt check
        if(commentary_cooldown <= 0):
            taunt_com = taunt_comment()
            if(taunt_com != None):
                print(taunt_com)
                commentary_cooldown = 120
        #taunt to get bodied commentary
        if(commentary_cooldown <= 0):
            tauntb_com = taunt_bodied_check()
            if(tauntb_com != None):
                print(tauntb_com)
                commentary_cooldown = 120
        #recovery check
        if(commentary_cooldown <= 0):
            recov_com = recovery_comment()
            if(recov_com != None):
                print(recov_com)
                commentary_cooldown = 60
        #Print support commentary if cooldown reaches -300 (5 seconds with nothing said)
        if(commentary_cooldown <= -300):
            print(get_support_commentary(data_list[1]))
            commentary_cooldown = 60

    update_analytics_frame_buffer()

def print_to_gui(text):
    if(commentary_queue.empty()):
        commentary_queue.put(text)
        connection.join()

#shared mem and data holders
full_filename = watch_for_create(".")
LSTM_batch1 = []
LSTM_batch2 = []
commentary_cooldown = 120
connection = Queue()
commentary_queue = Queue()

#live parse the newly created file
with open(full_filename, "rb") as replay:
    #skip init routine
    replay.seek(30)
    #game start
    data = read_frame(replay, 320)
    parse_game_start(data)

    match.player1_character = translator.external_character_id[game_start_data.character_ID_port1]
    match.player2_character = translator.external_character_id[game_start_data.character_ID_port2]
    match.current_stage = translator.stage_index[game_start_data.stage]

    #GUI threading
    Gui_thread = threading.Thread(target=GuiThreadStart, args=
    (match.player1_character,
    match.player2_character,
    match.current_stage, connection, commentary_queue))
    Gui_thread.daemon = True
    Gui_thread.start()

    #intro context
    print("And the match begins!")
    print(match.player1_character, "vs.", match.player2_character, "on", match.current_stage)
    print(get_matchup_score(match.player1_character, match.player2_character))
    print_to_gui(get_matchup_score(match.player1_character, match.player2_character))

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
        if(command == PRE_FRAME_UPDATE):
            data = read_frame(replay, 58)
            parse_pre_frame(data)
        elif(command == POST_FRAME_UPDATE):
            data = read_frame(replay, 33)
            parse_post_frame(data)
            #copy data into player container
            if(post_frame_data.player_index == 0):
                player1_data_dep = post_frame_as_list()
                update_player_data(player1_data)
            else:
                player2_data_dep = post_frame_as_list()
                update_player_data(player2_data)
            #if both player's data stored, send frame to LSTM
            if(post_frame_data.player_index == 1):
                if(connection.empty() and stocks != [player1_data.stocks_remaining, player2_data.stocks_remaining]):
                    stocks = [player1_data.stocks_remaining, player2_data.stocks_remaining]
                    connection.put([player1_data.stocks_remaining, player2_data.stocks_remaining])
                    connection.join()
                LSTM_update([game_start_data.stage] + [post_frame_data.frame_number] + player1_data_dep + player2_data_dep)
        elif(command == GAME_END):
            data = read_frame(replay, 1)
            game_end_data.game_end_method = hex_to_int([data[0]])
            if(game_end_data.game_end_method == 3):
                if(player1_data.stocks_remaining == 0):
                    print("Player 2 takes the game!")
                else:
                    print("Player 1 takes the game!")
            else:
                print("No Contest!")
            print_final_stats()
            flag = 1

    replay.close()
