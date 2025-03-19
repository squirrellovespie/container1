import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()
    
    if not data or 'file' not in data or 'data' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    file_data = data['data']

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = f"/Alex_PV_dir/{file_name}"  # Replace "Alex" with your first name

    try:
        with open(file_path, 'w') as f:
            f.write(file_data)
        return jsonify({"file": file_name, "message": "Success."}), 200
    except Exception:
        return jsonify({"file": file_name, "error": "Error while storing the file to the storage."}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    if not data or 'file' not in data or 'product' not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_name = data['file']
    product = data['product']

    if not file_name:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    # Forward request to Container 2 via Kubernetes service
    response = requests.post(
        "http://container2-service:6001/calculate",
        json={"file": file_name, "product": product}
    )
    
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)