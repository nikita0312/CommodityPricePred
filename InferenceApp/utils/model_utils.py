import numpy as np
import tensorflow as tf
from datetime import timedelta, datetime, date
import pandas as pd
from .date_features import calculate_year_features, generate_future_dates

PRICE_TRAINING_MEAN = 24.1731225  # Replace with your actual training mean
PRICE_TRAINING_STD = 13.758377640731982  # Replace with your actual training std


def preprocess(X):
    """Normalize price data using training statistics"""
    X[:, :, 0] = (X[:, :, 0] - PRICE_TRAINING_MEAN) / PRICE_TRAINING_STD
    return X


def prepare_input_sequence(prices, start_date):
    """
    Prepare input sequence with shape (1, 5, 3) where:
    - 1 is the batch size
    - 5 is the sequence length (timesteps)
    - 3 is the number of features [price, Year sin, Year cos]
    """
    # Create date range for the 5 days
    dates = pd.date_range(start=start_date, periods=5, freq="D")

    # Create DataFrame with date index
    sequence_df = pd.DataFrame(
        data={
            "Price": prices,
            "Year sin": [calculate_year_features(date)[0] for date in dates],
            "Year cos": [calculate_year_features(date)[1] for date in dates],
        },
        index=dates,
    )

    # Convert DataFrame to numpy array for model input
    feature_columns = ["Price", "Year sin", "Year cos"]
    sequence_array = sequence_df[feature_columns].values
    sequence_array = np.expand_dims(sequence_array, axis=0)  # Add batch dimension
    sequence_array = preprocess(sequence_array.copy())  # Preprocess input

    print(f"Input sequence shape: {sequence_array}")
    print("\nInput sequence DataFrame:")
    print(sequence_df)

    return sequence_array, sequence_df


def make_predictions(model, input_df, start_date):
    """
    Make 30-day predictions using the model.
    Input sequence shape: (1, 5, 3)
    """
    # Convert input_df to sequence array and preprocess
    feature_columns = ["Price", "Year sin", "Year cos"]
    current_sequence = input_df[feature_columns].values
    current_sequence = np.expand_dims(current_sequence, axis=0)
    current_pro_sequence = preprocess(current_sequence.copy())
    print(f"Current sequence first 5 rows: {current_sequence}")

    predictions = []

    # Create date range for predictions
    prediction_dates = pd.date_range(
        start=start_date + pd.Timedelta(days=5), periods=30, freq="D"
    )

    # Make predictions for 30 days
    for i in range(30):
        # Get prediction
        next_pred = model.predict(current_pro_sequence, verbose=0)[0][0]
        predictions.append(next_pred)  # Store actual prediction
        print(f"Predicted price for {prediction_dates[i]}: {next_pred}")

        # Calculate features for next timestep
        next_date = prediction_dates[i]
        year_sin, year_cos = calculate_year_features(next_date)

        # Create new sequence with the prediction
        new_sequence = np.concatenate(
            [
                current_sequence[:, 1:, :],  # Remove first timestep
                np.array([[[next_pred, year_sin, year_cos]]]),  # Add new timestep
            ],
            axis=1,
        )
        print(f"New sequence: {new_sequence}")
        # Preprocess the new sequence for next prediction
        current_pro_sequence = preprocess(new_sequence.copy())

    # Create predictions DataFrame
    predictions_df = pd.DataFrame(
        index=prediction_dates,
        data={
            "Predicted_Price": predictions,
            "Year sin": [calculate_year_features(date)[0] for date in prediction_dates],
            "Year cos": [calculate_year_features(date)[1] for date in prediction_dates],
        },
    )

    return predictions_df


def load_model(model_path):
    """Load the Keras model from the specified path."""
    try:
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully")
        print("Expected input shape: (batch_size, 5, 4)")
        print(f"Model input shape: {model.input_shape}")
        return model
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")
