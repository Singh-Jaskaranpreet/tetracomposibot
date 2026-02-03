
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
    repeats_per_eval = 3
    repeat_count = 0
    score_total = 0.0

    parent_param = []
    parent_score = None
    child_param = []
    child_score = None
    evaluation_child = False


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
        self.parent_param = [random.randint(-1, 1) for i in range(8)]
        self.param = self.parent_param.copy()
        self.it_per_evaluation = it_per_evaluation

        self.last_log_translation = 0.0
        self.last_log_rotation = 0.0
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # orientation aleatoire a chaque evaluation
        self.theta0 = random.randint(0, 359)
        super().reset()
        self.last_log_translation = 0.0
        self.last_log_rotation = 0.0

    def mutation(self, param):
        new_param = param.copy()
        index = random.randint(0, len(param) - 1)
        values = [-1, 0, 1]
        values.remove(new_param[index])
        new_param[index] = random.choice(values)
        return new_param

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
                    print ("Score for trial", self.trial, "eval", self.repeat_count + 1, ":", self.score)
                    print(" ")
            

                    self.score_total += self.score

                # fin de chaque meilleur comportement rejoue
                if self.it_per_evaluation == 1000:
                   
                    print ("Fin meilleur comportement, cycle", self.replay_cycle)
                    print ("Score du cycle :", self.score)
                    print ("Meilleurs paramètres :", self.bestParam)
                    self.replay_cycle = self.replay_cycle + 1
                    print(" ")
                    print ("Rejouer meilleur comportement, cycle", self.replay_cycle)
                    

                self.score = 0.0
                self.iteration = 0

                # evaluations multiples pour un meme comportement
                if self.it_per_evaluation == 400:
                    self.repeat_count = self.repeat_count + 1
                    if self.repeat_count < self.repeats_per_eval:
                        print ("Rejouer meme comportement (eval", self.repeat_count + 1, "/",
                               self.repeats_per_eval, ")")
                        return 0, 0, True 

                    # fin des 3 evaluations
                    print(" ")
                    print ("Score total (trial", self.trial, "):", self.score_total)
                    print ("-----------------------------------------------")
                    

                    #si 1ere evaluation du parent apres 1ere 400 itérations
                    if self.parent_score is None:
                        # premiere evaluation: parent
                        self.parent_score = self.score_total
                        self.best_score = self.parent_score
                        self.bestParam = self.parent_param.copy()
                        self.best_trial = self.trial
                    else:
                        if self.evaluation_child:
                            # fin evaluation enfant -> comparaison
                            self.child_score = self.score_total
                            if self.child_score > self.parent_score:
                                self.parent_param = self.child_param.copy()
                                self.parent_score = self.child_score
                                print("Enfant meilleur devient parent")
                            else:
                                print("Parent reste le meme")
                            self.evaluation_child = False

                        # mise a jour du meilleur global sur le parent
                        if self.parent_score > self.best_score:
                            self.best_score = self.parent_score
                            self.bestParam = self.parent_param.copy()
                            self.best_trial = self.trial
                            print ("New best score :", self.best_score, "(trial", self.best_trial, ")")
                            print ("parameters :", self.bestParam)

                    self.score_total = 0.0
                    self.repeat_count = 0

#a la fin de 500 trails on rejoue le meilleur
                if self.trial == self.max_trials and self.it_per_evaluation == 400:
                    self.param = self.bestParam.copy()
                    self.it_per_evaluation = 1000
                    print ("------------FIN 500-----------")
                    print ("Budget epuise:", self.max_trials, "essais.")
                    print ("Meilleur score :", self.best_score, "(trial", self.best_trial, ")")
                    print ("Meilleurs paramètres :", self.bestParam)
                    self.replay_cycle = 1
                    print ("Rejouer meilleur comportement, cycle", self.replay_cycle)
                    print ("------------FIN 500------------")
                    self.trial = self.max_trials + 1
                    return 0, 0, True 
                
                # generation suivante on a un enfant mute du parent
                if self.it_per_evaluation == 400:
                    self.child_param = self.mutation(self.parent_param)
                    self.param = self.child_param.copy()
                    self.evaluation_child = True
                    self.trial = self.trial + 1
                    print ("-----------------------------------------------")
                    print ("Generation", self.trial, "-> evaluation enfant")
                    return 0, 0, True

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
