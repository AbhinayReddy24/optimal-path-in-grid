from typing import List, Dict, Tuple
from tabulate import tabulate
import random
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
    return q_table


def epsilon_greedy(
        q_table,
        list_of_available_states,
        epsilon,
):
    possible_states_q_value_pairs = []
    current_action_number = 9 - len(list_of_available_states) + 1
    list_of_available_states = [(available_state['row'], available_state['column'])
                                for available_state in list_of_available_states]
    for i in range(1, len(q_table)):
        for j in range(1, current_action_number + 1):
            if q_table[i][0] in list_of_available_states:
                possible_states_q_value_pairs.append(
                    {
                        "state": q_table[i][0],
                        "q_value": q_table[i][j]
                    }
                )

    random_value = round(random.uniform(0, 1), 2)
    possible_state_to_play = ()
    if random_value <= epsilon:
        possible_state_to_play = random.choice(list_of_available_states)

    else:
        max_q_value_dict = max(
            possible_states_q_value_pairs,
            key=lambda x: x['q_value']
        )
        possible_state_to_play = max_q_value_dict['state']

    return {
        "row": possible_state_to_play[0],
        "column": possible_state_to_play[1]
    }

# here the action is to play at a particular position so you can pretty much neglect the action
# the state is all the available positions on the board

# agent would get +1 reward for the draw and +5 for the win -1 for the loss
# gamma is 0.9 cause we value future reward
# alpha is 0.1 for the learning rate

# POTENTIAL IMPROVEMENTS
# 1. Right now epsilon greedy alogrithm chooses the max value or random value
#    we can also add a feature to choose the second best value or the third
#    best value every once in a while


def retrieve_q_value_and_position(
        state: Dict[str, int],
        number_of_played_positions: int,
        q_table
):

    value_row_postion = 0

    for i in range(0, len(q_table)):
        if q_table[i+1][0] == (state['row'], state['column']):
            value_row_postion = i + 1
            break
    return q_table[value_row_postion][number_of_played_positions], {
        'row': value_row_postion, 'column': number_of_played_positions
    }


def retrieve_q_values_for_current_action(
    number_of_played_positions: int,
        list_of_played_positions: List[Tuple[int, int]],
        q_table,
        next_state_for_opponent,
        future_sate_for_current_action
):
    q_values = []
    if number_of_played_positions >= 9:
        return 0
    for i in range(1, len(q_table)):
        if q_table[i][0] not in list_of_played_positions:
            if q_table[i][0] != (next_state_for_opponent['row'], next_state_for_opponent['column']):
                if q_table[i][0] == (future_sate_for_current_action['row'], future_sate_for_current_action['column']):
                    max_q_value = q_table[i][number_of_played_positions]
            # q_values.append(q_table[i][number_of_played_positions])
    return max_q_value


x_win_rate = 0


def q_learning(
        list_of_available_states: List[Dict[str, int]],
        q_table_to_update,
        epsilon,
        iterations
):
    alpha = 0.5
    gamma = 1
    reward = 0
    column_position_on_q_table = 0
    list_of_played_positions = []
    list_of_available_states_copy = []
    global x_win_rate
    done = False
    list_of_states_to_play = []

    new_game = play_game()
    played_game_status = next(new_game)

    list_of_available_states_copy = list_of_available_states.copy()
    random.shuffle(list_of_available_states_copy)
    for i in range(len(list_of_available_states_copy)):
        state_to_play = epsilon_greedy(
            q_table=q_table_to_update,
            list_of_available_states=list_of_available_states_copy,
            epsilon=epsilon
        )
        list_of_available_states_copy.remove(state_to_play)
        list_of_states_to_play.append(state_to_play)

    while not done:
        play_sate = list_of_states_to_play[0]
        list_of_states_to_play.remove(play_sate)

        played_game_status = new_game.send(play_sate)

        column_position_on_q_table += 1

        list_of_played_positions.append(
            (play_sate['row'], play_sate['column']))

        if "winner" in played_game_status:
            if played_game_status["winner"] == "Draw":
                reward = 0
            else:
                reward = 2

            if played_game_status["winner"] == "X":
                x_win_rate += 1

            print("X win rate", (x_win_rate/iterations)
                  * 100, "%", "iteration", iterations)

        retrieved_position_and_q_value = retrieve_q_value_and_position(
            state=play_sate,
            number_of_played_positions=column_position_on_q_table,
            q_table=q_table_to_update,
        )

        current_q_value = retrieved_position_and_q_value[0]
        position_to_update_on_q_table = retrieved_position_and_q_value[1]

        if 'winner' in played_game_status:
            max_q_value = 0
            done = True
        else:
            next_state_for_opponent = list_of_states_to_play[0]
            if len(list_of_states_to_play) > 1:
                future_sate_for_current_action = list_of_states_to_play[1]
            else:
                future_sate_for_current_action = []
            max_q_value = retrieve_q_values_for_current_action(
                number_of_played_positions=len(
                    list_of_played_positions)+2,
                list_of_played_positions=list_of_played_positions,
                q_table=q_table_to_update,
                next_state_for_opponent=next_state_for_opponent,
                future_sate_for_current_action=future_sate_for_current_action
            )
        q_value = current_q_value + alpha * \
            (reward + gamma * max_q_value - current_q_value)
        q_table_to_update[position_to_update_on_q_table['row']
                          ][position_to_update_on_q_table['column']] = round(q_value, 6)

        with open('q_table.json', 'w') as f:
            json.dump(q_table_to_update, f)
        if done:
            break

    print(tabulate(q_table_to_update, tablefmt="grid"))


if __name__ == '__main__':

    # To make a new q_table uncomment the code below
    # and comment the code below it
    q_table_to_update_new = q_table_initialization()

    with open('q_table.json', 'w') as f:
        json.dump(q_table_to_update_new, f)

    with open('q_table.json', 'r') as f:
        q_table_to_update = json.load(f)

    for row in q_table_to_update:
        if isinstance(row[0], list):
            row[0] = tuple(row[0])

    list_of_available_states = [
        {"row": 0, "column": 0},
        {"row": 0, "column": 1},
        {"row": 0, "column": 2},
        {"row": 1, "column": 0},
        {"row": 1, "column": 1},
        {"row": 1, "column": 2},
        {"row": 2, "column": 0},
        {"row": 2, "column": 1},
        {"row": 2, "column": 2}
    ]
    epsilon = 0.9
    iterations = 1000

    final_epsilon = 0.3
    decay_rate = (epsilon - final_epsilon) / iterations

    for i in range(iterations):
        print("iteration", i, "epsilon", epsilon)
        q_learning(
            q_table_to_update=q_table_to_update,
            list_of_available_states=list_of_available_states,
            epsilon=epsilon,
            iterations=iterations
        )
        epsilon = max(final_epsilon, epsilon - decay_rate)
