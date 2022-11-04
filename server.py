from model_prediction import get_prediction
from chart_prepare import month_wise, cluster_wise
from flask import Flask, request, jsonify
from waitress import serve
from flask_cors import CORS , cross_origin

app = Flask(__name__)
# cors =  CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, support_credentials=True)


@app.route("/predict", methods=['POST'])
# @cross_origin(origin='*')
def predict():
    if request.get_json() is not None:
        input_params = request.get_json()
        is_cancelled = int(get_prediction(input_params)[0])

        response = {
            'Cancelled': is_cancelled
        }

        return jsonify(response)

    return None


@app.route("/get-data", methods=['GET'])
# @cross_origin(origin='*')
def get_chart_data():

    if request is not None:

        month_wise_cancelled, month_wise_not_cancelled = month_wise()
        cluster_wise_cancelled, cluster_wise_not_cancelled = cluster_wise()

        response = {
            'month_wise_cancelled': month_wise_cancelled,
            'month_wise_not_cancelled': month_wise_not_cancelled,
            'cluster_wise_cancelled': cluster_wise_cancelled,
            'cluster_wise_not_cancelled': cluster_wise_not_cancelled
        }

        return jsonify(response)

    return None


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8080)
