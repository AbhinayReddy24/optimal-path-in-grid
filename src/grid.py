def grid():
    grid = [[ 0 for _ in range (4)] for _ in range(3)]

    grid[0][0] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.8,
        "T_left": 0.1,
        "T_up": 0.1
        },
    }
    grid[0][1] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.8,
        "T_left": 0.1,
        "T_up": 0.1
        }
    }
    grid[0][2] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.8,
        "T_down": 0.1,
        "T_up": 0.1
        }
    }
    grid[0][3] = {
        "reward": 10,
    }
    grid[1][0] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.1,
        "T_up": 0.8
        }
    }
    grid[1][1] = "#"
    grid[1][2] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.4,
        "T_up": 0.5
        }
    }
    grid[1][3] = {
        "reward": -10,
    }
    grid[2][0] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.1,
        "T_up": 0.8
        }
    }
    grid[2][1] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.8,
        "T_up": 0.1
        }
    }
    grid[2][2] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.8,
        "T_up": 0.1
        }
    }
    grid[2][3] = {
        "reward": 0,
        "transition_probability": {
        "T_right": 0.1,
        "T_left": 0.8,
        "T_up": 0.1
        }
    }

    return grid

if __name__ == '__main__':
    grid = grid()
    print(grid)