import random
import numpy as np
import matplotlib.pyplot as plt
import math
import webbrowser
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

material = {
    "black" : 0,
    "white" : 0,
}

def create_grid():
    arr = [["1" for _ in range(8)] for _ in range(8)] 
    return(arr)

def create_material_debt(materialDebt):
    mu, sigma = 20, 2
    s = np.random.normal(mu, sigma, 2)
    materialDebt["black"] = math.ceil(s[0])
    materialDebt["white"] = math.ceil(s[1])
    print("Material White: " + str(materialDebt["white"]))
    print("Material Black: " + str(materialDebt["black"]))
        
    # count, bins, ignored = plt.hist(s, 30, density=True)
    # plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
    #             np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
    #         linewidth=2, color='r')
    # plt.show()

    return materialDebt


def add_pieces_to_board(arr, materialDebt):
    add_king(arr)
    while materialDebt["black"] + materialDebt["white"] != 0:
        if(materialDebt["white"] > 0):
            availPieces = available_pieces(materialValue, materialDebt["white"])
            availPiecesWeighted = dict((k, piecesWeight[k]) for k in availPieces)
            piece = random.choices(list(availPiecesWeighted.keys()), list(availPiecesWeighted.values()))[0].upper()
            position = generate_white_position(arr, piece)
            arr[position[0]][position[1]] = piece
            materialDebt["white"] -= materialValue[piece]
        if(materialDebt["black"] > 0):
            availPieces = available_pieces(materialValue, materialDebt["black"])
            availPiecesWeighted = dict((k, piecesWeight[k]) for k in availPieces)
            piece = random.choices(list(availPiecesWeighted.keys()), list(availPiecesWeighted.values()))[0].lower()
            position = generate_black_position(arr, piece)
            arr[position[0]][position[1]] = piece
            materialDebt["black"] -= materialValue[piece]
    return arr

def available_pieces(dict, val) :
    return [i for i in dict if dict[i] <= val]

def piece_position_weights(piece = ''):
    weights = []
    for x in range(0, 8):
        weights.append(((x/3)**2) + 1)
    if piece.upper() == "P":
        weights[0] = 0
        weights[-1] = 0
    if piece.isupper(): return weights
    else: return weights[::-1]    

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

def add_king(arr):
    white_king_pos = generate_white_position(arr, piece = "K")
    arr[white_king_pos[0]][white_king_pos[1]] = "K"
    black_king_pos = generate_black_position(arr, piece = "k")
    while check_nearby_for_white_king(arr, black_king_pos[0], black_king_pos[1]) == False:
        black_king_pos = generate_black_position(arr, piece = "k")
    arr[black_king_pos[0]][black_king_pos[1]] = "k"

def turn_selection():
    if random.random() < 0.5 : return " w"
    else : return " b"

def castling(str):
    castling = ""
    if str[-1] == "R" and str [-4] == "K":
        castling += "K"
    if  str[-8] == "R" and str [-4] == "K":
        castling += "Q"
    if str[0] == "r" and str [4] == "k":
        castling += "K"
    if  str[7] == "r" and str [4] == "k":
        castling += "q"     
    if castling != "" : return " " + castling
    return castling 

def generate_FEN(arr):
    positionString = ""
    for row in range(len(arr[0])):
        for col in range(len(arr[1])):
            positionString += arr[row][col]
        if row != 7 :
            positionString += "/"
    return positionString

def generate_lichess_link(str, open=False):
    str = "https://lichess.org/analysis/fromPosition/"+fen_string
    print(str.replace(' ', "_"))
    if open :
        return webbrowser.open(str)

materialDebt = create_material_debt(material)
board = create_grid()
board = add_pieces_to_board(board, materialDebt)

fen_string = generate_FEN(board)
fen_string += turn_selection()
fen_string += castling(fen_string)

print(fen_string)
generate_lichess_link(fen_string, True)