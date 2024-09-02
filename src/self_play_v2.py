from typing import List, Dict
from tabulate import tabulate
import random
import sys
import json

from tic_tac_toe_grid import play_game


def q_table_initialization():
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
    # print(tabulate(q_table, tablefmt="grid"))
    return q_table


def epsilon_greedy():
    pass

# here the action is to play at a particular position so you can pretty much neglect the action
# the state is all the available positions on the board

# agent would get +1 reward for the draw and +5 for the win -1 for the loss
# gamma is 0.9 cause we value future reward
# alpha is 0.1 for the learning rate


sys.setrecursionlimit(10**5)


def retrieve_q_value_and_position(state: Dict[str, int], number_of_played_positions: int):
    q_table = q_table_initialization()
    value_row_postion = 0

    for i in range(0, len(q_table)):
        if q_table[i+1][0] == (state['row'], state['column']):
            value_row_postion = i + 1
            break

    return q_table[value_row_postion][number_of_played_positions + 1], {
        'row': value_row_postion, 'column': number_of_played_positions + 1
    }


total_iterations = 0


def q_learning(list_of_available_states: List[Dict[str, int]],
               list_of_played_positions: List[Dict[str, int]],
               played_game_status,
               q_table_to_update,
               ):

    alpha = 0.1
    gamma = 0.9
    reward = 0
    # arg_max_list = []
    global total_iterations
    total_iterations += 1  # Increment the global counter
    print("Total iterations:", total_iterations)
    print('PLAYED GAME STATUS', played_game_status)

    if played_game_status is not None:
        if 'winner' in played_game_status:
            if played_game_status["winner"] == "Draw":
                print("Draw")
                return {"reward": 1, "winner_status": "Draw"}
            elif played_game_status["winner"] == "X":
                print("X wins")
                return {"reward": 5, "winner_status": "X"}
            elif played_game_status["winner"] == "O":
                print("O wins")
                return {"reward": -1, "winner_status": "O"}

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

        retrieved_position_and_q_value = retrieve_q_value_and_position(
            {"row": available_state["row"],
                "column": available_state["column"]},
            number_of_played_positions=len(list_of_played_positions)
        )
        current_q_value = retrieved_position_and_q_value[0]
        position_to_update_on_q_table = retrieved_position_and_q_value[1]

        next_state_q_values = q_learning(list_of_new_unplayed_positions,
                                         list_of_new_played_positions, played_game_status, q_table_to_update)

        if next_state_q_values is None:
            continue
        if isinstance(next_state_q_values, dict) and 'reward' in next_state_q_values:
            reward = next_state_q_values['reward']
            winner_staus = next_state_q_values['winner_status']

            q_value = current_q_value + alpha * \
                (reward + gamma * 0 - current_q_value)
            arg_max_list = []
            arg_max_list.append(round(q_value, 6))
        else:
            reward = 0
            arg_max_list = next_state_q_values
            print('ARg max list', arg_max_list)
            q_value = current_q_value + alpha * \
                (reward + gamma * max(arg_max_list) - current_q_value)

        print("Q VALUE", q_value)
        arg_max_list.append(round(q_value, 6))

        q_table_to_update[position_to_update_on_q_table['row']
                          ][position_to_update_on_q_table['column']] = round(q_value, 6)
        with open('q_table.json', 'w') as f:
            json.dump(q_table_to_update, f)

        print('updated q table', tabulate(q_table_to_update, tablefmt="grid"))

    return arg_max_list


if __name__ == '__main__':
    q_table_to_update = q_table_initialization()
    q_learning(list_of_available_states=[], list_of_played_positions=[
        # {'row': 1, 'column': 1},
        # {'row': 0, 'column': 1},
        # {'row': 2, 'column': 0},
        # {'row': 0, 'column': 2},
        # {'row': 0, 'column': 0},
        # {'row': 2, 'column': 2},
        # {'row': 1, 'column': 2},
    ],
        played_game_status=None,
        q_table_to_update=q_table_to_update)
