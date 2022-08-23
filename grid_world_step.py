import sys
import numpy as np



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


def neighbors(t, new_reward):
    global REWARD, WIN, LOSS, STATE

    i = t[0]
    j = t[1]
    n = []

    if i + 1 < COLS and (i + 1, j) not in WALLS: n += [(i+1, j)]
    else: n += [(i, j)]
    if i - 1 >= 0 and (i - 1, j) not in WALLS: n += [(i - 1, j)]
    else: n += [(i, j)]
    if j + 1 < ROWS and (i, j + 1) not in WALLS: n += [(i, j + 1)]
    else: n += [(i, j)]
    if j - 1 >= 0 and (i, j - 1) not in WALLS: n += [(i, j - 1)]
    else: n += [(i, j)]

    return n


def cycle(n=1):

    global ROWS, COLS, STATE, LAYOUT, REWARD, WALLS, WIN, LOSS

    for n1 in range(n):
        new_reward = [[0]*ROWS for i in range(COLS)]

        for j in range(ROWS):
            for i in range(COLS):
                if (i, j) not in WALLS and (i, j) not in LOSS and (i, j) not in WIN:
                    for n in neighbors((i, j), new_reward):
                        k = n[0]
                        l = n[1]
                        if n in WIN:
                            new_reward[i][j] += 1.0
                        elif n in LOSS:
                            new_reward[i][j] += -1.0
                        else:
                            new_reward[i][j] += REWARD[k][l] * 0.9
                    new_reward[i][j] *= .25
                elif (i, j) in WALLS:
                    new_reward[i][j] = "----"
                elif (i, j) in WIN:
                    new_reward[i][j] = 1.0
                elif (i, j) in LOSS:
                    new_reward[i][j] = -1.0
        REWARD = new_reward

    return new_reward

def display_board(board):
    for j in range(ROWS):
        d = ""
        for i in range(COLS):
            if board[i][j] != "----":
                print("{:.2f}".format(board[i][j]), end=" ")
            else:
                print(board[i][j], end=" ")
        print(d, "\n")


# p = []

# for j in range(ROWS):
#     p.append([])
#     for k in range(COLS):
#         p[-1].append([0.25, 0.25, 0.25, 0.25])
        # 0 up  1 down  2 left  3 right



if __name__ == "__main__":
    input()
    board = cycle()
    display_board(board)

