# LSTM Price Predictor

This Streamlit application provides price predictions using an LSTM model. The model takes 5 consecutive daily price values and predicts prices for the next 30 days.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Place your trained LSTM model file (`model.keras`) in the root directory.

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Features

- Input 5 consecutive daily price values
- Select start date for the prediction sequence
- Displays predictions for the next 30 days in both table and chart format
- Download predictions as CSV
- Automatic calculation of year sin and cos features

## Project Structure

- `app.py`: Main Streamlit application
- `utils/`:
  - `date_features.py`: Date-related feature calculations
  - `model_utils.py`: Model loading and prediction functions
- `requirements.txt`: Project dependencies
- `model.keras`: Your trained LSTM model (not included)