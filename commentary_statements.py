from structures import *
#this file contains functions that produce commentary strings
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
