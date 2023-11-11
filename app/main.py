from flask import Flask, request, jsonify
import mlflow.pyfunc
import numpy as np

# model details
logged_model = "s3://t-airticket-bucket-v1/artifacts/1/d5fa30d062ae46b3bbead72bd526ec5b/artifacts/KNNEconomy_Exp"
loaded_model = mlflow.pyfunc.load_model(logged_model)

app = Flask(__name__)

# create a URL for the web API
@app.route("/api/v1", methods=['POST'])

def pred():
     # Get data from the POST request
    request_data = request.get_json()
    if 'features' in request_data:
        features = request_data["features"]
        # Need to convert the single data into an array and change the dimension
        prediction = loaded_model.predict(np.array(features).reshape(1, -1))

        # Output response
        resp = {
            'prediction': prediction[0],
            # For which model run
            'run_id': loaded_model.metadata.run_id,
            # Model unique ID
            'model_uuid': loaded_model.metadata.model_uuid,
            # Train date of the model
            'utc_time_created': loaded_model.metadata.utc_time_created,
        }

        # Return should be in JSON format and HTTP status code 200
        return jsonify(resp), 200
    else:
        return jsonify({'error': 'invalid data format or missing features'}), 400

# For web app health check
@app.route("/health", methods=['GET'])
def healthy():
    return jsonify({"message": "api active!"}), 200

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80)
