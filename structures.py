#command bytes
EVENT_PAYLOADS = "0x35"
GAME_START = "0x36"
PRE_FRAME_UPDATE = "0x37"
POST_FRAME_UPDATE = "0x38"
GAME_END = "0x39"

#event data holders
class game_start_event:
    command_byte = GAME_START
    version = [] #major.minor.build.revision
    game_info_block = [] #not sure what this is
    is_teams = 0
    stage = 0
    character_ID_port1 = 0
    character_ID_port2 = 0
    character_ID_port3 = 0
    character_ID_port4 = 0
    player_type_port1 = 0
    player_type_port2 = 0
    player_type_port3 = 0
    player_type_port4 = 0
    character_color_port1 = 0
    character_color_port2 = 0
    character_color_port3 = 0
    character_color_port4 = 0
    team_ID_port1 = 0
    team_ID_port2 = 0
    team_ID_port3 = 0
    team_ID_port4 = 0
    random_seed = 0

class pre_frame_event:
    command_byte = PRE_FRAME_UPDATE
    frame_number = 0
    player_index = 0 #port is this +1
    is_follower = 0
    random_seed = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 0.0
    joystick_x = 0.0
    joystick_y = 0.0
    c_stick_x = 0.0
    c_stick_y = 0.0
    trigger = 0.0
    buttons = 0
    physical_buttons = 0
    physical_l = 0.0
    physical_r = 0.0

class post_frame_event:
    command_byte = PRE_FRAME_UPDATE
    frame_number = 0
    player_index = 0
    is_follower = 0
    internal_character_ID = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 0.0
    percent = 0.0
    shield_size = 0.0
    last_attack_landed = 0
    current_combo_count = 0
    last_hit_by = 0
    stocks_remaining = 0

class game_end_event:
    command_byte = GAME_END
    game_end_method = 0

class player_analytics:
    #shield health last frame (for detecting blocks)
    shield_health_last = -1.0
    #percentage last frame (for detecting hits)
    percentage_last = 0.0
    #recovery stuff last frame (for detecting recoveries in main commentary)
    recovery_success_last = 0
    recovery_fail_last = 0
    #number of frames in stage control
    stage_control = 0
    #number of frames above opponent
    above_opponent = 0
    #number of frames spent in shield
    time_shielded = 0
    #number of frames offstage
    time_offstage = 0
    #number of sucessful/failed recoveries
    recovery_success = 0
    recovery_fail = 0
    #number of sucessful/failed blocks
    block_success = 0
    block_failed = 0
    #number of punishes this player gets
    punish_amount = 0
    punish_time = 0
    #set to 600 when a player taunts for taunt to get bodied check
    taunt_timer = 0
    #flags
    punish_state = False
    damaged_state = False
    offstage_state = False
    recovery_state = False

class player_data:
    player_index = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 1
    percent = 0.0
    shield_size = 0.0
    stocks_remaining = 0

class match_info:
    player1_character = ""
    player2_character = ""
    stage = ""

def post_frame_as_list():
    data = []
    data.append(post_frame_data.player_index)
    data.append(post_frame_data.action_state)
    data.append(post_frame_data.x_pos)
    data.append(post_frame_data.y_pos)
    data.append(post_frame_data.facing_direction)
    data.append(post_frame_data.percent)
    data.append(post_frame_data.shield_size)
    data.append(post_frame_data.stocks_remaining)
    return data

def update_player_data(player_data):
    player_data.player_index = post_frame_data.player_index
    player_data.action_state = post_frame_data.action_state
    player_data.x_pos = post_frame_data.x_pos
    player_data.y_pos = post_frame_data.y_pos
    player_data.facing_direction = post_frame_data.facing_direction
    player_data.percent = post_frame_data.percent
    player_data.shield_size = post_frame_data.shield_size
    player_data.stocks_remaining = post_frame_data.stocks_remaining

#ALL GLOBAL DATA HOLDERS -------------------
#data holders
#variable values will be updated each time one of these
#commands are encountered in the replay file
game_start_data = game_start_event()
pre_frame_data = pre_frame_event()
post_frame_data = post_frame_event()
game_end_data = game_end_event()
player1_analytics = player_analytics()
player2_analytics = player_analytics()
match = match_info()
player1_data = player_data()
player2_data = player_data()

#depricated only for use in analytics and LSTM update until that file is updated
player1_data_dep = []
player2_data_dep = []
