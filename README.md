# SmartSoil
Simple Flask backend + static website for soil image analysis and fertilizer recommendation.

## Project Structure

- `app.py` – Flask API server
- `ImageExtraction.py` – Reads ESP32-CAM image data over serial and saves `captured_images/latest.jpg`
- `prediction/` – ML/data logic and CSV datasets
- `website/` – Static frontend files

## Requirements

- Python 3.10+
- pip

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Start API server:

```bash
python app.py
```

Continuously Capture images from ESP32-CAM:

```bash
python ImageExtraction.py
```

Server runs at `http://localhost:5000`.

## Main Endpoints

- `GET /analyze_soil`
- `GET /predict_soil`
- `POST /predict` (multipart form with `image`)
- `GET /captured_images/<filename>`