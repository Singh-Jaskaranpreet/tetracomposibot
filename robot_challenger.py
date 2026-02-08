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
    memory = 0        # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        #robot explorateur
        if self.robot_id == 1 :
            
            front_space = min(sensors[sensor_front],sensors[sensor_front_left],sensors[sensor_front_right])
            translation = front_space*0.4+0.5 # ON  CONTINUE MEME SI ON A BLOQUE DEVANT, ON ESSAIE DE SE FAUFILER


            danger_left  = (1 - sensors[sensor_left]) + (1 - sensors[sensor_front_left])
            danger_right = (1 - sensors[sensor_right]) + (1 - sensors[sensor_front_right])

            rotation = (danger_right - danger_left) * 0.3
            rotation += (random.random() - 0.5) * 0.1

        

        elif self.robot_id == 0 :

            front_space = min(sensors[sensor_front],sensors[sensor_front_left],sensors[sensor_front_right])
            translation = front_space*0.4


            danger_left  = (1 - sensors[sensor_left]) + (1 - sensors[sensor_front_left])
            danger_right = (1 - sensors[sensor_right]) + (1 - sensors[sensor_front_right])

            rotation = (danger_right - danger_left) * 0.3
            
             #ON utiliser la mémoire SI ON A CONINSE DANS GAUCHE ,DROTE 
            if abs(rotation) > 0.1:
                if rotation > 0:
                    self.memory = 1      # il memeorise que il avait troue  gauche donc si il est concine prochant fois il continuer a tourner a gauche
                else:
                    self.memory = -1     # pareil pour droite
            else:
                # hésitation donc il continue pareil comme la dernier fois 
                rotation = self.memory * 0.2

        elif self.robot_id == 2 :
            """
            translation = sensors[sensor_front]*0.1+0.2
            rotation = 0.2 * sensors[sensor_left] + 0.2 * sensors[sensor_front_left] - 0.2 * sensors[sensor_right] - 0.2 * sensors[sensor_front_right] + (random.random()-0.5)*1
            
            """
            if sensors[sensor_front] < 0.15 :
                if self.memory != -1 and self.memory != 1 :
                    self.memory = random.choice([-1, 1])
                translation = 0
                rotation = self.memory

            elif ((self.memory == 1 or self.memory == -1 ) or self.log_sum_of_translation !=0) and self.log_sum_of_translation == self.memory:
                if self.memory != -1 and self.memory != 1 :
                    self.memory = random.choice([-1, 1])
                translation = 0
                rotation = self.memory

            else :
                translation = 1
                rotation = (random.random() - 0.5) * 0.01
                self.memory = self.log_sum_of_translation
                

            print("front =", sensors[sensor_front],")  left = ",sensors[sensor_left], " right = ", sensors[sensor_right], "f left = ", sensors[sensor_front_left], "f rightt = ", sensors[sensor_front_right])
            print("rotation = ", rotation, " translation", translation, "\n")
            print(self.x,"    ",self.y)
            print("sum tran", self.log_sum_of_translation, " mem =",self.memory)

        elif self.robot_id == 3 :
            translation = sensors[sensor_front]*0.5 # A MODIFIER
            rotation = 0.5 # A MODIFIER

       

        return translation, rotation, False

