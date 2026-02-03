# Configuration file (C: hateWall).

import arenas
import robot_braitenberg_hateWall

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

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    margin = int(particle_box * 3)
    x_left = margin + 4
    y_mid = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(robot_braitenberg_hateWall.Robot_player(x_left, y_mid, 180, name="hateWall", team="A"))
    return robots
