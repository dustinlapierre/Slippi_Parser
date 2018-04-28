from structures import *
from general import *
#this file contains functions that produce commentary strings
def print_final_stats():
    if(player1_analytics.recovery_success != 0):
        p1_recovery_percent = ((player1_analytics.recovery_success/(player1_analytics.recovery_success+player1_analytics.recovery_fail))*100)
    else:
        p1_recovery_percent = 0
    if((player1_analytics.punish_amount + player2_analytics.punish_amount) != 0):
        p1_neutral_percent = ((player1_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))*100)
    else:
        p1_neutral_percent = 0

    if(player2_analytics.recovery_success != 0):
        p2_recovery_percent = ((player2_analytics.recovery_success/(player2_analytics.recovery_success+player2_analytics.recovery_fail))*100)
    else:
        p2_recovery_percent = 0
    if((player2_analytics.punish_amount + player1_analytics.punish_amount) != 0):
        p2_neutral_percent = ((player2_analytics.punish_amount/(player2_analytics.punish_amount + player1_analytics.punish_amount))*100)
    else:
        p2_neutral_percent = 0

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
    if(player2_data.stocks_remaining != 4):
        print("Openings Per Kill:", (player1_analytics.punish_amount/(4 - player2_data.stocks_remaining)))

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
    if(player1_data.stocks_remaining != 4):
        print("Openings Per Kill:", (player2_analytics.punish_amount/(4 - player1_data.stocks_remaining)))

    return (
    "Player 1 Important Stats ----------" + "\n" +
    "Frames in stage control: " + str(player1_analytics.stage_control) + "\n" +
    "Recovery %: " + str(p1_recovery_percent) + "\n" +
    "Neutral Win %: " + str(p1_neutral_percent) + "\n" +
    "Player 2 Important Stats ----------" + "\n" +
    "Frames in stage control: " + str(player2_analytics.stage_control) + "\n" +
    "Recovery %: " + str(p2_recovery_percent) + "\n" +
    "Neutral Win %: " + str(p2_neutral_percent)
    )

def recovery_comment():
    if(player1_analytics.recovery_success != player1_analytics.recovery_success_last):
        return choose("Good recovery from Player 1.",
                        "Player 2 drops the edge guard.")
    elif(player1_analytics.recovery_fail != player1_analytics.recovery_fail_last):
        return choose("Good edge guard from Player 2.",
                        "And Player 2 gets the edge guard.")
    if(player2_analytics.recovery_success != player2_analytics.recovery_success_last):
        return choose("Good recovery from Player 2.",
                        "Player 1 drops the edge guard.")
    elif(player2_analytics.recovery_fail != player2_analytics.recovery_fail_last):
        return choose("Good edge guard from Player 1.",
                        "And Player 1 gets the edge guard.")
    return None

def taunt_comment():
    if(player1_data.action_state in range(264, 266)):
        return "Player 1 is feeling themselves with that taunt."
        player1_analytics.taunt_timer = 600
    elif(player2_data.action_state in range(264, 266)):
        return "Player 2 is feeling themselves with that taunt."
        player2_analytics.taunt_timer = 600
    return None
