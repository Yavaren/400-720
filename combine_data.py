import os
import pandas as pd

data_files = [f for f in os.listdir('data') if f.startswith('combined_trends_data_') and f.endswith('.csv')]
combined_data = pd.concat([pd.read_csv(os.path.join('data', file)) for file in data_files])
combined_data.to_csv('data/combined_trends_data_final.csv', index=False)