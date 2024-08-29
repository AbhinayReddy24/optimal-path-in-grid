from typing import Dict, Callable, List, Generator


def tic_tac_toe_grid():
    grid = [["-" for j in range(3)] for i in range(3)]
    return grid


def construct_grid(board):
    for i in range(len(board)):
        construct_string = ""
        for j in range(len(board[i])):
            construct_string += board[i][j] + " | "
        print(construct_string)
        if i < 2:
            print("-----------")


def check_winner(board):

    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != "-":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] != "-":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "-":
        return board[0][2]
    if "-" not in board[0] and "-" not in board[1] and "-" not in board[2]:
        return "Draw"
    return None


def play_game() -> Generator[str, Dict[str, int], str]:
    board = tic_tac_toe_grid()
    i = 0
    while i < 9:
        winner = check_winner(board)
        if winner != None and winner != "Draw":
            yield {"winner": winner, "board": board}
        elif winner == "Draw":
            yield {"winner": "Draw", "board": board}
        player = "X" if i % 2 == 0 else "O"
        move = yield {"player": player, "board": board}
        print("Move is: ", move)
        row = move["row"]
        column = move["column"]
        if (row > 2 or column > 2) or (row < 0 or column < 0):
            print("Invalid input try again")
            return
        if board[row][column] != "-":
            print("position already taken")
            return
        else:

            # play position
            if (i % 2 == 0):
                board[row][column] = "X"
            else:
                board[row][column] = "O"
            i += 1
        construct_grid(board)


if __name__ == "__main__":
    game = play_game()
    print(next(game))
    for i in range(3):
        for j in range(3):
            print(game.send({"row": i, "column": j}))
