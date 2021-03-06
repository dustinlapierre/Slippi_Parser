from analytics import *
from commentary_statements import *
from structures import *
import LSTM
from queue import Queue

class randall_commentator:
    def __init__(self, commentary_queue):
        self.commentary_cooldown = 300
        self.LSTM_batch1 = []
        self.LSTM_batch2 = []
        self.lead_once = False
        self.commentary_queue = commentary_queue
    def main_commentary_update(self):
        self.commentary_cooldown -= 1
        update_analytics()

        if(self.commentary_cooldown <= 0):
            new_comment = self.get_commentary_statement()
            if(new_comment != None):
                print_to_gui(new_comment, self.commentary_queue)
        #Print support commentary if cooldown reaches -300 (5 seconds with nothing said)
        if(self.commentary_cooldown <= -300):
            print_to_gui(get_support_commentary(post_frame_data.frame_number), self.commentary_queue)
            self.commentary_cooldown = 60
        update_analytics_frame_buffer()

    def get_commentary_statement(self):
        #doesn't speak when on cooldown
        #gives people time to read or text to speach to talk
        normalized_data_player1 = LSTM.normalize(player1_data.as_LSTM_list())
        normalized_data_player2 = LSTM.normalize(player2_data.as_LSTM_list())

        #LSTM dash dance check
        if(len(self.LSTM_batch1) < 120):
            self.LSTM_batch1.append(normalized_data_player1)
        else:
            pred = LSTM.make_prediction(self.LSTM_batch1)
            del self.LSTM_batch1[:]
            if(pred >= 0.85):
                self.commentary_cooldown = 30
                return choose("Player 1 is trying to bait out a commit with that dash dance!",
                                    "Player 1 is dash dancing around trying to get player 2 to approach.")
        if(len(self.LSTM_batch2) < 120):
            self.LSTM_batch2.append(normalized_data_player2)
        else:
            pred = LSTM.make_prediction(self.LSTM_batch2)
            del self.LSTM_batch2[:]
            if(pred >= 0.85):
                self.commentary_cooldown = 30
                return choose("Player 2 is trying to bait out a commit with that dash dance!",
                                    "Player 2 is dash dancing around trying to get player 1 to approach.")

        #shield pressure check
        pressure = check_shield_pressure()
        if(pressure[0] == True):
            self.commentary_cooldown = 60
            return choose("Great shield pressure coming from Player 1\nPlayer 2's shield is looking like a Skittle.",
                                "Player 2 is under a lot of pressure, their shield might break!")
        elif(pressure[1] == True):
            self.commentary_cooldown = 60
            return choose("Great shield pressure coming from Player 2\nPlayer 2's shield is looking like a Skittle.",
                                "Player 2 is under a lot of pressure, their shield might break!")
        #character specific stuff
        character_com = character_specific_commentary()
        if(character_com != None):
            self.commentary_cooldown = 60
            return character_com
        #taunt check
        taunt_com = taunt_comment()
        if(taunt_com != None):
            self.commentary_cooldown = 120
            return taunt_com
        #taunt to get bodied commentary
        tauntb_com = taunt_bodied_check()
        if(tauntb_com != None):
            self.commentary_cooldown = 120
            return tauntb_com
        #recovery check
        recov_com = recovery_comment()
        if(recov_com != None):
            self.commentary_cooldown = 60
            return recov_com
        #huge lead check
        if(self.lead_once == False):
            lead_com = huge_lead_comment()
            if(lead_com != None):
                self.lead_once = True
                self.commentary_cooldown = 60
                return lead_com
        #comeback check
        elif(self.lead_once == True):
            comeback_com = comeback_comment()
            if(comeback_com != None):
                self.lead_once = False
                self.commentary_cooldown = 60
                return comeback_com
        return None

    def joke_commentary_update(self):
        if(self.commentary_cooldown <= 0):
            print_to_gui(choose_list(["Wait a second... this stage isn't even legal!",
                                    "I don't commentate for casuals.",
                                    "Don't forget to turn items on...",
                                    "Thank god 8 player smash wasn't a thing yet.",
                                    "I hear there's a pretty cool adventure mode in this.",
                                    "Oh great, there's nothing on TV either.",
                                    "I'm gonna grab a coffee real quick.",
                                    "Is it over yet?",
                                    "If I don't hear a shine in the next 5 minutes I might just lose it.",
                                    "At least the music is good!",
                                    "I went 0-2 in bracket for this!?",
                                    "Where's Vish, this is perfect for him.",
                                    "NICE BACKAIR! Or something like that.",
                                    "You should play Poke Floats next, I might try for that one."]), self.commentary_queue)
            self.commentary_cooldown = 500
        else:
            self.commentary_cooldown -= 1

    def print_intro(self):
        print_to_gui(("And the match begins!\n" +
        match.player1_character + " vs. " + match.player2_character + " on " + match.current_stage + "\n" +
        get_matchup_score(match.player1_character, match.player2_character)), self.commentary_queue)

    def show_results(self):
        if(game_end_data.game_end_method == 3):
            if(player1_data.stocks_remaining == 0):
                print_to_gui("Player 2 takes the game!", self.commentary_queue)
            else:
                print_to_gui("Player 1 takes the game!", self.commentary_queue)
        else:
            print_to_gui("No Contest!", self.commentary_queue)
        print_to_gui(print_final_stats(), self.commentary_queue)
