
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
import os
import pandas as pd
import socket
import requests
import re

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your-secret-key-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return "Unresolvable"

def get_whois_expiry(domain):
    try:
        url = f"https://who.is/whois/{domain}"
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return "Lookup failed"
        for line in resp.text.splitlines():
            if "Expires" in line or "Expiry Date" in line:
                match = re.search(r'(\d{4}-\d{2}-\d{2})', line)
                if match:
                    return match.group(1)
        return "Not found"
    except Exception:
        return "Error"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Parse zone file
            records = []
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith(';'):
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            records.append({
                                'name': parts[0],
                                'ttl': parts[1],
                                'type': parts[2],
                                'value': ' '.join(parts[3:]),
                                'resolved_ip': resolve_ip(parts[-1]),
                                'whois_expiry': get_whois_expiry(parts[-1])
                            })

            # Export to Excel
            excel_filename = filename.rsplit('.', 1)[0] + '.xlsx'
            excel_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)
            df = pd.DataFrame(records)
            df.to_excel(excel_path, index=False)

            # Clean up uploaded txt file
            os.remove(file_path)

            return render_template('results.html',
                                   records=records,
                                   excel_filename=excel_filename)
        except Exception as e:
            flash(f'Error analyzing zone file: {str(e)}')
            return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_excel(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('Excel file not found')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
