from flask import Flask, request, jsonify
import pandas as pd
from prophet import Prophet
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/forecast', methods=['POST'])
def forecast():
    print("Received request at /forecast")
    data = request.json

    if not data or not isinstance(data, list):
        print("Invalid data format received.")
        return jsonify({"error": "Invalid data format. Expecting a JSON array."}), 400

    try:
        print("Received data:", data)
        df = pd.DataFrame(data)

        # Group data by event type and generate forecasts
        event_forecasts = []
        for event_type in df['event_type'].unique():
            event_data = df[df['event_type'] == event_type]
            event_df = event_data[['ds', 'y']]
            
            # Determine the latest date in the dataset
            latest_date = pd.to_datetime(event_df['ds']).max()
            print(f"Latest date for {event_type}: {latest_date}")
            next_month_start = (latest_date + pd.DateOffset(months=1)).replace(day=1)

            # Fit the model and make predictions
            model = Prophet()
            model.fit(event_df)

            future = model.make_future_dataframe(periods=60, freq='D')
            forecast = model.predict(future)

            # Filter forecast for the next month after the latest data
            next_month_end = (next_month_start + pd.DateOffset(months=1)) - pd.DateOffset(days=1)
            filtered_forecast = forecast[(forecast['ds'] >= next_month_start) & 
                                         (forecast['ds'] <= next_month_end)]

            # Sum up predictions per event type for the next month
            if not filtered_forecast.empty:
                forecast_sum = filtered_forecast['yhat'].sum()
                event_forecasts.append({
                    'ds': next_month_start.strftime('%Y-%m-%d'),
                    'yhat': forecast_sum,
                    'event_type': event_type  # Include event type
                })

        print("Forecast successful:", event_forecasts)
        return jsonify(event_forecasts)

    except Exception as e:
        print("Error processing forecast:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
