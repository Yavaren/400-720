import pandas as pd
import matplotlib.pyplot as plt

# Function to read the first row from a CSV file
def read_first_row(file_path):
    df = pd.read_csv(file_path, index_col=0)
    first_row = df.iloc[0]
    return first_row

# Function to visualize the first row data
def visualize_first_row(data, row_name):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data.values, marker='o')
    plt.title(f'{row_name} Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# Example usage
csv_file_path = '/Users/yavaren/Documents/Documents/Spirex/spirex-data/combined_trends_data_501_to_750.csv'

# Read the first row
first_row_data = read_first_row(csv_file_path)

# Visualize the first row data
visualize_first_row(first_row_data, first_row_data.name)
