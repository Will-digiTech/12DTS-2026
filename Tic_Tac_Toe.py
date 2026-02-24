#VARIABLES
board = [["_", "_", "_"],
         ["_", "_", "_"],
         ["_", "_", "_"]
         ]
x_turn = True
end_game = False


#FUNCTIONS
# def clear_board():
#     board = [[],[],[]]

def print_board():
    for i in range(len(board)):
        row = board[i]
        print(" ".join(row))

def check_win():
    lines = []

    for row in board:
        lines.append(row)

    for i in range(len(board)):
        column_values = []
        for row in range(len(board)):
            column_values.append(board[row][i])
        lines.append(column_values)

    positive_diagonal = []
    negative_diagonal = []
    for i in range(len(board)):
        positive_diagonal.append(board[i][i])
        negative_diagonal.append(board[i][len(board) - 1 - i])
    lines.append(positive_diagonal)
    lines.append(negative_diagonal)

    for line in lines:
        if line.count(line[0]) == len(line) and "_" not in line:
            print("Game Over!")
            return True

    return False


def find_coordinate(x_turn, end_game):
    while end_game == False:
        try:
            row = int(input("Choose row: "))
            column = int(input("Choose column: "))

            coordinate = board[row - 1][column - 1]
            if coordinate == "_":
                pass
            else:
                print("Coordinate already chosen")
                continue


            if x_turn:
                coordinate = "X"
            else:
                coordinate = "O"

            board[row - 1][column - 1] = coordinate

            print_board()
            end_game = check_win()
            x_turn = not x_turn
        except IndexError:
            print("Not a valid coordinate")
        except ValueError:
            print("Choose a valid number")

def check_who_won(x_turn):
    print(x_turn)
    # if x_turn == True:
    #     print("X wins!")
    # else:
    #     print("O wins!")




#SCRIPT
# clear_board()
print_board()
find_coordinate(x_turn, end_game)
check_who_won(find_coordinate(x_turn, end_game))
print("Game Over!")
