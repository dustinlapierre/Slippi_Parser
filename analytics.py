from math import *
from random import *
from enum import Enum
import translator
from structures import *
from general import *

#history of last three things said
commentary_history = []

#left ledge positions
#right ledge is (-x, y)
ledge_position = {
    "Fountain of Dreams": (-68, -9),
    "Pokemon Stadium": (-92, -10),
    "Yoshi's Story": (-61, -13),
    "Dreamland 64": (-82, -10),
    "Battlefield": (-73, -10),
    "Final Destination": (-90, -10)
}

#enum for all possible commentary statements
class CommentaryNumber(Enum):
    STAGE_CONTROL = 0
    BLOCK_SUCCESS = 1
    NEUTRAL_WINS = 2
    RECOVERY = 3
    PUNISH = 4
    OFFSTAGE = 5
    ABOVE = 6
    OPENINGS = 7

def update_analytics():
    #using data for this frame update all analytics
    check_stage_control()
    check_above()
    check_shielding()
    check_block()

    update_flags()
    check_neutral()
    check_recovery()
    on_death_check()

def update_analytics_frame_buffer():
    #update shield and percentage for next run
    player1_analytics.shield_health_last = player1_data.shield_size
    player1_analytics.percentage_last = player1_data.percent
    player1_analytics.recovery_success_last = player1_analytics.recovery_success
    player1_analytics.recovery_fail_last = player1_analytics.recovery_fail
    player2_analytics.shield_health_last = player2_data.shield_size
    player2_analytics.percentage_last = player2_data.percent
    player2_analytics.recovery_success_last = player2_analytics.recovery_success
    player2_analytics.recovery_fail_last = player2_analytics.recovery_fail

def character_specific_commentary():
    #shine spike
    if(match.player1_character == "Fox"):
        if(player2_analytics.percentage_last != player2_data.percent and player2_analytics.offstage_state == True):
            if(player1_data.action_state in translator.fox_special_action_id):
                if(player1_data.action_state in range(360, 369)):
                    return "Player 1 lands a shine spike, Player 2 is in a bad position"
    if(match.player2_character == "Fox"):
        if(player1_analytics.percentage_last != player1_data.percent and player1_analytics.offstage_state == True):
            if(player2_data.action_state in translator.fox_special_action_id):
                if(player2_data.action_state in range(360, 369)):
                    return "Player 2 lands a shine spike, Player 1 is in a bad position"
    #Rest
    if(match.player1_character == "Jigglypuff"):
        if(player2_analytics.percentage_last != player2_data.percent and player2_analytics.offstage_state == False and player2_data.percent != 0):
            if(player1_data.action_state in translator.puff_special_action_id):
                if(player1_data.action_state in range(369, 373)):
                    return "Player 1 connects a rest, Player 2 wants to die off the side so they can get a punish"
    if(match.player2_character == "Jigglypuff"):
        if(player1_analytics.percentage_last != player1_data.percent and player1_analytics.offstage_state == False and player1_data.percent != 0):
            if(player2_data.action_state in translator.puff_special_action_id):
                if(player2_data.action_state in range(369, 373)):
                    return "Player 2 connects a rest, Player 1 wants to die off the side so they can get a punish"
    #Falco/Marth Dair
    if(match.player1_character == "Falco" or match.player1_character == "Marth"):
        if(player2_analytics.percentage_last != player2_data.percent and player2_analytics.offstage_state == True):
            if(player1_data.action_state in translator.action_state_id):
                if(player1_data.action_state == 69):
                    return choose("Player 1 with an offstage dair, Player 2 is in a bad position",
                                    "That dair should close out this stock")
    if(match.player2_character == "Falco" or match.player2_character == "Marth"):
        if(player1_analytics.percentage_last != player1_data.percent and player1_analytics.offstage_state == True):
            if(player2_data.action_state in translator.action_state_id):
                if(player2_data.action_state == 69):
                    return choose("Player 2 with an offstage dair, Player 1 is in a bad position",
                                    "That dair should close out this stock")
    return None

def add_history(com_number):
    if(len(commentary_history) < 4):
        commentary_history.append(com_number)
    else:
        #pop the front off then append
        del commentary_history[0]
        commentary_history.append(com_number)

def select_commentary_by_weight(history):
    weights = []
    #weight stage control
    weight = abs(player1_analytics.stage_control - player2_analytics.stage_control)
    weight = flatten(weight, 0, 10000)
    if(CommentaryNumber.STAGE_CONTROL in history):
        weight = weight/(history.count(CommentaryNumber.STAGE_CONTROL)+1)
    weights.append(weight)
    #weight block success
    weight = abs(player1_analytics.block_success - player2_analytics.block_success)
    weight = flatten(weight, 0, 100)
    if(CommentaryNumber.BLOCK_SUCCESS in history):
        weight = weight/(history.count(CommentaryNumber.BLOCK_SUCCESS)+1)
    weights.append(weight)
    #weight neutral
    weight = abs(player1_analytics.punish_amount - player2_analytics.punish_amount)
    weight = flatten(weight, 0, 100)
    if(player1_analytics.punish_amount < 3 and player2_analytics.punish_amount < 3):
        weight = 0
    if(CommentaryNumber.NEUTRAL_WINS in history):
        weight = weight/(history.count(CommentaryNumber.NEUTRAL_WINS)+1)
    weights.append(weight)
    #weight recovery
    weight = abs(player1_analytics.recovery_success - player2_analytics.recovery_success)
    weight = flatten(weight, 0, 50)
    if(CommentaryNumber.RECOVERY in history):
        weight = weight/(history.count(CommentaryNumber.RECOVERY)+1)
    weights.append(weight)
    #weight punish
    if(player2_analytics.block_failed != 0 and player1_analytics.block_failed != 0):
        weight = abs((player1_analytics.punish_amount/player2_analytics.block_failed) - (player2_analytics.punish_amount/player1_analytics.block_failed))
        weight = flatten(weight, 0, 15)
    else:
        weight = 0
    if(CommentaryNumber.PUNISH in history):
        weight = weight/(history.count(CommentaryNumber.PUNISH)+1)
    weights.append(weight)
    #weight offstage
    weight = abs(player1_analytics.time_offstage - player2_analytics.time_offstage)
    weight = flatten(weight, 0, 10000)
    if(CommentaryNumber.OFFSTAGE in history):
        weight = weight/(history.count(CommentaryNumber.OFFSTAGE)+1)
    weights.append(weight)
    #weight above
    weight = abs(player1_analytics.above_opponent - player2_analytics.above_opponent)
    weight = flatten(weight, 0, 10000)
    if(CommentaryNumber.ABOVE in history):
        weight = weight/(history.count(CommentaryNumber.ABOVE)+1)
    weights.append(weight)
    #weight openings per kill
    if(player1_data.stocks_remaining != 4 and player2_data.stocks_remaining != 4):
        weight = abs((player1_analytics.punish_amount/(4 - player2_data.stocks_remaining)) - (player2_analytics.punish_amount/(4 - player1_data.stocks_remaining)))
        weight = flatten(weight, 0, 15)
    else:
        weight = 0
    if(CommentaryNumber.OPENINGS in history):
        weight = weight/(history.count(CommentaryNumber.OPENINGS)+1)
    weights.append(weight)

    return CommentaryNumber(weights.index(max(weights)))

def get_support_commentary(frame_number):
    choice = select_commentary_by_weight(commentary_history)
    if(choice == CommentaryNumber.STAGE_CONTROL):
        add_history(CommentaryNumber.STAGE_CONTROL)
        if(frame_number != 0):
            p1_stage = player1_analytics.stage_control/frame_number
            p2_stage = player2_analytics.stage_control/frame_number
        else:
            p1_stage = 0
            p2_stage = 0

        if(p1_stage > p2_stage):
            return choose("Player 1 has had stage control for a majority of the game.",
                            "Player 1 has been controlling the stage beautifully this game.")
        elif(p2_stage > p1_stage):
            return choose("Player 1 has had stage control for a majority of the game.",
                            "Player 1 has been controlling the stage beautifully this game.")
        else:
            return "Stage control has been hotly contested this match."

    elif(choice == CommentaryNumber.BLOCK_SUCCESS):
        add_history(CommentaryNumber.BLOCK_SUCCESS)
        if((player1_analytics.block_success + player1_analytics.block_failed) != 0):
            p1_block = player1_analytics.block_success/(player1_analytics.block_success + player1_analytics.block_failed)
        else:
            p1_block = 0
        if((player2_analytics.block_success + player2_analytics.block_failed) != 0):
            p2_block = player2_analytics.block_success/(player2_analytics.block_success + player2_analytics.block_failed)
        else:
            p2_block = 0

        if(p1_block < p2_block):
            return "Player 2 is finding a lot of holes in Player 1's defense.\nPlayer 1's block rate is " + str(p1_block * 100) + "%"
        elif(p1_block > p2_block):
            return "Player 1 is finding a lot of holes in Player 2's defense.\nPlayer 2's block rate is " + str(p2_block * 100) + "%"
        else:
            if(player1_data.stocks_remaining < player2_data.stocks_remaining):
                return choose("Player 2's strong offense is helping them hold the lead.",
                                "Player 1 is going to need to strengthen their defense if they want to catch up.")
            elif(player2_data.stocks_remaining < player1_data.stocks_remaining):
                return choose("Player 1's strong offense is helping them hold the lead.",
                                "Player 2 is going to need to strengthen their defense if they want to catch up.")
            else:
                return "I'm seeing really strong defense from both players."

    elif(choice == CommentaryNumber.NEUTRAL_WINS):
        add_history(CommentaryNumber.NEUTRAL_WINS)
        if((player1_analytics.punish_amount + player2_analytics.punish_amount) != 0):
            player1_nooch = (player1_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))
            player2_nooch = (player2_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))

            if(player1_nooch > 0.60):
                output = choose("Player 1 is really dominating in neutral",
                                "Player 1's neutral game is looking strong")
                if(player1_data.stocks_remaining < player2_data.stocks_remaining):
                    output += ", but Player 2 seems to be getting more off their neutral wins."
                return output
            elif(player2_nooch > 0.60):
                output = choose("Player 2 is really dominating in neutral",
                                "Player 2's neutral game is looking strong")
                if(player2_data.stocks_remaining < player1_data.stocks_remaining):
                    output += ", but Player 1 seems to be getting more off their neutral wins."
                return output
            else:
                output = choose("Both players are going about even in neutral so far",
                                "The neutral game from both players is looking strong")
                if(player1_data.stocks_remaining < player2_data.stocks_remaining):
                    output += ", but Player 2 is getting more off their neutral wins."
                elif(player2_data.stocks_remaining < player1_data.stocks_remaining):
                    output += ", but Player 1 is getting more off their neutral wins."
                return output
        else:
            return "Neither player has been able to score a single neutral win."

    elif(choice == CommentaryNumber.RECOVERY):
        add_history(CommentaryNumber.RECOVERY)
        if(player1_analytics.recovery_success > player2_analytics.recovery_success):
            if(player1_data.stocks_remaining >= player2_data.stocks_remaining):
                return choose("Player 1's recovery has been solid this game.",
                                "Player 2 is having a tough time edge guarding")
            if(player1_data.stocks_remaining < player2_data.stocks_remaining):
                return "Player 1's recovery has been good, but it just isn't enough to stay ahead."
        elif(player2_analytics.recovery_success > player1_analytics.recovery_success):
            if(player2_data.stocks_remaining >= player1_data.stocks_remaining):
                return choose("Player 2's recovery has been solid this game.",
                                "Player 1 is having a tough time edge guarding")
            if(player2_data.stocks_remaining < player1_data.stocks_remaining):
                return "Player 2's recovery has been good, but it just isn't enough to stay ahead."
        else:
            return "Both player's recovery is looking good."

    elif(choice == CommentaryNumber.PUNISH):
        add_history(CommentaryNumber.PUNISH)
        if(player1_analytics.block_failed != 0 and player2_analytics.block_failed != 0):
            p1_punish = (player2_analytics.block_failed/player1_analytics.punish_amount)
            p2_punish = (player1_analytics.block_failed/player2_analytics.punish_amount)
        else:
            p1_punish, p2_punish = 0, 0
        if(p1_punish > p2_punish):
            return choose("Player 1 has been getting a lot more off their openings.",
                            "Player 1's punish game is looking strong.")
        elif(p1_punish < p2_punish):
            return choose("Player 2 has been getting a lot more off their openings.",
                            "Player 2's punish game is looking strong.")
        else:
            return "The punish game from both players has been close to even."

    elif(choice == CommentaryNumber.OFFSTAGE):
        add_history(CommentaryNumber.OFFSTAGE)
        if(player1_analytics.time_offstage > player2_analytics.time_offstage):
            return choose("Player 2 isn't allowing Player 1 to get their footing on stage.",
                            "Player 1 is spending a lot of time offstage")
        elif(player2_analytics.time_offstage > player1_analytics.time_offstage):
            return choose("Player 1 isn't allowing Player 1 to get their footing on stage.",
                            "Player 2 is spending a lot of time offstage")
        else:
            return "Hard to say which player has spent more time offstage."

    elif(choice == CommentaryNumber.ABOVE):
        add_history(CommentaryNumber.ABOVE)
        if(player1_analytics.above_opponent > player2_analytics.above_opponent):
            if(player1_data.stocks_remaining < player2_data.stocks_remaining):
                return choose("Player 2 has been doing well juggling Player 1 in the air.",
                                "Player 2 just won't let player 1 stay grounded.")
            elif(player1_data.stocks_remaining >= player2_data.stocks_remaining):
                return "Player 1 has been playing the vertical advantage and attacking from above."
        elif(player2_analytics.above_opponent > player1_analytics.above_opponent):
            if(player2_data.stocks_remaining < player1_data.stocks_remaining):
                return choose("Player 1 has been doing well juggling Player 1 in the air.",
                                "Player 1 just won't let player 2 stay grounded.")
            elif(player2_data.stocks_remaining >= player1_data.stocks_remaining):
                return "Player 2 has been playing the vertical advantage and attacking from above."
        else:
            return "The players are staying grounded."

    elif(choice == CommentaryNumber.OPENINGS):
        add_history(CommentaryNumber.OPENINGS)
        if(player1_data.stocks_remaining != 4 and player2_data.stocks_remaining != 4):
            p1_openings = (player1_analytics.punish_amount/(4 - player2_data.stocks_remaining))
            p2_openings = (player2_analytics.punish_amount/(4 - player1_data.stocks_remaining))
        else:
            p1_openings, p2_openings = 0, 0
        if(p1_openings > p2_openings):
            return choose("Player 1 has been extremely efficient with their punishes.",
                            ("Player 1 is averaging " + str(p1_openings) + " openings per kill!"))
        elif(p1_openings < p2_openings):
            return choose("Player 2 has been extremely efficient with their punishes.",
                            ("Player 2 is averaging " + str(p2_openings) + " openings per kill!"))
        else:
            return "Both players have been pretty efficient with their kills."

def check_stage_control():
    #stage control - when you are inside middle 100 pixels and opponent outside it
    if(abs(player1_data.x_pos) <= 50 and abs(player2_data.x_pos) > 50):
        player1_analytics.stage_control += 1
    elif(abs(player2_data.x_pos) <= 50 and abs(player1_data.x_pos) > 50):
        player2_analytics.stage_control += 1

def check_above():
    #if player is above the other
    if(player1_data.y_pos > player2_data.y_pos):
        player1_analytics.above_opponent += 1
    elif(player2_data.y_pos > player1_data.y_pos):
        player2_analytics.above_opponent += 1

def check_shielding():
    #if player is shielding
    if(player1_data.action_state == 179):
        player1_analytics.time_shielded += 1
    if(player2_data.action_state == 179):
        player2_analytics.time_shielded += 1

def check_block():
    #if you took abnormal shield damage you blocked an attack
    #the plus 1.5 accounts for natural shield degeneration
    if((player1_data.shield_size + 1.5) < player1_analytics.shield_health_last):
        player1_analytics.block_success += 1
    elif((player2_data.shield_size + 1.5) < player2_analytics.shield_health_last):
        player2_analytics.block_success += 1
    #if you gained percent you didn't
    if(player1_data.percent > player1_analytics.percentage_last):
        player1_analytics.block_failed += 1
    if(player2_data.percent > player2_analytics.percentage_last):
        player2_analytics.block_failed += 1

def update_flags():
    #punish check - took damage and wasn't in a punish
    if(player1_data.percent > player1_analytics.percentage_last):
        if(player1_analytics.punish_state == False):
            player2_analytics.punish_amount += 1
        player1_analytics.punish_state = True
        player1_analytics.punish_time = 0
    if(player2_data.percent > player2_analytics.percentage_last):
        if(player2_analytics.punish_state == False):
            player1_analytics.punish_amount += 1
        player2_analytics.punish_state = True
        player2_analytics.punish_time = 0

    #damaged check
    if(player1_data.action_state in range(75, 92)):
        player1_analytics.damaged_state = True
    else:
        player1_analytics.damaged_state = False

    if(player2_data.action_state in range(75, 92)):
        player2_analytics.damaged_state = True
    else:
        player2_analytics.damaged_state = False

    #offstage check
    edge = ledge_position[match.current_stage]
    if(((abs(player1_data.x_pos) > abs(edge[0])) or (player1_data.y_pos < (edge[1] - 10)))):
        player1_analytics.offstage_state = True
        player1_analytics.time_offstage += 1
    else:
        player1_analytics.offstage_state = False
        player1_analytics.knocked_offstage = False

    if(((abs(player2_data.x_pos) > abs(edge[0])) or (player2_data.y_pos < (edge[1] - 10)))):
        player2_analytics.offstage_state = True
        player2_analytics.time_offstage += 1
    else:
        player2_analytics.offstage_state = False
        player2_analytics.knocked_offstage = False

    #knocked offstage
    if(player1_analytics.offstage_state == True and player1_analytics.damaged_state == True):
        player1_analytics.knocked_offstage = True
    if(player2_analytics.offstage_state == True and player2_analytics.damaged_state == True):
        player2_analytics.knocked_offstage = True

    #taunt to get bodied timer
    if(player1_analytics.taunt_timer > 0):
        player1_analytics.taunt_timer -= 1
    if(player2_analytics.taunt_timer > 0):
        player2_analytics.taunt_timer -= 1

def check_recovery():
    #recovery check
    if(player1_analytics.knocked_offstage == True and player1_analytics.damaged_state == False):
        if(player1_data.action_state not in range(0, 13)):
            player1_analytics.recovery_state = True
    if(player2_analytics.knocked_offstage == True and player2_analytics.damaged_state == False):
        if(player2_data.action_state not in range(0, 13)):
            player2_analytics.recovery_state = True

def on_death_check():
    edge = ledge_position[match.current_stage]
    if(player1_data.action_state in range(0, 13) and player1_analytics.recovery_state == True):
        player1_analytics.recovery_state = False
        player1_analytics.punish_state = False
        player1_analytics.damaged_state = False
        player1_analytics.offstage_state = False
        player1_analytics.punish_time = 0
        player1_analytics.recovery_fail += 1
    if(not (abs(player1_data.x_pos) > abs(edge[0]+10)) and (player1_data.y_pos > (edge[1] - 10))):
        if(player1_analytics.recovery_state == True):
            player1_analytics.recovery_state = False
            player1_analytics.recovery_success += 1
    if(player2_data.action_state in range(0, 13) and player2_analytics.recovery_state == True):
        player2_analytics.recovery_state = False
        player2_analytics.punish_state = False
        player2_analytics.damaged_state = False
        player2_analytics.offstage_state = False
        player2_analytics.punish_time = 0
        player2_analytics.recovery_fail += 1
    if(not (abs(player2_data.x_pos) > abs(edge[0]+10)) and (player2_data.y_pos > (edge[1] - 10))):
        if(player2_analytics.recovery_state == True):
            player2_analytics.recovery_state = False
            player2_analytics.recovery_success += 1

def taunt_bodied_check():
    if(player1_data.action_state in range(0, 13) and player1_analytics.taunt_timer > 0):
        return "Player 1 with the taunt to get bodied true combo!"
    elif(player2_data.action_state in range(0, 13) and player2_analytics.taunt_timer > 0):
        return "Player 2 with the taunt to get bodied true combo!"
    return None

def huge_lead_comment():
    if(abs(player1_data.stocks_remaining - player2_data.stocks_remaining) >= 2):
        if(player1_data.stocks_remaining > player2_data.stocks_remaining):
            return "Player 2 is getting bodied pretty hard."
        else:
            return "Player 1 is getting bodied pretty hard."
    return None

def comeback_comment():
    if(player1_data.stocks_remaining == player2_data.stocks_remaining):
        return "What an incredible comeback!"
    return None

def get_matchup_score(player1_character, player2_character):
    #this will eventually return a string discussing the matchup from player 1's perspective
    if(player1_character in translator.matchup_guide and player2_character in translator.matchup_guide):
        match_score = translator.matchup_guide[player1_character][player2_character]
        result_string = "This matchup is "
        if(match_score == 0):
            result_string += "fairly even."
        elif(match_score == 1):
            result_string += ("pretty good for " + player1_character + ".")
        elif(match_score == 2):
            result_string += ("really good for " + player1_character + ".")
        elif(match_score == -1):
            result_string += ("pretty bad for " + player1_character + ".")
        elif(match_score == -2):
            result_string += ("extremely bad for " + player1_character + ".")
        return result_string
    else:
        return "This is a matchup we don't see often!"

def check_shield_pressure():
    #returns boolean tuple, (player1, player2)
    #True means player is currently pressuring shield
    #players are close
    distance = sqrt(pow((player2_data.x_pos - player1_data.x_pos), 2) + pow((player2_data.x_pos - player1_data.x_pos), 2))
    if(distance < 15):
        #player 1 under pressure
        if(player1_data.shield_size <= 25.0 and player1_data.action_state == 179):
            return (False, True)
        #player 2 under pressure
        elif(player2_data.shield_size <= 25.0 and player2_data.action_state == 179):
            return (True, False)

    return (False, False)

def check_neutral():
    #check_neutral - (# punishes by this player/# of punishes total)
        #punish - starts when player takes damage, ends when player is on stage and doesnt take damage for 80 frames (1.3 second)
    #punish time increment
    if(player1_analytics.damaged_state == False and player1_analytics.offstage_state == False and player1_analytics.punish_state == True):
        player1_analytics.punish_time += 1
    if(player2_analytics.damaged_state == False and player2_analytics.offstage_state == False and player2_analytics.punish_state == True):
        player2_analytics.punish_time += 1

    #punish ended check
    if(player1_analytics.punish_time >= 80):
        player1_analytics.punish_state = False
        player1_analytics.punish_time = 0
    if(player2_analytics.punish_time >= 80):
        player2_analytics.punish_state = False
        player2_analytics.punish_time = 0
