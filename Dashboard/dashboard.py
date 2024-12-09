import streamlit as st
import pandas as pd
import plotly.express as px
import os

folder_path = "download"


def get_csv_from_folder(folder_path):

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out the CSV files
    csv_files = [file for file in files if file.endswith(".csv")]

    # Check if there is exactly one CSV file
    if len(csv_files) == 0:
        raise FileNotFoundError("No CSV file found in the folder.")
    elif len(csv_files) > 1:
        raise Exception("Multiple CSV files found in the folder. Expected only one.")

    # Return the full path of the CSV file
    return os.path.join(folder_path, csv_files[0])


def run_dashboard():
    # Run the web scraper
    file = get_csv_from_folder(folder_path=folder_path)

    # Read the CSV file
    df = pd.read_csv(file, sep=",")

    st.subheader("Dataset")

    # Check if required columns exist (case-sensitive check)
    if "date" in df.columns and "value" in df.columns:
        st.write("Found required columns!")
        # Remove invalid rows and convert "date" to datetime
        df = df[
            df["date"].apply(lambda x: pd.to_datetime(x, errors="coerce")).notnull()
        ]
        df["date"] = pd.to_datetime(df["date"])

        # Add year and month columns for filtering purposes
        df["Year"] = df["date"].dt.year
        df["Month"] = df["date"].dt.month
        df["Day"] = df["date"].dt.day

        ### Year Filter ###
        unique_years = df["Year"].unique()
        selected_year = st.selectbox("Select Year", unique_years)

        # Filter dataset based on the selected year
        df_filtered = df[df["Year"] == selected_year]

        ### Month Filter ###
        unique_months = df_filtered["Month"].unique()
        selected_month = st.selectbox("Select Month", unique_months)

        # Filter dataset based on the selected month
        df_filtered = df_filtered[df_filtered["Month"] == selected_month]

        ### Date Range Filter ###
        st.subheader("Select Date Range")
        min_date = df_filtered["date"].min()
        max_date = df_filtered["date"].max()

        # Allow the user to select a custom date range
        date_range = st.date_input(
            "Select a date range",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date,
        )

        # Filter the dataset based on the selected date range
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered["date"] >= pd.to_datetime(start_date))
            & (df_filtered["date"] <= pd.to_datetime(end_date))
        ]

        # Display the filtered data
        st.subheader(f"Filtered Data from {start_date} to {end_date}")
        st.dataframe(df_filtered)

        ### Interactive Line Chart ###
        st.subheader("Interactive Line Chart")
        line_fig = px.line(
            df_filtered,
            x="date",
            y="value",
            title="Value Over Time",
            labels={"date": "Date", "value": "Value"},
            template="plotly_dark",  # Choose a theme: "plotly", "ggplot2", "seaborn", etc.
        )
        st.plotly_chart(line_fig)

        ### Interactive Bar Chart ###
        st.subheader("Interactive Bar Chart")
        bar_fig = px.bar(
            df_filtered,
            x="date",
            y="value",
            title="Value Distribution",
            labels={"date": "Date", "value": "Value"},
            color="value",  # Add color gradient
            color_continuous_scale="Viridis",  # Choose color scale
            template="plotly_dark",
        )
        st.plotly_chart(bar_fig)

        ### Interactive Scatter Plot ###
        st.subheader("Interactive Scatter Plot")
        scatter_fig = px.scatter(
            df_filtered,
            x="date",
            y="value",
            size="value",  # Use value as size of dots
            title="Scatter Plot of Value",
            labels={"date": "Date", "value": "Value"},
            color="value",
            color_continuous_scale="Plasma",
            template="plotly_dark",
        )
        st.plotly_chart(scatter_fig)

    else:
        st.error(
            f"Required columns (date, value) not found in the dataset. Available columns are: {df.columns.tolist()}"
        )

        # Try to handle case-insensitive column names
        columns_lower = [col.lower() for col in df.columns]
        if "date" in columns_lower and "value" in columns_lower:
            st.warning(
                "Columns found but with different capitalization. Renaming columns..."
            )
            # Create a mapping of current column names to desired column names
            column_mapping = {}
            for col in df.columns:
                if col.lower() == "date":
                    column_mapping[col] = "date"
                elif col.lower() == "value":
                    column_mapping[col] = "value"

            # Rename the columns
            df = df.rename(columns=column_mapping)
            st.write("Columns after renaming:", df.columns.tolist())

            # Now process the data with correct column names
            df["date"] = pd.to_datetime(df["date"])


if __name__ == "__main__":
    run_dashboard()
