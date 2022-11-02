from model_prediction import get_prediction
from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/predict", methods=['POST'])
def predict():
    if request.get_json() is not None:
        input_params = request.get_json()
        is_cancelled = int(get_prediction(input_params)[0])

        response = {
            'Cancelled': is_cancelled
        }

        return jsonify(response)

    return None

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
