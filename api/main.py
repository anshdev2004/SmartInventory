import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from pricing.combined_engine import generate_smart_markdown_sheet

app = FastAPI(title="SmartInventory API")


@app.get("/")
def root():
    return {"message": "SmartInventory API is running"}


@app.get("/markdowns")
def get_markdowns():
    sheet = generate_smart_markdown_sheet()
    return sheet.to_dict(orient="records")