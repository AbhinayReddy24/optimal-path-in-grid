import numpy as np
import random

class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' ']*9
        self.done = False
        self.winner = None
        return self.get_state()

    def get_state(self):
        # Generate all symmetrical boards and choose the canonical one
        boards = [
            self.board,
            self.board[::-1],  # Horizontal flip
            [self.board[i] for i in [2,5,8,1,4,7,0,3,6]],  # Rotate 90
            [self.board[i] for i in [8,7,6,5,4,3,2,1,0]],  # Rotate 180
            [self.board[i] for i in [6,3,0,7,4,1,8,5,2]],  # Rotate 270
            [self.board[i] for i in [2,1,0,5,4,3,8,7,6]],  # Vertical flip
            [self.board[i] for i in [0,3,6,1,4,7,2,5,8]],  # Diagonal flip
            [self.board[i] for i in [8,5,2,7,4,1,6,3,0]],  # Other diagonal flip
        ]
        canonical_board = min([''.join(b) for b in boards])
        return canonical_board

    def available_actions(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def step(self, action, player):
        if self.board[action] != ' ':
            raise ValueError("Invalid action!")
        self.board[action] = player
        self.check_winner(player)
        return self.get_state(), self.get_reward(player), self.done

    def check_winner(self, player):
        win_states = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]            # Diagonals
        ]
        for state in win_states:
            if all(self.board[i] == player for i in state):
                self.done = True
                self.winner = player
                return
        if ' ' not in self.board:
            self.done = True
            self.winner = 'Draw'

    def get_reward(self, player):
        if self.winner == player:
            return 1  # Win
        elif self.winner == 'Draw':
            return 0  # Draw
        elif self.winner is not None:
            return -1  # Loss
        else:
            return -0.01  # Small penalty for each move

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0):
        self.Q = {}  # State-action values
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate

    def get_Q(self, state, action):
        return self.Q.get((state, action), 0.0)

    def choose_action(self, env, state):
        actions = env.available_actions()
        if random.uniform(0,1) < self.epsilon:
            return random.choice(actions)
        qs = [self.get_Q(state, a) for a in actions]
        max_q = max(qs)
        max_actions = [a for a, q in zip(actions, qs) if q == max_q]
        return random.choice(max_actions)

    def learn(self, state, action, reward, next_state, done):
        q_current = self.get_Q(state, action)
        if done:
            q_target = reward
        else:
            # Get available actions from next_state directly
            next_actions = [i for i, spot in enumerate(next_state) if spot == ' ']
            q_next = max([self.get_Q(next_state, a) for a in next_actions], default=0)
            q_target = reward + self.gamma * q_next
        self.Q[(state, action)] = q_current + self.alpha * (q_target - q_current)

def train_agent(episodes=100000):
    agent = QLearningAgent()
    epsilon_decay = 0.99999  # Decay epsilon to reduce exploration over time
    min_epsilon = 0.1
    for _ in range(episodes):
        env = TicTacToeEnv()
        state = env.reset()
        done = False
        player = 'X'

        while not done:
            # Agent's move
            action = agent.choose_action(env, state)
            next_state, reward, done = env.step(action, player)
            agent.learn(state, action, reward, next_state, done)

            if done:
                break

            state = next_state

            # Opponent's move (random)
            opponent_actions = env.available_actions()
            if opponent_actions:
                opponent_action = random.choice(opponent_actions)
                next_state_op, reward_op, done = env.step(opponent_action, 'O')
                agent.learn(state, action, -reward_op, next_state_op, done)
                if done:
                    break
                state = next_state_op

        # Decay epsilon
        if agent.epsilon > min_epsilon:
            agent.epsilon *= epsilon_decay

    return agent

def print_board(board):
    display = [spot if spot != ' ' else str(idx) for idx, spot in enumerate(board)]
    print(f"{display[0]} | {display[1]} | {display[2]}")
    print("--+---+--")
    print(f"{display[3]} | {display[4]} | {display[5]}")
    print("--+---+--")
    print(f"{display[6]} | {display[7]} | {display[8]}")

def play_against_agent(agent):
    env = TicTacToeEnv()
    state = env.reset()
    done = False
    print("Welcome to Tic-Tac-Toe! You are 'O'.")
    print_board(env.board)
    while not done:
        # Agent's move
        action = agent.choose_action(env, state)
        state, reward, done = env.step(action, 'X')
        print("\nAgent's move:")
        print_board(env.board)
        if done:
            break

        # Player's move
        player_action = int(input("Your move (0-8): "))
        while player_action not in env.available_actions():
            player_action = int(input("Invalid move. Choose again (0-8): "))
        state, reward, done = env.step(player_action, 'O')
        print_board(env.board)

    if env.winner == 'O':
        print("You win!")
    elif env.winner == 'X':
        print("Agent wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    agent = train_agent()
    play_against_agent(agent)