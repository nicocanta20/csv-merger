# CSV Merger

Upload several CSV files and download them as a single Excel file, with one
sheet per CSV.

## How it works
- Detects each file's delimiter automatically (comma, tab, semicolon, pipe,
  or space), so files exported from different tools can be mixed.
- Skips empty files and reports which ones could not be processed.

## Run locally
```bash
pip install -r requirements.txt
streamlit run main.py
```

## Stack
Python · Streamlit · pandas · openpyxl

Built in August 2023 with [Florian Reyes](https://github.com/florianreyes) and
[Julian Fischman](https://github.com/JulianFischman).
