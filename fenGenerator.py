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

def createGrid():
    arr = [["1" for x in range(8)] for y in range(8)] 
    return(arr)

def createMaterialDebt(materialDebt):
    mu, sigma = 30, 2
    s = np.random.normal(mu, sigma, 2)
    materialDebt["black"] = math.ceil(s[0])
    materialDebt["white"] = math.ceil(s[1])
        
    # count, bins, ignored = plt.hist(s, 30, density=True)
    # plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
    #             np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
    #         linewidth=2, color='r')
    # plt.show()

    return materialDebt


def AddPiecesToBoard(arr, materialDebt):
    addKing(arr)
    while materialDebt["black"] != 0 and materialDebt["white"] != 0:
        if(materialDebt["white"] > 0):
            availPieces = availablePieces(materialValue, materialDebt["white"])
            availPiecesWeighted = dict((k, piecesWeight[k]) for k in availPieces)
            piece = random.choices(list(availPiecesWeighted.keys()), list(availPiecesWeighted.values()))[0].upper()
            position = (generatePosition(arr), generatePawnPosition(arr))[piece == "P"]
            arr[position[0]][position[1]] = piece
            materialDebt["white"] -= materialValue[piece]
        if(materialDebt["black"] > 0):
            availPieces = availablePieces(materialValue, materialDebt["black"])
            availPiecesWeighted = dict((k, piecesWeight[k]) for k in availPieces)
            piece = random.choices(list(availPiecesWeighted.keys()), list(availPiecesWeighted.values()))[0].lower()
            position = (generatePosition(arr), generatePawnPosition(arr))[piece == "p"]
            arr[position[0]][position[1]] = piece
            materialDebt["black"] -= materialValue[piece]
    return arr

def availablePieces(dict, val) :
    return [i for i in dict if dict[i] <= val]

def generatePawnPosition(arr):
    row = random.randrange(1,7)
    column = random.randrange(0,8)
    while arr[row][column] != "1":
        row = random.randrange(1,7)
        column = random.randrange(0,8)
    return row, column

def checkNearbyForWhiteKing(arr, x, y):
    for dx in range(3):
        for dy in range(3):
            try:
                value = arr[dx-1+x][dy-1+y]
                if (value == "K"):
                    return False
            except:
                pass
    return True

def generatePosition(arr):
    row = random.randrange(0,8)
    column = random.randrange(0,8)
    while arr[row][column] != "1":
        row = random.randrange(0,8)
        column = random.randrange(0,8)
    return row, column

def addKing(arr):
    white_king_pos = generatePosition(arr)
    arr[white_king_pos[0]][white_king_pos[1]] = "K"
    black_king_pos = generatePosition(arr)
    while checkNearbyForWhiteKing(arr, black_king_pos[0], black_king_pos[1]) == False:
        black_king_pos = generatePosition(arr)
    arr[black_king_pos[0]][black_king_pos[1]] = "k"

def turn():
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

def generateFEN(arr):
    positionString = ""
    for row in range(len(arr[0])):
        for col in range(len(arr[1])):
            positionString += arr[row][col]
        if row != 7 :
            positionString += "/"
    return positionString

def generateLichessLink(str, open=False):
    str = "https://lichess.org/analysis/fromPosition/"+fen_string
    print(str.replace(' ', "_"))
    return webbrowser.open(str)

materialDebt = createMaterialDebt(material)
board = createGrid()
board = AddPiecesToBoard(board, materialDebt)

fen_string = generateFEN(board)
fen_string += turn()
fen_string += castling(fen_string)

print(fen_string)
generateLichessLink(fen_string, True)