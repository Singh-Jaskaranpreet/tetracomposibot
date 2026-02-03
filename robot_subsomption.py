
from robot import * 

nb_robots = 0
debug = True

def behavior_toutDroit():
    return 0.4, 0.0

def behavior_hateWall(sensor_to_wall):
    translation = sensor_to_wall[sensor_front] * 0.4
    rotation = (
        -(1 - sensor_to_wall[sensor_left]) * 0.15
        - (1 - sensor_to_wall[sensor_front_left]) * 0.2
        + (1 - sensor_to_wall[sensor_front_right]) * 0.2
        + (1 - sensor_to_wall[sensor_right]) * 0.15
        + (random.random() - 0.5) * 0.2
    )
    return translation, rotation

def behavior_LoveBot(sensors, sensor_to_robot):
    translation = sensors[sensor_front] * 0.4
    rotation = (1 - sensor_to_robot[sensor_front_left]) - (1 - sensor_to_robot[sensor_front_right])
    return translation, rotation

class Robot_player(Robot):

    team_name = "subsomption"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        # --- subsomption (priorites) ---
        wall_is_close = min(
            sensor_to_wall[sensor_front],
            sensor_to_wall[sensor_front_left],
            sensor_to_wall[sensor_front_right],
            sensor_to_wall[sensor_left],
            sensor_to_wall[sensor_right],
        ) < 0.6 # on a chosi 0.6 pour detecter les murs un peu plus tot

        robot_seen = min(sensor_to_robot) < 1.0 

        if wall_is_close:
            translation, rotation = behavior_hateWall(sensor_to_wall)
        elif robot_seen:
            translation, rotation = behavior_LoveBot(sensors, sensor_to_robot)
        else:
            translation, rotation = behavior_toutDroit()

        self.iteration = self.iteration + 1        
        return translation, rotation, False
