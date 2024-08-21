def tic_tac_toe_grid():
    grid = [["-" for j in range(3)] for i in range(3) ]
    return grid

def construct_grid(board):
    for i in range (len(board)):
        construct_string = ""
        for j in range(len(board[i])):
            construct_string += board[i][j] + " | "
        print(construct_string)
        if i < 2:
            print("-----------")

def play_game(): 
    board = tic_tac_toe_grid()
    print("Player X turn:")
    x = (input("Enter row column: "))
    row = int(x.split(" ")[0])
    column = int(x.split(" ")[1])
    if (row > 2 or column > 2) or (row < 0 or column < 0):
        print("Invalid input try again")
        return
    board[row][column] = "X"
    construct_grid(board)

        

if __name__ == "__main__":
    # print(tic_tac_toe_grid())
    # construct_grid()
    play_game()