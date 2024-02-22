# From flask-server directory:
# python server.py


from flask import Flask
from flask import request
import fenGenerator

app = Flask(__name__)
@app.route("/members", methods=['POST', 'GET'])
def members():
    if request.method == 'GET':
        return {"members": ["Member1", "Member2", "Member3"]}
    if request.method == 'POST':
        print('Got post request')
        chess_data = request.get_json()
        blackMaterialValue = chess_data['blackMaterialValue']
        whiteMaterialValue = chess_data['whiteMaterialValue']
        evaluationThresholdValue = chess_data['evaluationThresholdValue']
        zeroEvaluationValue = chess_data['zeroEvaluationValue']
        forcedMateValue = chess_data['forcedMateValue']

        print(chess_data)
        
        chessPosition = fenGenerator.main(whiteMaterialValue, blackMaterialValue, zeroEvaluationValue, forcedMateValue, evaluationThresholdValue)

        return chessPosition

if __name__ == "__main__":
    app.run(debug = True)