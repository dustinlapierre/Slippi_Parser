from analytics import player_analytics

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

class player_data:
    player_index = 0
    action_state = 0
    x_pos = 0.0
    y_pos = 0.0
    facing_direction = 1
    percent = 0.0
    shield_size = 0.0
    stocks_remaining = 0

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
player1_character = ""
player2_character = ""
player1_data = player_data()
player2_data = player_data()

#depricated only for use in analytics and LSTM update until that file is updated
player1_data_dep = []
player2_data_dep = []
