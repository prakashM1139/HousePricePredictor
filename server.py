import logging
import traceback

from flask import Flask, request, jsonify
import util
import warnings

app = Flask(__name__)


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    try:
        print(request.method)
        print(request.headers)
        print("enteredddd")
        if request.method == 'POST':
            # Check if Content-Type is 'application/json'
            # content_type = request.headers.get('Content-Type', '')
            if request.is_json:
                print("data is json")
                data = request.get_json()
                print("JSON Data:", data)
                total_sqft = float(data.get('total_sqft', 0))
                location = data.get('location', '')
                bhk = int(data.get('bhk', 0))
                bath = int(data.get('bath', 0))
            else:
                # Handle form data
                print("data is form")
                data = request.form
                print("Form Data:", data)
                total_sqft = float(data.get('total_sqft', 0))
                location = data.get('location', '')
                bhk = int(data.get('bhk', 0))
                bath = int(data.get('bath', 0))
        elif request.method == 'GET':
            logging.info("entering get")
            # Handle GET requests
            total_sqft = float(request.args.get('total_sqft'))
            location = request.args.get('location')
            bhk = int(request.args.get('bhk'))
            bath = int(request.args.get('bath'))
        else:
            # Unsupported request method
            return jsonify({'error': 'Unsupported request method'}), 400

        # Perform prediction
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        # Prepare response
        # Make the POST request with form data and headers
        # response = requests.post(url, data=form_data, headers=headers)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response
    except Exception as e:
        # Print the specific exception for debugging
        traceback.print_exc()
        return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    print("app.run -- started")
    app.run(debug=True)
