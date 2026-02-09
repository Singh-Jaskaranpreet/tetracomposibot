# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant : Jaskaranpreet SINGH 21239295
#  Prénom Nom No_étudiant : Guillaume QU 21316059
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

import math
from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Centurion"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0        # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier
    Best_PARAM = [1, -1, 0, 1, 1, 0, 0, -1] # variable globale pour stocker les meilleurs Best_PARAMètres trouvés par l'algorithme génétique, à utiliser pour le robot 3


    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # Robot 1 : robot explorateur
        # Il avance presque en permanence pour couvrir un maximum de terrain,
        # ajuste légèrement sa vitesse selon l’espace devant,
        # évite les murs grâce à la rotation,
        # et utilise un peu d’aléatoire pour ne pas tourner en rond.

        if self.robot_id == 1 :
            
            front_space = min(sensors[sensor_front],sensors[sensor_front_left],sensors[sensor_front_right])
            translation = front_space*0.4+0.5 # ON  CONTINUE MEME SI ON A BLOQUE DEVANT, ON ESSAIE DE SE FAUFILER


            danger_left  = (1 - sensors[sensor_left]) + (1 - sensors[sensor_front_left])
            danger_right = (1 - sensors[sensor_right]) + (1 - sensors[sensor_front_right])

            rotation = (danger_right - danger_left) * 0.3
            rotation += (random.random() - 0.5) * 0.1

        
        # Robot 0 : robot d’évitement stable
        # Il avance quand l’espace devant est libre,
        # évite les murs en comparant le danger à gauche et à droite,
        # et utilise sa mémoire pour garder la même direction
        # quand la situation est ambiguë (évite le zigzag).

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
                translation = 0.1
                rotation = self.memory

            elif int(self.log_sum_of_translation) == self.memory :
                if int(self.log_sum_of_translation) == 0 :
                    translation = 1
                    rotation = (random.random() - 0.5) * 0.01
                else :
                    if sensors[sensor_front] > 0.8  and sensors[sensor_front_left] > 0.3 and sensors[sensor_front_right] > 0.3 and sensors[sensor_left] > 0.15 and sensors[sensor_right] > 0.15:
                        translation = 1 
                        rotation = (random.random() - 0.5) * 0.01
                    else :
                        self.memory = random.choice([-1, 1])
                        translation = 0.1
                        rotation = self.memory

            elif sensors[sensor_front] > 0.8:
                translation = 1
                rotation = (random.random() - 0.5) * 0.01
                self.memory = int(self.log_sum_of_translation)

            elif (self.memory == 1 or self.memory == -1 ):  
                translation = 0.1
                rotation = self.memory

            else :
                translation = 1
                rotation = (random.random() - 0.5) * 0.01
                self.memory = int(self.log_sum_of_translation)
            
            print("front =", sensors[sensor_front],")  left = ",sensors[sensor_left], " right = ", sensors[sensor_right], "f left = ", sensors[sensor_front_left], "f rightt = ", sensors[sensor_front_right])
            print("rotation = ", rotation, " translation", translation, "\n")
            print(self.x,"    ",self.y)
            print("sum tran", int(self.log_sum_of_translation), " mem =",self.memory)
            

        # Robot 3 : robot optimisé par algorithme génétique
        # Ce robot utilise un comportement de type Braitenberg (capteurs → moteurs).
        # Les coefficients de translation et de rotation ont été optimisés
        # hors ligne à l’aide d’un algorithme génétique.
        # Pendant l’exécution du match, les paramètres sont fixes :
        # le robot applique directement la fonction de contrôle apprise


        elif self.robot_id == 3:

        # fonction de contrôle (qui dépend des entrées sensorielles, et des Best_PARAMètres)
            translation = math.tanh ( self.Best_PARAM[0] + self.Best_PARAM[1] * sensors[sensor_front_left] + self.Best_PARAM[2] * sensors[sensor_front] + self.Best_PARAM[3] * sensors[sensor_front_right] )
            rotation = math.tanh ( self.Best_PARAM[4] + self.Best_PARAM[5] * sensors[sensor_front_left] + self.Best_PARAM[6] * sensors[sensor_front] + self.Best_PARAM[7] * sensors[sensor_front_right] )


        

        return translation, rotation, False

