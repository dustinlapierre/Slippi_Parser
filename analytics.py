class player_analytics:
    #shield health last frame (for detecting blocks)
    shield_health_last = -1.0
    #percentage last frame (for detecting hits)
    percentage_last = -1.0
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
    #check_shielding
    #check_neutral
    #check block
    #check attack

    #recovery_analysis : more complex than other stats

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
