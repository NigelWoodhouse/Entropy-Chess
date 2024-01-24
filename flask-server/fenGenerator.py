# python -m flask --app .\entropyChessServer\fenGenerator.py  run

import random
import numpy as np
import matplotlib.pyplot as plt
import math
import webbrowser
from stockfish import Stockfish

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

def create_material_debt(whiteMaterial, blackMaterial, display=False):
    # Initialize the amount of material each player has
    material = {
        "black" : blackMaterial,
        "white" : whiteMaterial,
    }

    # Create Normal distribution for the amount of material each player gets
        # mu, sigma = 30, 2
        # s = np.random.normal(mu, sigma, 2)
        # material["black"] = abs(math.ceil(s[0]))
        # material["white"] = abs(math.ceil(s[1]))
        # print("Material White: " + str(material["white"]))
        # print("Material Black: " + str(material["black"]))
    
    # Show piece distribution curve
        # if display == True:
        #     s = np.random.normal(mu, sigma, 500)
        #     count, bins, i = plt.hist(s, 30, density=True)
        #     plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
        #                 np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
        #             linewidth=2, color='r')
        #     plt.show()
    return material

# Add pieces to board
def add_pieces_to_board(arr, material):
    # First add kings to the board
    add_king(arr)

    # Add pieces to the board until remaining material is 0 for both sides
    while material["black"] + material["white"] != 0:
        if(material["white"] > 0):
            add_piece(arr, material, "white")
        if(material["black"] > 0):
            add_piece(arr, material, "black")
    return arr

# Add single piece to board
def add_piece(arr, material, color):
    availablePieces = available_pieces(materialValue, material[color]) # Get available pieces based on remaining material for player
    availablePiecesWeighted = dict((k, piecesWeight[k]) for k in availablePieces) # Get subset of pieces from piecesWeight dictionary that are available based on remaining material for player
    piece = random.choices(list(availablePiecesWeighted.keys()), list(availablePiecesWeighted.values()))[0] # Choose piece based on weight
    if color == "white": piece = piece.upper() # Ensure piece is aligned with color
    else: piece = piece.lower()
    position = generate_position(arr, piece) # Get position to place piece
    arr[position[0]][position[1]] = piece # Add piece to board
    material[color] -= materialValue[piece] # Deduct material

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
    for x in range(8):
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

def generate_position(arr, piece):
    default = ""
    while default != "1":
        row_weights = piece_position_weights(piece)
        column = random.randrange(0,8)
        row = random.choices(range(8), row_weights)[0]
        default = arr[row][column]
    return row, column

# Add kings to board
# Add White king first. Add black king second and make sure it is not adjacent.
def add_king(arr):
    white_king_pos = generate_position(arr, piece = "K")
    arr[white_king_pos[0]][white_king_pos[1]] = "K"
    black_king_pos = generate_position(arr, piece = "k")
    while check_nearby_for_white_king(arr, black_king_pos[0], black_king_pos[1]) == False:
        black_king_pos = generate_position(arr, piece = "k")
    arr[black_king_pos[0]][black_king_pos[1]] = "k"

# Randomly determine side to start
def turn_selection(material):
    if material["black"] == 0: return " b"
    threshold = (material["white"]/material["black"])/2
    if random.random() > threshold : return " w"
    else : return " b"

# Check if castling is available (lichess is more forgiving)
# def castling(arr):
#     castling = ""
#     # Check white position
#     if ("K" in arr[-1] and "R" in arr[-1]):
#         first_rank_string = ""
#         for i in arr[-1]:
#             if i == "K" or i == "R":
#                 first_rank_string += i
#         if ("KR") in first_rank_string:
#             castling += "K"
#         if ("RK") in first_rank_string:
#             castling += "Q"

#     # Check black position
#     if ("k" in arr[0] and "r" in arr[0]):
#         back_rank_string = ""
#         for i in arr[0]:
#             if i == "k" or i == "r":
#                 back_rank_string += i
#         if ("kr") in back_rank_string:
#             castling += "k"
#         if ("rk") in back_rank_string:
#             castling += "q"

#     if castling != "" : return " " + castling
#     return castling 

# Check if castling is available (only starting location)
def castling(arr):
    castling = ""
    # Castling White
    # King side
    if arr[7][4] == "K" and arr[7][7] == "R":
        castling += "K"
    if arr[7][4] == "K" and arr[7][0] == "R":
        castling += "Q"
    if arr[0][4] == "K" and arr[0][7] == "R":
        castling += "k"
    if arr[0][4] == "K" and arr[0][0] == "R":
        castling += "q"
    if castling != "" : return " " + castling
    return " -"  

def move_count():
    return ' - 0 0'

# Convert board 2D array to FEN string
def generate_FEN(arr):
    positionString = ""
    for row in range(len(arr[0])):
        for col in range(len(arr[1])):
            positionString += arr[row][col]
        if row != 7 :
            positionString += "/"
    return positionString

def FEN_String_Cleanup(fen):
    # Initialize an empty result string
    result = ""
    # Initialize a counter variable to 1
    count = 1
    # Loop through the input string
    for i in range (len(fen)):
        # If the current character is '1' and the next character is also '1'
        if fen[i] == '1' and i < len(fen) - 1 and fen[i + 1] == '1':
            # Increment the counter by 1
            count += 1
        # Otherwise
        
        else:
        # If the counter is greater than 1
            if count > 1:
                # Append the counter to the result string
                result += str(count)
                # Reset the counter to 1
                count = 1
            else:
                # Append the current character to the result string
                result += fen[i]
    # Return the result string
    return result


# Get stockfish engine evaluation
def engineCheck(allowZeroEvaluation = True, allowForcedMate = True, engineEvaluationThreshold = 100, fen_string="rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"):
    stockfish = Stockfish(path=r"D:\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe", depth=18, parameters={"Threads": 2, "Minimum Thinking Time": 30})
    # Starting position
    if fen_string == '':
        return 0.3
    
    try:
        stockfish.set_fen_position(fen_position=fen_string)
        print(fen_string)
        if not stockfish.is_fen_valid(fen_string):
            print('INVALID BOARD POSITION')
            return -1
        engine = stockfish.get_evaluation()
    except:
        print('ISSUE WITH STOCKFISH')
        return -1
    
    print(engine)

    # Forced Mate Conditions
    if allowForcedMate == True and engine['type'] == 'mate':
        print('Forced mate. Allowing forced mate.')
        return abs(engine['value'])
    
    if allowForcedMate == False and engine['type'] == 'mate':
        print('FAILED POSITION. Position is forced mate and we deny forced mate.')
        return -1

    # Position is 0 eval but we do not want 0 eval
    if allowZeroEvaluation == False and engine['value'] == 0:
        print('FAILED POSITION. Position is 0 eval and we deny 0 eval.')
        return -1
    
    if engine['type'] == 'cp' and abs(engine['value']/100) > engineEvaluationThreshold:
        print('FAILED POSITION. Engine eval is outside of desired range')
        return -1

    if engine['type'] == 'cp' and abs(engine['value']/100) <= engineEvaluationThreshold:
        print('Valid position based on range')
        return abs(stockfish.get_evaluation()['value']/100)

    print('UNCAUGHT CASE!')
    return -1


# Create a link to open board position in LiChess. Opens webpage automatically if open is set to True
def generate_lichess_link(str, open=False):
    lichessString = "https://lichess.org/analysis/fromPosition/"+str
    print(lichessString.replace(' ', "_"))
    if open :
        return webbrowser.open(lichessString)

def main(whiteMaterial=39, blackMaterial=39, allowZeroEvaluation=True, allowForcedMate=True, engineEvaluationThreshold=100):
    
    engineEvaluation = -1
    fen_string = ''

    while engineEvaluation == -1:
        # Create amount of material per side
        material = create_material_debt(whiteMaterial, blackMaterial)
        #
        turn = turn_selection(material)

        # Generate blank board
        board = create_grid()
        # Add piece to board
        board = add_pieces_to_board(board, material)

        # Convert 2D board array to string 
        fen_string = generate_FEN(board)

        # Fen String cleanup - condensing 1's - for stockfish to verify valid FEN
        fen_string = FEN_String_Cleanup(fen_string)

        # Add turn to FEN string
        fen_string += turn
        # Add castling to FEN string
        fen_string += castling(board)

        fen_string += move_count()

        # Produce FEN string and LiChess link
        # print(fen_string)

        engineEvaluation = engineCheck(allowZeroEvaluation, allowForcedMate, engineEvaluationThreshold, fen_string)
        
        # generate_lichess_link(fen_string, True)
    return(fen_string)

if __name__ == "__main__":
    main()