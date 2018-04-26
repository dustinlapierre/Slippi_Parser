import threading
from queue import Queue
import time

import translator
from structures import *
from general import *
from randall import *
from file_detection import watch_for_create

import sys
sys.path.insert(0, 'GUI/')
from gui import GuiThreadStart

#Written by Dustin Lapierre copyright 04/18/2018

#shared mem and data holders
full_filename = watch_for_create("../")
connection = Queue()
commentary_queue = Queue()
randall = randall_commentator(commentary_queue)

#live parse the newly created file
with open(full_filename, "rb") as replay:
    #skip init routine
    replay.seek(30)
    #game start
    data = read_frame(replay, 320)
    game_start_data.parse_game_start(data)

    match.set_match_context(translator.external_character_id[game_start_data.character_ID_port1],
    translator.external_character_id[game_start_data.character_ID_port2],
    translator.stage_index[game_start_data.stage])

    #GUI threading
    Gui_thread = threading.Thread(target=GuiThreadStart, args=
    (match.player1_character,
    match.player2_character,
    match.current_stage, connection, commentary_queue))
    Gui_thread.daemon = True
    Gui_thread.start()

    #intro and matchup statement
    randall.print_intro()

    #frame update
    command = ""
    flag = 0
    stocks = [0,0]
    while(flag != 1):
        #get command byte
        command = read_frame(replay, 1)[0]

        #parse command
        if(command == PRE_FRAME_UPDATE):
            data = read_frame(replay, 58)
            pre_frame_data.parse_pre_frame(data)
        elif(command == POST_FRAME_UPDATE):
            data = read_frame(replay, 33)
            post_frame_data.parse_post_frame(data)

            #copy data into player container
            if(post_frame_data.player_index == 0):
                player1_data.update_player_data()
            else:
                player2_data.update_player_data()

            #if both player's data stored, send frame to LSTM
            if(post_frame_data.player_index == 1):
                #update stocks if a change has occured
                if(connection.empty() and stocks != [player1_data.stocks_remaining, player2_data.stocks_remaining]):
                    stocks = [player1_data.stocks_remaining, player2_data.stocks_remaining]
                    connection.put([player1_data.stocks_remaining, player2_data.stocks_remaining])
                    connection.join()
                if(match.current_stage in translator.legal_stages):
                    randall.main_commentary_update()
                else:
                    randall.joke_commentary_update()
        elif(command == GAME_END):
            data = read_frame(replay, 1)
            game_end_data.game_end_method = hex_to_int([data[0]])
            #print final results and give time to read before close
            randall.show_results()
            time.sleep(8)
            flag = 1

    replay.close()
