from typing import List
from tabulate import tabulate

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


def get_move(player: str, board: List[List[str]]):
    print("Current board status in get move", board)
    print("Player ", player)
    row = int(input("Enter row: "))
    column = int(input("Enter column: "))
    return {"row": row, "column": column}


def self_play():
    next_player = 'X'
    next_position = (0, 0)


if __name__ == '__main__':
    # q_table()
    play_game(get_move)
