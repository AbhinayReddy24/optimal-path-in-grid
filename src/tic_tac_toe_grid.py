from typing import Dict, Callable, List


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


def play_game(get_move: Callable[[str, List[List[str]]], Dict[str, int]]):
    board = tic_tac_toe_grid()
    i = 0
    while i < 9:
        winner = check_winner(board)
        if winner != None and winner != "Draw":
            print("Winner is: ", winner)
            return winner
        elif winner == "Draw":
            print("It's a draw")
            return "Draw"
        player = "X" if i % 2 == 0 else "O"
        move = get_move(player, board)
        row = move["row"]
        column = move["column"]
        if (row > 2 or column > 2) or (row < 0 or column < 0):
            print("Invalid input try again")
            return
        if board[row][column] != "-":
            print("position already taken")
        else:

            # play position
            if (i % 2 == 0):
                board[row][column] = "X"
            else:
                board[row][column] = "O"
            i += 1
        construct_grid(board)


if __name__ == "__main__":
    play_game()
