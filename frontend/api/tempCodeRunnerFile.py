# backend/app.py
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from urllib.parse import urlencode 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.app.ml.extraction import extract_from_url
from backend.app.ml.data_annotation.data_annotation import extract_semantic_fields
from backend.app.ml.inference import *

app = Flask(__name__)
CORS(app)

@app.route('/api/extract', methods=['POST'])
def extract_biology_info():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'message': 'URL is required'}), 400

        result = extract_from_url(url)

        if result is None:
            return jsonify({'message': 'Extraction failed'}), 500

        annotated_result = extract_semantic_fields(result)
        new_result = annotated_result
        params = urlencode(new_result)
        streamlit_url = f"http://localhost:8501?{params}"   

        return jsonify({"redirect_url": streamlit_url}), 200

    except Exception as e:
        logging.exception("Error occurred during extraction and annotation")
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


