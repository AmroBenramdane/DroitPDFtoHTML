from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Cette ligne permet les requêtes CORS

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf = request.files['pdf']
    pdf_path = f'/tmp/{pdf.filename}'
    pdf.save(pdf_path)

    result = subprocess.run(['python', 'main.py', pdf_path], capture_output=True, text=True)

    if result.returncode == 0:
        html_path = pdf_path.replace('.pdf', '.html')
        if os.path.exists(html_path):
            html_filename = os.path.basename(html_path)
            return jsonify({'message': 'PDF processed successfully', 'html_url': f'/files/{html_filename}'})
        else:
            return jsonify({'error': 'HTML file not found'}), 500
    else:
        return jsonify({'error': 'PDF processing failed', 'details': result.stderr}), 400

@app.route('/files/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('/tmp', filename)

if __name__ == '__main__':
    app.run(debug=True)
