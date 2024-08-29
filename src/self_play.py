from typing import List, Dict
from tabulate import tabulate
from random import choice

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


def q_learning(state: Dict[str, int], current_q_value: int, game):
    alpha = 0.1
    gamma = 0.9
    reward = 0
    argmax_list = []
    list_of_available_states = []

    if game is None:
        game = play_game()
        game_status = next(game)
    else:
        game_status = game.send(
            {"row": state["row"], "column": state["column"]})

    board_status = game_status["board"]

    for i in range(len(board_status)):
        for j in range(len(board_status[i])):
            if board_status[i][j] == "-":
                if (i, j) != (state["row"], state["column"]):
                    list_of_available_states.append(
                        {"row": i, "column": j})
    if "winner" in game_status:
        winner = game_status["winner"]
        if winner == "Draw":
            reward = 2
        elif winner == "X":
            reward = 5
            
            return reward
        elif winner == "O":
            reward = -5
        list_of_available_states = []

    for available_state in list_of_available_states:
        print('its coming here')
        value_to_be_added = q_learning(
            state={"row": available_state["row"], "column": available_state["column"]}, current_q_value=0, game=game)
        argmax_list.append(value_to_be_added)
        # print("Argmax list", argmax_list)
        # print("len of argmax list", len(argmax_list))
    # q_value_for_being_in_state = current_q_value + alpha * \
    #     (reward + gamma * max(argmax_list) - current_q_value)

    # print("Q value for being in state", q_value_for_being_in_state)

    # if len(argmax_list) == 0:
    #     return q_value_for_being_in_state


def argmax(action, state):
    pass


def self_play():
    next_player = 'X'
    next_position = (0, 0)


if __name__ == '__main__':
    # q_table()
    q_learning({"row": 1, "column": 1}, 0, game=None)
