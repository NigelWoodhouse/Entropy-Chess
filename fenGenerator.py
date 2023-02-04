import random
import numpy as np
import matplotlib.pyplot as plt
import math
import webbrowser

# Likelyhood of selecting this piece
piecesWeight = {
    "B": 3,
    "b": 3,
    "R": 2,
    "r": 2,
    "N": 3,
    "n": 3,
    "P": 8,
    "p": 8,
    "Q": 1,
    "q": 1,
}

# Value of pieces
materialValue = {
    "B": 3,
    "b": 3,
    "R": 5,
    "r": 5,
    "N": 3,
    "n": 3,
    "P": 1,
    "p": 1,
    "Q": 9,
    "q": 9,
}

# Create 8x8 gird of 1's
def create_grid():
    arr = [["1" for _ in range(8)] for _ in range(8)] 
    return(arr)

def create_material_debt(display=False):
    # Initialize the amount of material each player has
    material = {
        "black" : 0,
        "white" : 0,
    }

    # Create Normal distribution for the amount of material each player gets
    mu, sigma = 20, 2
    s = np.random.normal(mu, sigma, 2)
    material["black"] = math.ceil(s[0])
    material["white"] = math.ceil(s[1])
    print("Material White: " + str(material["white"]))
    print("Material Black: " + str(material["black"]))
    
    # Show piece distribution curve
    if display == True:
        s = np.random.normal(mu, sigma, 500)
        count, bins, i = plt.hist(s, 30, density=True)
        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
                    np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
                linewidth=2, color='r')
        plt.show()
    return material

# Add pieces to board
def add_pieces_to_board(arr, material):
    # First add kings to the board
    add_king(arr)

    # Add pieces to the board until remaining material is 0 for both sides
    while material["black"] + material["white"] != 0:
        if(material["white"] > 0):
            availablePieces = available_pieces(materialValue, material["white"])
            availablePiecesWeighted = dict((k, piecesWeight[k]) for k in availablePieces)
            piece = random.choices(list(availablePiecesWeighted.keys()), list(availablePiecesWeighted.values()))[0].upper()
            position = generate_white_position(arr, piece)
            arr[position[0]][position[1]] = piece
            material["white"] -= materialValue[piece]
        if(material["black"] > 0):
            availablePieces = available_pieces(materialValue, material["black"])
            availablePiecesWeighted = dict((k, piecesWeight[k]) for k in availablePieces)
            piece = random.choices(list(availablePiecesWeighted.keys()), list(availablePiecesWeighted.values()))[0].lower()
            position = generate_black_position(arr, piece)
            arr[position[0]][position[1]] = piece
            material["black"] -= materialValue[piece]
    return arr

# Get all pieces whose material value is less than the reamining material debt of that player
def available_pieces(dict, val) :
    return [i for i in dict if dict[i] <= val]

# If piece is a king
def isKing(piece=''):
    if piece.upper() == "K": 
        return True
    else:
        return False

# Generate row weights for piece placement. Encourage pieces to be placed on your side of the board. 
# King is more encouraged to be on your side of the board in attempt to reduce forced mates and impossible positions.
# Prevent pawns from generating on the first and last ranks.
def piece_position_weights(piece = ''):
    weights = []
    # Encourage King to spawn on players side by changing division factor
    factor = (3, 1)[isKing(piece)]
    for x in range(0, 8):
        # Parabolic distribution curve for placing pieces
        weights.append(((x/factor)**2) + 1)
    # Prevent pawns from generating on first and last rank
    if piece.upper() == "P":
        weights[0] = 0
        weights[-1] = 0
    if piece.isupper(): return weights
    else: return weights[::-1]    

# Check 3x3 area around black king to see if white king is adjacent.
# Return true if kings are not adjacent
def check_nearby_for_white_king(arr, x, y):
    for dx in range(3):
        for dy in range(3):
            try:
                value = arr[dx-1+x][dy-1+y]
                if (value == "K"):
                    return False
            except:
                pass
    return True

def generate_white_position(arr, piece):
    row_weights = piece_position_weights(piece)
    column = random.randrange(0,8)
    row = random.choices(range(8), row_weights)[0]
    while arr[row][column] != "1":
        row = random.choices(range(8), row_weights)[0]
        column = random.randrange(0,8)
    return row, column

def generate_black_position(arr, piece):
    row_weights = piece_position_weights(piece)
    column = random.randrange(0,8)
    row = random.choices(range(8), row_weights)[0]
    while arr[row][column] != "1":
        row = random.choices(range(8), row_weights)[0]
        column = random.randrange(0,8)
    return row, column

# Add kings to board
# Add White king first. Add black king second and make sure it is not adjacent.
def add_king(arr):
    white_king_pos = generate_white_position(arr, piece = "K")
    arr[white_king_pos[0]][white_king_pos[1]] = "K"
    black_king_pos = generate_black_position(arr, piece = "k")
    while check_nearby_for_white_king(arr, black_king_pos[0], black_king_pos[1]) == False:
        black_king_pos = generate_black_position(arr, piece = "k")
    arr[black_king_pos[0]][black_king_pos[1]] = "k"

# Randomly determine side to start
def turn_selection():
    if random.random() < 0.5 : return " w"
    else : return " b"

# Check if castling is available
def castling(arr):
    castling = ""
    if ("K" in arr[-1] and "R" in arr[-1]):
        first_rank_string = ""
        for i in arr[-1]:
            if i == "K" or i == "R":
                first_rank_string += i
        if ("KR") in first_rank_string:
            castling += "K"
        if ("RK") in first_rank_string:
            castling += "Q"

    if ("k" in arr[0] and "r" in arr[0]):
        back_rank_string = ""
        for i in arr[0]:
            if i == "k" or i == "r":
                back_rank_string += i
        if ("kr") in back_rank_string:
            castling += "k"
        if ("rk") in back_rank_string:
            castling += "q"

    if castling != "" : return " " + castling
    return castling 

# Convert board 2D array to FEN string
def generate_FEN(arr):
    positionString = ""
    for row in range(len(arr[0])):
        for col in range(len(arr[1])):
            positionString += arr[row][col]
        if row != 7 :
            positionString += "/"
    return positionString

# Create a link to open board position in LiChess. Opens webpage automatically if open is set to True
def generate_lichess_link(str, open=False):
    lichessString = "https://lichess.org/analysis/fromPosition/"+str
    print(lichessString.replace(' ', "_"))
    if open :
        return webbrowser.open(lichessString)

def main():
    # Create amount of material per side
    material = create_material_debt()
    # Generate blank board
    board = create_grid()
    # Add piece to board
    board = add_pieces_to_board(board, material)

    # Convert 2D board array to string 
    fen_string = generate_FEN(board)
    # Add turn to FEN string
    fen_string += turn_selection()
    # Add castling to FEN string
    fen_string += castling(board)

    # Produce FEN string and LiChess link
    print(fen_string)
    generate_lichess_link(fen_string, True)

if __name__ == "__main__":
    main()