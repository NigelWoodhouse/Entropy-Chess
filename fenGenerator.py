import random

piecesDictionary = {
    "B": 2,
    "b": 2,
    "R": 2,
    "r": 2,
    "K": 2,
    "k": 2,
    "P": 8,
    "p": 8,
    "Q": 1,
    "q": 1,
    "K": 1,
    "k": 1,
    "1": 70,
}

def selectPiece():
    piece = random.choices(list(piecesDictionary.keys()), weights=(
    piecesDictionary.get("B"), 
    piecesDictionary.get("b"), 
    piecesDictionary.get("R"), 
    piecesDictionary.get("r"), 
    piecesDictionary.get("K"), 
    piecesDictionary.get("k"),
    piecesDictionary.get("P"), 
    piecesDictionary.get("p"), 
    piecesDictionary.get("Q"), 
    piecesDictionary.get("q"), 
    piecesDictionary.get("1"), 
    ), k=1)
    return piece[0]

def turn():
    if random.random() < 0.5 : return " w"
    else : return " b"

def castling(str):
    castling = " "
    if str[-1] == "R" and str [-4] == "K":
        castling += "K"
    if  str[-8] == "R" and str [-4] == "K":
        castling += "Q"
    if str[0] == "r" and str [4] == "k":
        castling += "K"
    if  str[7] == "r" and str [4] == "k":
        castling += "q"     
    if castling == "" : return " -"
    return castling 
    
def forceAddKing(str, king):
    if king == "k": 
        while king not in str:
            for index, place in enumerate(str):
                ran = random.random()
                if place == "1" and ran < (1/32):
                    str = str[:index] + king + str[index+1:]
                    break
    else: 
        while king not in str:
            for index, place in enumerate(reversed(str)):
                ran = random.random()
                if place == "1" and ran < (1/32):
                    index = len(str) - index - 1
                    str = str[:index] + king + str[index+1:]
                    break
    return str

fen_string=""

print(fen_string)
for row in range(8):
    for column in range(8):
        currentPiece = selectPiece()
        while (row == 0 and currentPiece.lower() == "p") or (row == 7 and currentPiece.lower() == "p"):
            currentPiece = selectPiece() 
        if ("K" in fen_string and currentPiece == "K") or ("k" in fen_string and currentPiece == "k"):
            currentPiece = "1"
        piecesDictionary[currentPiece] -= 1
        fen_string += currentPiece
    if row != 7 :
        fen_string += "/"

if "k" not in fen_string:
    fen_string = forceAddKing(fen_string, "k")
if "K" not in fen_string:
    fen_string = forceAddKing(fen_string, "K")      
fen_string += turn()
fen_string += castling(fen_string)

print(fen_string)