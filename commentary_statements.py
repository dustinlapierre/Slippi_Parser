from structures import *
#this file contains functions that produce commentary strings
def send_stats_gui(stats_queue):
    if(stats_queue.empty()):
        stats = []
        stats.append(str(player1_analytics.stage_control))
        stats.append(str(player1_analytics.above_opponent))
        stats.append(str(player1_analytics.time_offstage))
        stats.append(str(player1_analytics.time_shielded))
        stats.append(str(player1_analytics.block_success))
        stats.append(str(player1_analytics.block_failed))
        stats.append(str(player1_analytics.punish_amount))
        if(player1_analytics.punish_amount != 0):
            stats.append(str((player2_analytics.block_failed/player1_analytics.punish_amount)))
        else:
            stats.append("0")
        if(player1_analytics.recovery_success != 0):
            stats.append(str((player1_analytics.recovery_success/(player1_analytics.recovery_success+player1_analytics.recovery_fail))*100))
        else:
            stats.append("0")
        if((player1_analytics.punish_amount + player2_analytics.punish_amount) != 0):
            stats.append(str((player1_analytics.punish_amount/(player1_analytics.punish_amount + player2_analytics.punish_amount))*100))
        else:
            stats.append("0")
        if(player2_data.stocks_remaining != 4):
            stats.append(str((player1_analytics.punish_amount/(4 - player2_data.stocks_remaining))))
        else:
            stats.append("0")

        stats.append(str(player2_analytics.stage_control))
        stats.append(str(player2_analytics.above_opponent))
        stats.append(str(player2_analytics.time_offstage))
        stats.append(str(player2_analytics.time_shielded))
        stats.append(str(player2_analytics.block_success))
        stats.append(str(player2_analytics.block_failed))
        stats.append(str(player2_analytics.punish_amount))
        if(player2_analytics.punish_amount != 0):
            stats.append(str((player1_analytics.block_failed/player2_analytics.punish_amount)))
        else:
            stats.append("0")
        if(player2_analytics.recovery_success != 0):
            stats.append(str((player2_analytics.recovery_success/(player2_analytics.recovery_success+player2_analytics.recovery_fail))*100))
        else:
            stats.append("0")
        if((player2_analytics.punish_amount + player1_analytics.punish_amount) != 0):
            stats.append(str((player2_analytics.punish_amount/(player2_analytics.punish_amount + player1_analytics.punish_amount))*100))
        else:
            stats.append("0")
        if(player1_data.stocks_remaining != 4):
            stats.append(str((player2_analytics.punish_amount/(4 - player1_data.stocks_remaining))))
        else:
            stats.append("0")
        stats_queue.put(stats)
        stats_queue.join()
    """
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
    """

def recovery_comment():
    if(player1_analytics.recovery_success != player1_analytics.recovery_success_last):
        return "Good recovery from Player 1."
    elif(player1_analytics.recovery_fail != player1_analytics.recovery_fail_last):
        return "Good edge guard from Player 2."
    if(player2_analytics.recovery_success != player2_analytics.recovery_success_last):
        return "Good recovery from Player 2."
    elif(player2_analytics.recovery_fail != player2_analytics.recovery_fail_last):
        return "Good edge guard from Player 1."
    return None

def taunt_comment():
    if(player1_data.action_state in range(264, 266)):
        return "Player 1 feeling themselves with that taunt."
        player1_analytics.taunt_timer = 600
    elif(player2_data.action_state in range(264, 266)):
        return "Player 2 feeling themselves with that taunt."
        player2_analytics.taunt_timer = 600
    return None
