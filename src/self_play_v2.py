from typing import List, Dict
from tabulate import tabulate
import random
import sys

from tic_tac_toe_grid import play_game


def q_table():
    q_table = [[0 for i in range(10)] for j in range(10)]
    j = 0
    k = 0
    for first_position_each_row in range(1, len(q_table)):
        q_table[first_position_each_row][0] = (k, j)
        j += 1
        if first_position_each_row % 3 == 0:
            j = 0
            k += 1
    for column_headers in range(1, len(q_table[0])):
        if column_headers % 2 != 0:
            q_table[0][column_headers] = "X"
        else:
            q_table[0][column_headers] = "O"
    print(tabulate(q_table, tablefmt="grid"))


def epsilon_greedy():
    pass

# here the action is play at a particular position
# the state is all the available positions on the board

# agent would get +2 reward for the draw and +5 for the win -1 for the loss
# ghamma is 0.9 cause we value future reward
# alpha is 0.1 for the learning rate


sys.setrecursionlimit(10**5)

total_iterations = 0


def q_learning(list_of_available_states: List[Dict[str, int]],
               list_of_played_positions: List[Dict[str, int]],
               played_game_status,
               ):

    alpha = 0.1
    gamma = 0.9
    reward = 0
    global total_iterations
    total_iterations += 1  # Increment the global counter
    print("Total iterations:", total_iterations)

    if played_game_status is not None:
        if 'winner' in played_game_status:
            if played_game_status["winner"] == "Draw":
                print("Draw")
                return 2
            elif played_game_status["winner"] == "X":
                print("X wins")
                return 1
            elif played_game_status["winner"] == "O":
                print("O wins")
                return -1

    list_of_available_states = []
    for i in range(3):
        for j in range(3):
            list_of_available_states.append(
                {"row": i, "column": j})
    for played_position in list_of_played_positions:
        list_of_available_states.remove(played_position)

    random.shuffle(list_of_available_states)
    for available_state in list_of_available_states:
        new_game = play_game()
        played_game_status = next(new_game)

        # this stage is to set the environment already played states
        for played_position in list_of_played_positions:
            played_game_status = new_game.send(
                {"row": played_position["row"], "column": played_position["column"]})

        # this is where the real game starts
        played_game_status = new_game.send(
            {"row": available_state["row"], "column": available_state["column"]})

        list_of_new_played_positions = list_of_played_positions.copy()
        list_of_new_played_positions.append(
            {"row": available_state["row"], "column": available_state["column"]})
        list_of_new_unplayed_positions = list_of_available_states.copy()
        list_of_new_unplayed_positions.remove(available_state)

        reward = q_learning(list_of_new_unplayed_positions,
                            list_of_new_played_positions, played_game_status)
        print("Reward", reward, )
        # print("List of new played positions", list_of_new_played_positions)
        # print("List of new unplayed positions",
        #       list_of_new_unplayed_positions)


if __name__ == '__main__':
    # q_table()
    q_learning([], [],
               played_game_status=None)
