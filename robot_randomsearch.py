
from robot import * 
import math
import random

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "Optimizer"
    robot_id = -1
    iteration = 0
    score = 0.0
    best_score = -1e9
    param = []
    bestParam = []
    it_per_evaluation = 400
    trial = 0
    max_trials = 500
    best_trial = -1
    replay_cycle = 0

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a",evaluations=0,it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.it_per_evaluation = it_per_evaluation

        self.last_log_translation = 0.0
        self.last_log_rotation = 0.0
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        super().reset()
        self.last_log_translation = 0.0
        self.last_log_rotation = 0.0

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # cet exemple montre comment générer au hasard, et évaluer, des stratégies comportementales
        # Remarques:
        # - la liste "param", définie ci-dessus, permet de stocker les paramètres de la fonction de contrôle
        # - la fonction de controle est une combinaison linéaire des senseurs, pondérés par les paramètres (c'est un "Perceptron")

        # calcul du score à partir du déplacement effectif de l'itération précédente
        if self.iteration > 0:
            delta_translation = self.log_sum_of_translation - self.last_log_translation
            delta_rotation = self.log_sum_of_rotation - self.last_log_rotation
            self.score += delta_translation * (1 - abs(delta_rotation))
            self.last_log_translation = self.log_sum_of_translation
            self.last_log_rotation = self.log_sum_of_rotation

        # toutes les X itérations: le robot est remis à sa position initiale de l'arène avec une orientation aléatoire
        if self.iteration > 0 and self.iteration % self.it_per_evaluation == 0:
                # apres chaque evaluation on affiche les resultats et on genere de nouveaux parametres
                if self.it_per_evaluation == 400:
                    print ("\tparameters           =",self.param)
                    print ("\ttranslations         =",self.log_sum_of_translation,"; rotations =",self.log_sum_of_rotation) # *effective* translation/rotation (ie. measured from displacement)
                    print ("\tdistance from origin =",math.sqrt((self.x-self.x_0)**2+(self.y-self.y_0)**2))
                    print ("Score for trial", self.trial, ":", self.score)
                    if self.score > self.best_score:
                        self.best_score = self.score
                        self.bestParam = self.param.copy()
                        self.best_trial = self.trial
                        print ("New best score :", self.best_score, "(trial", self.best_trial, ")")
                        print ("parameters :", self.bestParam)
                        print ("-------------------------")

                # fin de chaque meilleur comportement rejoue
                if self.it_per_evaluation == 1000:
                    print ("-------------------------")
                    print ("Fin meilleur comportement, cycle", self.replay_cycle)
                    print ("Score du cycle :", self.score)
                    print ("Meilleurs paramètres :", self.bestParam)
                    self.replay_cycle = self.replay_cycle + 1
                    print ("Rejouer meilleur comportement, cycle", self.replay_cycle)
                    print ("-------------------------")

                self.score = 0.0
                self.iteration = 0
#a la fin de 500 trails on rejoue le meilleur
                if self.trial == self.max_trials and self.it_per_evaluation == 400:
                    self.param = self.bestParam.copy()
                    self.it_per_evaluation = 1000
                    print ("-------------------------")
                    print ("Budget épuisé:", self.max_trials, "essais.")
                    print ("Meilleur score :", self.best_score, "(trial", self.best_trial, ")")
                    print ("Meilleurs paramètres :", self.bestParam)
                    self.replay_cycle = 1
                    print ("Rejouer meilleur comportement, cycle", self.replay_cycle)
                    print ("-------------------------")
                    self.trial = self.max_trials + 1
                    return 0, 0, True # ask for reset
                
                #pour chauque essai on génère des nouveaux paramètres
                if self.it_per_evaluation == 400:
                    self.param = [random.randint(-1, 1) for i in range(8)]
                    self.trial = self.trial + 1
                    print ("-------------------------")
                    print ("Trying strategy no.",self.trial)
                    return 0, 0, True # ask for reset

        # fonction de contrôle (qui dépend des entrées sensorielles, et des paramètres)
        translation = math.tanh ( self.param[0] + self.param[1] * sensors[sensor_front_left] + self.param[2] * sensors[sensor_front] + self.param[3] * sensors[sensor_front_right] )
        rotation = math.tanh ( self.param[4] + self.param[5] * sensors[sensor_front_left] + self.param[6] * sensors[sensor_front] + self.param[7] * sensors[sensor_front_right] )

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)

        self.iteration = self.iteration + 1

        return translation, rotation, False
