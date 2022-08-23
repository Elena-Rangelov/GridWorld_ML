import sys
import numpy as np
import random



ROWS = 0
COLS = 0

REWARD = []
LAYOUT = []

STATE = (0,0)


WALLS = []
WIN = []
LOSS = []


def input():

    global ROWS, COLS, STATE, LAYOUT, REWARD, WALLS, WIN, LOSS


    COLS = int(sys.argv[1])
    ROWS = int(sys.argv[2])

    LAYOUT = [[0]*ROWS for i in range(COLS)]
    REWARD = [[0]*ROWS for i in range(COLS)]

    for i in range(0, int(sys.argv[3])*2, 2):
        WALLS += [(int(sys.argv[3+i+2]), int(sys.argv[3+i+1]))]
        n = i+6

    for i in range(1, int(sys.argv[n])*3, 3):
        if(int(sys.argv[n+i+2]) == 1):
            WIN += [(int(sys.argv[n+i+1]), int(sys.argv[n+i]))]
        else: LOSS += [(int(sys.argv[n+1+i]), int(sys.argv[n+i]))]


class Agent:

    def __init__(self):
        self.directions = [(1, 0),  # right
                           (0, 1),  # up
                           (-1, 0),  # left
                           (0, -1)]  # down

        self.exp_rate = 0.3
        self.curr = (0, 0)
        self.states = []
        self.neighbors = []
        self.lr = 0.2

        self.values = {}
        for i in range(ROWS):
            for j in range(COLS):
                self.values[(i, j)] = 0

    def neighbors(self, t, new_reward):
        global REWARD, WIN, LOSS, STATE

        i = t[0]
        j = t[1]
        self.neighbors = []

        if i + 1 < COLS and (i + 1, j) not in WALLS: self.neighbors += [(i+1, j)]
        #else: self.neighbors += [(i, j)]
        if i - 1 >= 0 and (i - 1, j) not in WALLS: self.neighbors += [(i - 1, j)]
        #else: self.neighbors += [(i, j)]
        if j + 1 < ROWS and (i, j + 1) not in WALLS: self.neighbors += [(i, j + 1)]
        #else: self.neighbors += [(i, j)]
        if j - 1 >= 0 and (i, j - 1) not in WALLS: self.neighbors += [(i, j - 1)]
        #else: self.neighbors += [(i, j)]

        return self.neighbors

    def try_action(self, dir):

        global REWARD, WIN, LOSS, STATE, COLS, ROWS

        if (self.curr[0] + self.directions[dir][0], self.curr[1] + self.directions[dir][1]) in self.neighbors:
                return REWARD[self.curr[0] + self.directions[dir][0]][self.curr[1] + self.directions[dir][1]]


    def choose_action(self):
        global REWARD, WIN, LOSS, STATE

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = random.randint(0, 3)
            #action = self.directions[a]
        else:
            nxt_reward = self.try_action(0)
            action = 0

            for d in range(len(self.directions)):
                if self.try_action(d):
                    if self.try_action(d) > nxt_reward:
                        nxt_reward = self.try_action(d)
                        action = d

        return action

    def take_action(self, action):
        return (self.curr[0] + self.directions[action][0], self.curr[1] + self.directions[action][1])

    def reset(self):
        self.states = []
        self.curr = (0, 0)
        self.neighbors = []

    def print_values(self):
        for i in range(0, ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, COLS):
                out += str(self.values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')



def is_done(agent):
    if agent.curr in WIN:
        return 1
    elif agent.curr in LOSS:
        return -1
    else: return 0


def cycle(agent=Agent(), rounds=50):
    i = 0
    while i < rounds:
        r = is_done(agent)
        if r == 0:
            action = agent.choose_action()
            agent.states.append(agent.take_action(action))
            agent.state = agent.take_action(action)
        else:
            reward = r
#            self.state_values[self.State.state] = reward  # this is optional
            print("Game End Reward", reward)
            for s in reversed(agent.states):
                reward = agent.values[s] + agent.lr * (reward - agent.values[s])
                agent.values[s] = round(reward, 3)
            agent.reset()
            i += 1


if __name__ == "__main__":
    input()
    ag = Agent()
    cycle(ag, 1)
    print(ag.print_values())