from translator import stage_index
from math import *
from random import *
from enum import Enum

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

class player_analytics:
    #shield health last frame (for detecting blocks)
    shield_health_last = -1.0
    #percentage last frame (for detecting hits)
    percentage_last = 0.0
    #number of frames in stage control
    stage_control = 0
    #number of frames above opponent
    above_opponent = 0
    #number of frames spent in shield
    time_shielded = 0
    #number of sucessful/failed recoveries
    recovery_success = 0
    recovery_fail = 0
    #number of sucessful/failed edge guards
    edge_success = 0
    edge_fail = 0
    #number of sucessful/failed blocks
    block_success = 0
    block_failed = 0
    #number of punishes this player gets
    punish_amount = 0
    punish_time = 0
    #flags
    punish_state = False
    damaged_state = False
    offstage_state = False
    recovery_state = False

def update_analytics(player1, player2, data):
    #stage, frame num, (player index, action, x, y, direction, percent, shield, stocks) x 2
    check_stage_control(player1, player2, data)
    check_above(player1, player2, data)
    check_shielding(player1, player2, data)
    check_block(player1, player2, data)

    update_flags(player1, player2, data)
    check_neutral(player1, player2, data)
    check_recovery(player1, player2)
    on_death_check(player1, player2, data)

    #TODO add average hits per punish filler commentary (player times hit/opponents punishes)

    #recovery_analysis : more complex than other stats but doable
        #When player in damaged state off stage then offstage begins
        #if damaged state is gone during offstage (player didn't die from hit) then recovery/edge guard begins
            #ON DEATH
            #if offstage = true and recovery = false: initial hit killed player
                #reset all flags
            #if offstage and recovery = True
                #recovery failed, edge guard success, reset flags
        #If player reaches stage, reset flags


    #update shield and percentage for next run
    player1.shield_health_last = data[8]
    player1.percentage_last = data[7]
    player2.shield_health_last = data[16]
    player2.percentage_last = data[15]

def flatten(x, min, max):
    return ((x-min) / (max-min))

def select_commentary_by_weight(player1, player2, history):
    weights = []
    #weight stage control
    weight = abs(player1.stage_control - player2.stage_control)
    weight = flatten(weight, 0, 14400)
    if(CommentaryNumber.STAGE_CONTROL in history):
        weight = weight/2
    weights.append(weight)
    #weight block success
    weight = abs(player1.block_success - player2.block_success)
    weight = flatten(weight, 0, 100)
    if(CommentaryNumber.BLOCK_SUCCESS in history):
        weight = weight/2
    weights.append(weight)
    #weight neutral
    weight = abs(player1.punish_amount - player2.punish_amount)
    weight = flatten(weight, 0, 100)
    if(CommentaryNumber.NEUTRAL_WINS in history):
        weight = weight/2
    weights.append(weight)
    #weight recovery
    weight = abs(player1.recovery_success - player2.recovery_success)
    weight = flatten(weight, 0, 50)
    if(CommentaryNumber.RECOVERY in history):
        weight = weight/2
    weights.append(weight)

    return CommentaryNumber(weights.index(max(weights)))

def get_support_commentary(player1, player2, data):
    choice = select_commentary_by_weight(player1, player2, [])
    if(choice == CommentaryNumber.STAGE_CONTROL):
        #stage control comment
        if(data[1] != 0):
            p1_stage = player1.stage_control/data[1]
            p2_stage = player2.stage_control/data[1]
        else:
            p1_stage = 0
            p2_stage = 0

        if(p1_stage > p2_stage):
            return "Player 1 has had stage control for a majority of the game"
        elif(p2_stage > p1_stage):
            return "Player 2 has had stage control for a majority of the game"
        else:
            return "Stage control has been hotly contested this match"

    elif(choice == CommentaryNumber.BLOCK_SUCCESS):
        #talk about leading player and their block success
        if((player1.block_success + player1.block_failed) != 0):
            p1_block = player1.block_success/(player1.block_success + player1.block_failed)
        else:
            p1_block = 0
        if((player2.block_success + player2.block_failed) != 0):
            p2_block = player2.block_success/(player2.block_success + player2.block_failed)
        else:
            p2_block = 0

        if(p1_block < p2_block):
            return "Player 2 is finding a lot of holes in Player 1's defense.\nPlayer 1's block rate is " + str(p1_block * 100) + "%"
        elif(p1_block > p2_block):
            return "Player 1 is finding a lot of holes in Player 2's defense.\nPlayer 2's block rate is " + str(p2_block * 100) + "%"
        else:
            if(data[9] < data[17]):
                return "Player 2's strong offense is helping them hold the lead"
            elif(data[17] < data[9]):
                return "Player 1's strong offense is helping them hold the lead"
            else:
                return "I'm seeing really strong defense from both players"


    elif(choice == CommentaryNumber.NEUTRAL_WINS):
        #neutral comment
        if((player1.punish_amount + player2.punish_amount) != 0):
            player1_nooch = (player1.punish_amount/(player1.punish_amount + player2.punish_amount))
            player2_nooch = (player2.punish_amount/(player1.punish_amount + player2.punish_amount))

            if(player1_nooch > 0.60):
                output = "Player 1 is really dominating in neutral"
                if(data[9] < data[17]):
                    output += ", but Player 2 seems to be getting more off their neutral wins"
                return output
            elif(player2_nooch > 0.60):
                output = "Player 2 is really dominating in neutral"
                if(data[17] < data[9]):
                    output += ", but Player 1 seems to be getting more off their neutral wins"
                return output
            else:
                output = "Both players are going about even in neutral so far"
                if(data[9] < data[17]):
                    output += ", but Player 2 is getting more off their neutral wins"
                elif(data[17] < data[9]):
                    output += ", but Player 1 is getting more off their neutral wins"
                return output
        else:
            return "Neither player has been able to score a single neutral win"
    elif(choice == CommentaryNumber.RECOVERY):
        return "Recovery"
    #TODO check each one for weight, if the stats are interesting put those strings in a list
    #then randomly choose from the list
    #TODO add recovery comment

def check_stage_control(player1, player2, data):
    #stage control - when you are inside middle 100 pixels and opponent outside it
    if(abs(data[4]) <= 50 and abs(data[12]) > 50):
        player1.stage_control += 1
    elif(abs(data[12]) <= 50 and abs(data[4]) > 50):
        player2.stage_control += 1

def check_above(player1, player2, data):
    #if player is above the other
    if(data[5] > data[13]):
        player1.above_opponent += 1
    elif(data[13] > data[5]):
        player2.above_opponent += 1

def check_shielding(player1, player2, data):
    #if player is shielding
    if(data[3] == 179):
        player1.time_shielded += 1
    if(data[11] == 179):
        player2.time_shielded += 1

def check_block(player1, player2, data):
    #if you took abnormal shield damage you blocked an attack
    #the plus 1.5 accounts for natural shield degeneration
    if((data[8] + 1.5) < player1.shield_health_last):
        player1.block_success += 1
    elif((data[16] + 1.5) < player2.shield_health_last):
        player2.block_success += 1
    #if you gained percent you didn't
    if(data[7] > player1.percentage_last):
        player1.block_failed += 1
    if(data[15] > player2.percentage_last):
        player2.block_failed += 1

def update_flags(player1, player2, data):
    #punish check - took damage and wasn't in a punish
    if(data[7] > player1.percentage_last):
        if(player1.punish_state == False):
            player2.punish_amount += 1
        player1.punish_state = True
        player1.punish_time = 0
    if(data[15] > player2.percentage_last):
        if(player2.punish_state == False):
            player1.punish_amount += 1
        player2.punish_state = True
        player2.punish_time = 0

    #damaged check
    if(data[3] in range(75, 91)):
        player1.damaged_state = True
    else:
        player1.damaged_state = False

    if(data[11] in range(75, 91)):
        player2.damaged_state = True
    else:
        player2.damaged_state = False

    #offstage check
    edge = ledge_position[stage_index[data[0]]]
    #offstage = x > edge_x+characterlen or y < -10 (under stage)
    if((abs(data[4]) > abs(edge[0])) or (data[5] < (edge[1] - 10))):
        player1.offstage_state = True
    else:
        if(player1.recovery_state == True and data[3] not in range(0, 13)):
            player1.recovery_state = False
            player1.recovery_success += 1
        player1.offstage_state = False

    if((abs(data[12]) > abs(edge[0])) or (data[13] < (edge[1] - 10))):
        player2.offstage_state = True
    else:
        if(player2.recovery_state == True and data[11] not in range(0, 13)):
            player2.recovery_state = False
            player2.recovery_success += 1
        player2.offstage_state = False

def check_recovery(player1, player2):
    #recovery check
    if(player1.offstage_state == True and player1.damaged_state == False):
        player1.recovery_state = True
    if(player2.offstage_state == True and player2.damaged_state == False):
        player2.recovery_state = True

def on_death_check(player1, player2, data):
    if(data[3] == 12):
        if(player1.recovery_state == True):
            player1.recovery_state = False
            player1.punish_state = False
            player1.damaged_state = False
            player1.offstage_state = False
            player1.punish_time = 0
            player1.recovery_fail += 1
    if(data[11] == 12):
        if(player2.recovery_state == True):
            player2.recovery_state = False
            player2.punish_state = False
            player2.damaged_state = False
            player2.offstage_state = False
            player2.punish_time = 0
            player2.recovery_fail += 1

def check_shield_pressure(data):
    #returns boolean tuple, (player1, player2)
    #True means player is currently pressuring shield
    #players are close
    distance = sqrt(pow((data[12] - data[4]), 2) + pow((data[13] - data[5]), 2))
    if(distance < 15):
        #player 1 under pressure
        if(data[8] <= 25.0 and data[3] == 179):
            return (False, True)
        #player 2 under pressure
        elif(data[16] <= 25.0 and data[11] == 179):
            return (True, False)

    return (False, False)

def check_neutral(player1, player2, data):
    #check_neutral - (# punishes by this player/# of punishes total)
        #punish - starts when player takes damage, ends when player is on stage and doesnt take damage for 120 frames (2 seconds)
    #punish time increment
    if(player1.damaged_state == False and player1.offstage_state == False and player1.punish_state == True):
        player1.punish_time += 1
    if(player2.damaged_state == False and player2.offstage_state == False and player2.punish_state == True):
        player2.punish_time += 1

    #punish ended check
    if(player1.punish_time >= 120):
        player1.punish_state = False
        player1.punish_time = 0
    if(player2.punish_time >= 120):
        player2.punish_state = False
        player2.punish_time = 0
