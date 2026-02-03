# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 1
position = False 
max_iterations = 501 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = True # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import sys
import config_A
import config_B
import config_C
import config_D
import config_E
import config_F

# Choix du comportement via l'argument position:
# python tetracomposibot.py config_TP1 1 A
# A: avoider, B: hateBot, C: hateWall, D: loveWall, E: loveBot, F: subsomption
behavior_choice = "A"
if len(sys.argv) >= 4:
    arg = str(sys.argv[3]).strip()
    if arg:
        behavior_choice = arg.upper()


def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    choice = behavior_choice
    if choice == "A":
        return config_A.initialize_robots(arena_size, particle_box)
    if choice == "B":
        return config_B.initialize_robots(arena_size, particle_box)
    if choice == "C":
        return config_C.initialize_robots(arena_size, particle_box)
    if choice == "D":
        return config_D.initialize_robots(arena_size, particle_box)
    if choice == "E":
        return config_E.initialize_robots(arena_size, particle_box)
    if choice == "F":
        return config_F.initialize_robots(arena_size, particle_box)
    return config_A.initialize_robots(arena_size, particle_box)
