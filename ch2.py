# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Achmad Firza Fuadi 21307932
#  Prénom Nom No_étudiant/e : Chami Ayman 21315473
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

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

        # ------------------------------------------------------------
        # Reculer si un obstacle est trop proche
        # ------------------------------------------------------------
        if (sensors[sensor_front] < 0.15 or
            sensors[sensor_front_left] < 0.10 or
            sensors[sensor_front_right] < 0.10) or self.memory > 0:
            if self.memory == 0:
                self.memory = 3
            else:
                self.memory -= 1
            v = -0.3  # reculer

            if sensors[sensor_front_left] > sensors[sensor_front_right]:
                w = 1.0
            else:
                w = -1.0

            return v, w, False
        
        # ------------------------------------------------------------
        # CHASE ENEMY
        # ------------------------------------------------------------
        if self.robot_id == 0:
            imin = 0
            for i in range(1, 8):
                if i in [sensor_rear_left, sensor_rear, sensor_rear_right]:
                    continue
                if sensor_team[i] != self.team_name:
                    if sensor_to_robot[i] < sensor_to_robot[imin] :
                        imin = i

            if sensor_to_robot[imin] < 0.3:
                translation = sensor_to_robot[sensor_front]*0.5
                rotation = (random.random()-0.5)*0.1
                if imin == sensor_front:
                    rotation = random.choice([-0.1, 0.1]) + (random.random()-0.5)*0.1
                elif imin == sensor_front_left or imin == sensor_left:
                    rotation = 0.5 * sensor_to_robot[sensor_front_left] + 0.9 * sensor_to_robot[sensor_left] + (random.random()-0.5)*0.1
                elif imin == sensor_front_right or imin == sensor_right:
                    rotation = - 0.4 * sensor_to_robot[sensor_front_right] - 0.8 * sensor_to_robot[sensor_right] + (random.random()-0.5)*0.1

                return translation, rotation, False

        # ------------------------------------------------------------
        # 1. ENNEMI DEVANT
        # ------------------------------------------------------------
        enemy_ahead = False
        if sensor_robot is not None and sensor_team is not None:
            rid = sensor_robot[sensor_front]
            rteam = sensor_team[sensor_front]
            if rid != -1 and rteam != self.team_name:
                enemy_ahead = True

        if enemy_ahead:
            return 0.5, (random.random()-0.5)*1.0, False
        
        
        # ------------------------------------------------------------
        # 2. Braitenberg avec poids optimizé par Algorithme génétique
        # ------------------------------------------------------------
        if self.robot_id == 1:
            param = [0.4610170044648054, 0.16055430911265922, 0.9102720238017682, 0.7340279886815912]
            translation = sensors[sensor_front] * param[0]
            rotation = param[1]*random.choice([1, -1]) * sensors[sensor_front] + param[2] * sensors[sensor_front_left] - param[3] * sensors[sensor_front_right] + (random.random()-0.5)*0.1
            return translation, rotation, False
        
        if self.robot_id == 2:
            proba = random.random()
            if proba < 0.5:
        # ------------------------------------------------------------
        # 3. ROBOT 1 : exploration large (rotation légère)
        # ------------------------------------------------------------
                translation = 0.8 * sensors[sensor_front] + 0.1
                rotation = 0.4 * sensors[sensor_front_left] - 0.4 * sensors[sensor_front_right]
                rotation += 0.15  # biais pour tourner légèrement
                return translation, rotation, False
        # ------------------------------------------------------------
        # 4. ROBOT 2 : exploration large (rotation opposée)
        # ------------------------------------------------------------
            translation = 0.8 * sensors[sensor_front] + 0.1
            rotation = 0.4 * sensors[sensor_front_left] - 0.4 * sensors[sensor_front_right]
            rotation -= 0.15  # biais opposé
            return translation, rotation, False

        # ------------------------------------------------------------
        # ÉVITEMENT ALÉATOIRE
        # ------------------------------------------------------------
        translation = sensors[sensor_front]*0.5
        rotation = 0.8*random.choice([1, -1]) * sensors[sensor_front] + 0.7 * sensors[sensor_front_left] - 0.7 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
        return translation, rotation, False
