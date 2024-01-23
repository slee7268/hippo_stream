import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data
def load_data(filename='sample.json'):
    with open(filename) as f:
        data = json.load(f)
    return data

# Function to transform JSON data into a DataFrame
# Function to transform JSON data into a DataFrame and parse dates
def transform_data(data):
    records = []
    for entry in data:
        record = {
            'Date': pd.to_datetime(entry['date'], format='%m/%d'), # Adjust the format as per your data
            'Run Name': entry['run_name'],
            **entry['results']
        }
        records.append(record)
    df = pd.DataFrame(records)
    # Sort by Date to ensure the plot follows chronological order
    df.sort_values(by='Date', inplace=True)
    return df

# Main app
def main():
    st.title('Model Performance Visualization')

    # Load and transform data
    data = load_data()
    df = transform_data(data)

    st.write("### Raw Data", df)

    # Visualization
    st.write("### Accuracy Over Time")
    fig, ax = plt.subplots()
    for name, group in df.groupby('Run Name'):
        ax.scatter(group['Date'], group['overall_acc'], label=name, s=100)  # s is the size of the point
    ax.set_xlabel('Date')
    ax.set_ylabel('Overall Accuracy')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
