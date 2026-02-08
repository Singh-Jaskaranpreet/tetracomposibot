# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant : Jaskaranpreet SINGH 21239295
#  Prénom Nom No_étudiant : Guillaume QU 21316059
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Centurion"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = random.choice([-1,1])         # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if self.robot_id == 1 :
            if sensors[sensor_left] < 0.1 and sensors[sensor_right] < 0.1 :
                if sensors[sensor_front] < 0.2 :
                    rotation = self.memory
                else :
                    rotation = 0
                    translation = 0.2

            elif sensors[sensor_left] < 0.2 or sensors[sensor_right] < 0.2 :
                translation = 0.1
                rotation =  self.memory * 0.5

            elif sensors[sensor_left] > 0.7 or sensors[sensor_right] > 0.7 :
                if sensors[sensor_front] == 1 :
                    translation = 0.75
                    rotation = 0
                else :
                    translation = 0
                    rotation = self.memory * 0.66

            elif sensors[sensor_front] < 1 :
                translation = -0.001
                rotation = self.memory

            elif sensors[sensor_front_left] < 1 or sensors[sensor_front_right] < 1 :
                translation = -0.001
                rotation = self.memory

            else :
                translation = 0.75
                rotation = (random.random() - 0.5) * 0.1
            
            

        elif self.robot_id == 0 :
            translation = sensors[sensor_front]*0.4
            rotation = -(1-sensors[sensor_left])*0.2-(1-sensors[sensor_front_left])*0.25+(1-sensors[sensor_front_right])*0.25+(1-sensors[sensor_right])*0.2

        elif self.robot_id == 2 :
            if sensors[sensor_front] < 0.15 :
                if self.memory == 0 :
                    self.memory = random.choice([-1, 1])
                translation = 0
                rotation = self.memory

            elif self.log_sum_of_translation == 0 :
                if self.memory == 0 :
                    self.memory = random.choice([-1, 1])
                translation = 0
                rotation = self.memory

            else :
                translation = 1
                rotation = 0
                self.memory = 0
            print("front =", sensors[sensor_front],")  left = ",sensors[sensor_left], " right = ", sensors[sensor_right], "f left = ", sensors[sensor_front_left], "f rightt = ", sensors[sensor_front_right])
            print("rotation = ", rotation, " translation", translation, "\n")
            print("sum trans = ", self.log_sum_of_translation, "  sum rota = ", self.log_sum_of_rotation)
        elif self.robot_id == 3 :
            translation = sensors[sensor_front]*0.5 # A MODIFIER
            rotation = 0.5 # A MODIFIER

       

        return translation, rotation, False

