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
    #check recovery

    #check_neutral - (# punishes by this player/# of punishes total)
        #punish - starts when player takes damage, ends when player is on stage and doesnt take damage for 120 frames (2 seconds)

    #recovery_analysis : more complex than other stats but doable
        #When player in damaged state off stage then offstage begins
        #if damaged state is gone during offstage (player didn't die from hit) then recovery/edge guard begins
            #ON DEATH
            #if offstage = true and recovery = false: initial hit killed player
                #reset all flags
            #if offstage and recovery = True
                #recovery failed, edge guard success, reset flags
        #If player reaches stage, reset flags
        #offstage = x > edge_x+characterlen or y < -10 (under stage)
        #damaged state = action state 75-91


    #update shield and percentage for next run
    player1.shield_health_last = data[8]
    player1.percentage_last = data[7]
    player2.shield_health_last = data[16]
    player2.percentage_last = data[15]
    #TODO update punish


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
    #offstage = x > edge_x+characterlen or y < -10 (under stage)


def check_neutral(player1, player2, data):
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
