# Spice SSR Genomics Database

## Overview
A full-stack bioinformatics platform for SSR marker exploration across spice crops.

## Features
- 1.6M+ SSR markers
- Gene, trait, and phytochemical integration
- FastAPI backend
- Interactive web UI
- Motif analysis and visualization
- CSV export functionality

## Tech Stack
- MySQL (normalized schema)
- FastAPI (backend API)
- HTML + JS (frontend)
- Chart.js (visualization)

## API Endpoints
- /search
- /motif-analysis

## Run Locally

### Backend
pip install -r requirements.txt  
python -m uvicorn app:app --reload --port 8001  

### Frontend
python -m http.server 8080  

Open in browser:
http://127.0.0.1:8080/index.html

## Author
M.Pharm Pharmacology | BITS Pilani
