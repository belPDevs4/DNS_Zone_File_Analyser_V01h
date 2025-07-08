# DNS Zone Analyzer

This Flask web app analyzes DNS zone files and exports results to Excel.

## 📂 Project Structure
```
dns-zone-analyzer/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── index.html
│   ├── indextest.html
│   ├── results.html
├── uploads/                # XLSX version of uploaded files
├── README.md               # Project documentation
```

## 🚀 How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Open in browser: http://localhost:5000

## 📥 Upload
- Upload a zone file `.txt`
- Download results as Excel

