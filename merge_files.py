import pandas as pd
import os

# Path to the directory containing the data files
data_dir = 'data'
output_file = os.path.join(data_dir, 'final_combined_trends_data.csv')

# List to hold data frames
df_list = []

# Iterate over files in the data directory
for file_name in os.listdir(data_dir):
    if file_name.startswith('combined_trends_data_') and file_name.endswith('.csv'):
        file_path = os.path.join(data_dir, file_name)
        df = pd.read_csv(file_path)
        df_list.append(df)

# Concatenate all data frames
final_df = pd.concat(df_list, ignore_index=True)

# Save the final concatenated data frame to CSV
final_df.to_csv(output_file, index=False)

print(f"Merged data saved to {output_file}")
