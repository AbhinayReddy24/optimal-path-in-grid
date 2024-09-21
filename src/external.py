import numpy as np
import random

# Initialize the board and players
board = np.array([['-', '-', '-'],
                  ['-', '-', '-'],
                  ['-', '-', '-']])
players = ['X', 'O']
num_players = len(players)
Q = {}

# Hyperparameters
learning_rate = 0.001
discount_factor = 0.9
exploration_rate = 0.5
num_episodes = 1000


# Function to convert the board state to a string to use it as a key in the Q-table dictionary

def board_to_string(board):
    return ''.join(board.flatten())


def is_game_over(board):
    # Check rows for winning condition
    for row in board:
        if len(set(row)) == 1 and row[0] != '-':
            return True, row[0]

    # Check columns
    for col in board.T:
        if len(set(col)) == 1 and col[0] != '-':
            return True, col[0]

    # Check diagonals
    if len(set(board.diagonal())) == 1 and board[0, 0] != '-':
        return True, board[0, 0]
    if len(set(np.fliplr(board).diagonal())) == 1 and board[0, 2] != '-':
        return True, board[0, 2]

    # Check if the board is full
    if '-' not in board:
        return True, 'draw'

    return False, None

# Function to choose an action based on the Q-table


def choose_action(board, exploration_rate):
    state = board_to_string(board)

    # Exploration-exploitation trade-off
    if random.uniform(0, 1) < exploration_rate or state not in Q:
        # Choose a random action
        empty_cells = np.argwhere(board == '-')
        action = tuple(random.choice(empty_cells))
    else:
        # Choose the action with the highest Q-value
        q_values = Q[state]
        empty_cells = np.argwhere(board == '-')
        empty_q_values = [q_values[cell[0], cell[1]] for cell in empty_cells]
        max_q_value = max(empty_q_values)
        max_q_indices = [i for i in range(
            len(empty_cells)) if empty_q_values[i] == max_q_value]
        max_q_index = random.choice(max_q_indices)
        action = tuple(empty_cells[max_q_index])

    return action

# Function to get the next state of the board


def board_next_state(cell):
    next_state = board.copy()
    next_state[cell[0], cell[1]] = players[0]
    return next_state

# Function to update the Q-table


def update_q_table(state, action, next_state, reward):
    q_values = Q.get(state, np.zeros((3, 3)))

    # Calculate the maximum Q-value for the next state
    next_q_values = Q.get(board_to_string(next_state), np.zeros((3, 3)))
    max_next_q_value = np.max(next_q_values)
    # Q-learning update equation
    q_values[action[0], action[1]] += learning_rate * \
        (reward + discount_factor * max_next_q_value -
         q_values[action[0], action[1]])
    
    print('q_values', q_values)

    Q[state] = q_values


# Main Q-learning algorithm
agent_wins = 0
num_draws = 0

for episode in range(num_episodes):
    board = np.array([['-', '-', '-'],
                      ['-', '-', '-'],
                      ['-', '-', '-']])

    current_player = random.choice(players)
    game_over = False

    while not game_over:
        # Choose an action based on the current state
        action = choose_action(board, exploration_rate)

        # Make the chosen move
        row, col = action
        board[row, col] = current_player

        # Check if the game is over
        game_over, winner = is_game_over(board)

        if game_over:
            # Update the Q-table with the final reward
            if winner == current_player:
                reward = 1
                agent_wins += 1
            elif winner == 'draw':
                reward = 0.5
                num_draws += 1
            else:
                reward = 0
            update_q_table(board_to_string(board), action, board, reward)
        else:
            # Switch to the next player
            current_player = players[(players.index(
                current_player) + 1) % num_players]

        # Update the Q-table based on the immediate reward and the next state
        if not game_over:
            next_state = board_next_state(action)
            update_q_table(board_to_string(board), action, next_state, 0)

    # Decay the exploration rate
    exploration_rate *= 0.99

# Calculate and print the agent's win and draw percentages
num_games = num_episodes
agent_win_percentage = (agent_wins / num_games) * 100
draw_percentage = (num_draws / num_games) * 100

print("Agent win percentage: {:.2f}%".format(
    agent_win_percentage), 'number of games', num_games)
print("Draw percentage: {:.2f}%".format(draw_percentage))
