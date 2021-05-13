import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

style.use('ggplot')

#Temptation Payoff
T = 5
#Reward for Cooperating
R = 3
#Punishment Payoff
P = 1
#Suckers Payoff
S = 0

#Parameters for Reinforcement Learning
SIZE = 2
HM_EPISODE = 25000
epsilon = 0.5
EPS_DECAY = 0.9998
SHOW_EVERY = 3000
start_q_table = None # or filename if there is an existing qTable
LEARNING_RATE = 0.1
DISCOUNT = 0.95

#Define a Prisoner class where state 0 is Cooperate and state 1 is Defect
class Prisoner:
    def __init__(self, x = None):
        if x is None:
            self.x = np.random.randint(0,2)
        else:
            self.x = x
    def __str__(self):
        return f'{self.x}'
    def __eq__(self, other):
        if(self.x == 0 and other.x == 0):
            print(f'Nice you collaborated!')
        elif(self.x == 0 and other.x == 1):
            print(f'You have been betrayed!')
        elif(self.x == 1 and other.x == 0):
            print(f'You betrayed him!')
        elif(self.x == 1 and other.x == 1):
            print(f'You both betrayed eachother')
        return (self.x == other.x)
    def action(self, choice = 1):
        if choice == 0:
            #Cooperate
            self.x = 0
        elif choice == 1:
            #Betray
            self.x = 1
        pass
#Initialize a qTable with the size of 4x4x2 (State x State x Action)
if start_q_table is None:
    q_table = np.zeros(shape =(4,4,2))
else:
    with open(start_q_table,'rb') as f:
        q_table = pickle.load(f) 

#Initialize an empty eipsode_reward list
episode_rewards = []
#Instantiate two players
prisonerA = Prisoner()
prisonerB = Prisoner()  
#Loop for the number of episodes to do leearning
for episode in range(HM_EPISODE):  
    state = tuple([prisonerA.x , prisonerB.x])
    episode_reward = 0
    if ((episode == 0) or (np.random.random() <= epsilon)):
        action = np.random.randint(0,2)
    else:
        action = np.argmax(q_table[state])
    prisonerA.action(action)
    #prisonerA == prisonerB
    
    #Assuming PrisonerB is a random agent  
    prisonerB.action(np.random.randint(0,2))

    #Get new state
    new_state = tuple([prisonerA.x , prisonerB.x])
    print(new_state)
    #Get qValue of new state
    max_future_q = np.max(q_table[new_state])
    #Get qValue of current state
    current_q = q_table[state + (action,)]
    #Reward Calculation
    if(prisonerA.x == 0 and prisonerB.x == 0):
        reward = R
    elif(prisonerA.x == 0 and prisonerB.x == 1):
        reward = S
    elif(prisonerA.x == 1 and prisonerB.x == 0):
        reward = T
    elif(prisonerA.x == 1 and prisonerB.x == 1):
        reward = P
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
    #Assign new qValue to the qTable
    q_table[state + (action, )] = new_q
    #Update Epsilon 
    epsilon *= EPS_DECAY

print(q_table)
prisonerA == Prisoner(0)
    
# with open(f"qtable-{int(time.time())}.pickle","wb") as f:
#     pickle.dump(q_table,f)