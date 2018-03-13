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
    #number of neutral wins
    neutral_wins = 0
    #number of sucessful/failed blocks
    block_success = 0
    block_failed = 0
    #number of sucessful/failed attacks
    attack_success = 0
    attack_failed = 0

def update_analytics(player1, player2, data):
    #frame num, (player index, action, x, y, direction, percent, shield, stocks) x 2
    check_stage_control(player1, player2, data)
    check_above(player1, player2, data)
    check_shielding(player1, player2, data)
    check_block(player1, player2, data)
    #check attack - successful attacks easy, failed attacks not easy (too many possibilities)
    #check_neutral - ambiguous and hard to program
    #recovery_analysis : more complex than other stats but doable

    #update shield and percentage for next run
    player1.shield_health_last = data[7]
    player1.percentage_last = data[6]
    player2.shield_health_last = data[15]
    player2.percentage_last = data[14]


def check_stage_control(player1, player2, data):
    #stage control - when you are inside middle 100 pixels and opponent outside it
    if(abs(data[3]) <= 50 and abs(data[11]) > 50):
        player1.stage_control += 1
    elif(abs(data[11]) <= 50 and abs(data[3]) > 50):
        player2.stage_control += 1

def check_above(player1, player2, data):
    #if player is above the other
    if(data[4] > data[12]):
        player1.above_opponent += 1
    elif(data[12] > data[4]):
        player2.above_opponent += 1

def check_shielding(player1, player2, data):
    #if player is shielding
    if(data[2] == 179):
        player1.time_shielded += 1
    if(data[10] == 179):
        player2.time_shielded += 1

def check_block(player1, player2, data):
    #if you took abnormal shield damage you blocked an attack
    #the plus 1.5 accounts for natural shield degeneration
    if((data[7] + 1.5) < player1.shield_health_last):
        player1.block_success += 1
    elif((data[15] + 1.5) < player2.shield_health_last):
        player2.block_success += 1
    #if you gained percent you didn't
    if(data[6] > player1.percentage_last):
        player1.block_failed += 1
    if(data[14] > player2.percentage_last):
        player2.block_failed += 1
