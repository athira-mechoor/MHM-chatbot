import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load dataset
def load_data():
    # Streamlit file uploader to allow the user to upload a CSV file
    uploaded_file = st.file_uploader("Upload your data file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        st.warning("Please upload a CSV file.")
        return None

# Preprocess the data
def preprocess_data(data):
    numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
    non_numeric_cols = data.select_dtypes(exclude=['float64', 'int64']).columns

    # Handle missing values for numeric columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

    # Handle missing values for non-numeric columns (fill with mode)
    data[non_numeric_cols] = data[non_numeric_cols].fillna(data[non_numeric_cols].mode().iloc[0])

    # Normalize numeric data
    scaler = StandardScaler()
    data[numeric_cols] = scaler.fit_transform(data[numeric_cols])

    return data

# Provide personalized suggestions based on user input
def provide_suggestions(user_input, data):
    suggestions = []

    # Diet suggestion
    if user_input['stress_level'] > 7:
        suggestions.append("Try consuming magnesium-rich foods like leafy greens, nuts, and seeds to reduce stress.")
    if user_input['exercise_frequency'] < 3:
        suggestions.append("Incorporate more physical activity to help balance your hormones.")

    # Sleep-related suggestion
    if user_input['sleep_hours'] < 7:
        suggestions.append("Aim to get at least 7-8 hours of sleep to maintain hormonal balance.")

    return suggestions

# Main function to create Streamlit app
def main():
    st.title("Menstrual Health Chatbot")

    # Load and preprocess data
    data = load_data()
    if data is not None:
        processed_data = preprocess_data(data)

        st.subheader("Tell me about your current situation:")

        # User inputs
        cycle_length = st.slider("Cycle Length (days)", 21, 35)
        bleeding_duration = st.slider("Bleeding Duration (days)", 1, 7)
        sleep_hours = st.slider("Sleep Hours per Night", 3, 12)
        stress_level = st.slider("Stress Level (1-10)", 1, 10)
        exercise_frequency = st.slider("Exercise Frequency per Week", 0, 7)

        # Create a dictionary of user inputs
        user_input = {
            'cycle_length': cycle_length,
            'bleeding_duration': bleeding_duration,
            'sleep_hours': sleep_hours,
            'stress_level': stress_level,
            'exercise_frequency': exercise_frequency
        }

        # Generate suggestions based on user input
        if st.button("Get Suggestions"):
            suggestions = provide_suggestions(user_input, processed_data)
            if suggestions:
                st.write("Here are some suggestions for you:")
                for suggestion in suggestions:
                    st.write("- " + suggestion)
            else:
                st.write("No specific suggestions at this time.")

if __name__ == "__main__":
    main()
