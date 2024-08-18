from  grid import grid
import random

def something():


    #  kind of useless in this case cause we have very limited states
    intial_policy = [
        {'state': (2, 3), 'action': 'LEFT'},
        {'state': (2, 2), 'action': 'LEFT'},
        {'state': (2, 1), 'action': 'LEFT'},
        {'state': (2, 0), 'action': 'UP'},
        {'state': (1, 0), 'action': 'UP'},
        {'state': (0, 0), 'action': 'RIGHT'},
        {'state': (0, 1), 'action': 'RIGHT'},
        {'state': (0, 2), 'action': 'RIGHT'},
    ]

    values_for_grid = [[ 0 for _ in range (4)] for _ in range(3)]
    starting_state = (2, 3)
    final_value_grid = value_function(starting_state, values_for_grid)
    print('value function value' , final_value_grid)

def random_transition_probability_selector(transition_probabilities_of_state):

    probability_range_for_key = {}

    previous_value_end = 0
    for key, value in transition_probabilities_of_state.items():
        probability_range_for_key[key] = (previous_value_end, previous_value_end + value)
        previous_value_end = previous_value_end + value

    random_number = random.uniform(0, 1)

    for key, value in probability_range_for_key.items():
        if random_number > value[0] and random_number <= value[1]:
            return key, value[1]

def next_step_to_take(key, current_state):
    if key == 'T_left':
        future_state = (current_state[0], current_state[1] -1)
    elif key == 'T_right':
        future_state = (current_state[0], current_state[1] +1)
    elif key == 'T_up':
        future_state = (current_state[0] -1, current_state[1])
    else:
        future_state = (current_state[0] +1, current_state[1])
    if is_valid_state(future_state):
        return future_state
    else:
        return current_state

def is_valid_state(state):
    if state[0] < 0 or state[0] > 2 or state[1] < 0 or state[1] > 3 or (state[0] == 1 and state[1] == 1):
        return False
    return True

def value_function(state: tuple[int, int], values_for_grid):
    
    value = 0
    grid_data = grid()
    reward = grid_data[state[0]][state[1]]['reward']
    if (grid_data[state[0]][state[1]].get('transition_probability') is not None):
        transition_probabilities = grid_data[state[0]][state[1]]['transition_probability']
        randomly_chosen_probability = random_transition_probability_selector(transition_probabilities)
        next_move = randomly_chosen_probability[0]

        next_state = next_step_to_take(next_move, state)
        print(next_state)
    
        next_state_value_function = value_function(next_state, values_for_grid)
        for probability in transition_probabilities.values():
                value += probability *(0.6 * next_state_value_function)
        value += reward
    else:
        value = reward
    values_for_grid[state[0]][state[1]] = value.__round__(4)
    print(values_for_grid)
    return value
if __name__ == '__main__':
   returnd_value =  something()
