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
```
After clonning the git repo in local dev environment(
i)git init
ii)git clone https://github.com/belPDevs4/DNS_Zone_File_Analyser_V01h
)
```
1. Install dependencies:```(make sure you are inside the projet folder otherwise do cd folderpath)```
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

