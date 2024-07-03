from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf = request.files['pdf']
    pdf_path = f'/tmp/{pdf.filename}'
    pdf.save(pdf_path)

    print("jiji1")
    result = subprocess.run(['python', 'main.py', pdf_path], capture_output=True, text=True)

    if result.returncode == 0:
        html_path = pdf_path.replace('.pdf', '.html')
        if os.path.exists(html_path):
            return jsonify({'message': 'PDF processed successfully', 'html_path': html_path})
        else:
            return jsonify({'error': 'HTML file not found'}), 500
    else:
        return jsonify({'error': 'PDF processing failed', 'details': result.stderr}), 400

if __name__ == '__main__':
    app.run(debug=True)
