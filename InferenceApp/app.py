import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.model_utils import load_model, prepare_input_sequence, make_predictions

model_path = "models/model_lstm_multi.keras"


def main():
    st.title("LSTM Price Predictor")
    st.write("Enter 5 consecutive daily price values to predict the next 30 days")

    try:
        model = load_model(model_path=model_path)
        st.success("Model loaded successfully!")

    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        prices = [
            col1.number_input(f"Price Day {i+1}", value=0.0, format="%f")
            for i in range(5)
        ]
        start_date = col2.date_input(
            "Start Date",
            datetime.now().date(),
            help="Select the date of the first price input",
        )
        submitted = st.form_submit_button("Make Prediction")

        if submitted:
            if len(prices) == 5 and all(p > 0 for p in prices):
                input_sequence, input_df = prepare_input_sequence(prices, start_date)
                predictions_df = make_predictions(model, input_df, start_date)

                st.subheader("Input Sequence")
                st.dataframe(input_df)

                st.subheader("Predictions for the next 30 days")
                st.dataframe(predictions_df)

                # Combine input and predictions for plotting
                combined_df = pd.concat(
                    [
                        input_df["Price"].to_frame("Actual_Price"),  # Changed this line
                        predictions_df["Predicted_Price"],
                    ]
                ).sort_index()

                st.line_chart(combined_df)

                csv = predictions_df.to_csv()
                st.download_button(
                    label="Download Predictions as CSV",
                    data=csv,
                    file_name="predictions.csv",
                    mime="text/csv",
                )

            else:
                st.warning("Please enter 5 non-zero positive price values.")


if __name__ == "__main__":
    main()
