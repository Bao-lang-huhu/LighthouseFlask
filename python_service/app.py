from flask import Flask, request, jsonify
import pandas as pd
from prophet import Prophet
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Home route to check if the Flask app is running
@app.route('/')
def home():
    return "Flask app is running!"

@app.route('/forecast', methods=['POST'])
def forecast():
    print("Received request at /forecast")
    data = request.json

    if not data or not isinstance(data, list):
        print("Invalid data format received.")
        return jsonify({"error": "Invalid data format. Expecting a JSON array."}), 400

    try:
        print("Received data:", data)  # Log the received data for debugging
        df = pd.DataFrame(data)[['ds', 'y']]
        model = Prophet()
        model.fit(df)

        future = model.make_future_dataframe(periods=60, freq='D')
        forecast = model.predict(future)

        filtered_forecast = forecast[(forecast['ds'] >= '2025-01-01') & (forecast['ds'] < '2025-02-01')]

        if not filtered_forecast.empty:
            print("Forecast successful:", filtered_forecast[['ds', 'yhat']])
            return jsonify(filtered_forecast[['ds', 'yhat']].to_dict(orient='records'))
        else:
            print("No forecast data available")
            return jsonify({"message": "No forecast data available"}), 404
    except Exception as e:
        print("Error processing forecast:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
