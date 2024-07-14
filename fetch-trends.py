import os
from pytrends.request import TrendReq
import pandas as pd
import time

# Function to read keywords from a CSV file based on index range
def read_keywords_from_csv(file_path, start_index, end_index):
    df = pd.read_csv(file_path)
    keywords = df.loc[(df['Index'] >= start_index) & (df['Index'] <= end_index), 'Product'].tolist()
    return keywords

def fetch_trends_data(keywords, geo, timeframe='2020-06-04 2024-06-04', start_index=1, end_index=250):
    pytrends = TrendReq(hl='en-US', tz=360)
    data_dict = {'Product': []}
    
    for keyword in keywords:
        data_dict['Product'].append(keyword)
        try:
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
            interest_over_time_df = pytrends.interest_over_time()
            if not interest_over_time_df.empty:
                interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                interest_over_time_df.reset_index(inplace=True)
                for index, row in interest_over_time_df.iterrows():
                    timestamp = row['date'].strftime('%Y-%m-%d')
                    if timestamp not in data_dict:
                        data_dict[timestamp] = []
                    data_dict[timestamp].append(row[keyword])
                print(f"Collected data for {keyword} in {geo}")
            else:
                print(f"No data for {keyword} in {geo}.")
                for timestamp in data_dict.keys():
                    if timestamp != 'Product':
                        data_dict[timestamp].append(None)
            time.sleep(120)  # Wait for 120 seconds to avoid hitting the rate limit
        except Exception as e:
            if 'too many requests' in str(e).lower():
                print(f"Too many requests error for keyword {keyword} in {geo}. Sleeping for 30 minutes.")
                time.sleep(1800)  # Wait for 30 minutes before retrying
            else:
                print(f"An error occurred for keyword {keyword} in {geo}: {e}")
            for timestamp in data_dict.keys():
                if timestamp != 'Product':
                    data_dict[timestamp].append(None)
            # Save collected data so far
            save_data(data_dict, start_index, end_index)
            continue

    # Ensure all lists in the dictionary are of the same length
    max_len = max(len(lst) for lst in data_dict.values())
    for key in data_dict:
        while len(data_dict[key]) < max_len:
            data_dict[key].append(None)

    # Convert dictionary to DataFrame
    all_data = pd.DataFrame(data_dict)

    # Save DataFrame to CSV file
    if not all_data.empty:
        file_path = os.path.join('data', f'combined_trends_data_{start_index}_to_{end_index}.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

def save_data(data_dict, start_index, end_index):
    # Ensure all lists in the dictionary are of the same length
    max_len = max(len(lst) for lst in data_dict.values())
    for key in data_dict:
        while len(data_dict[key]) < max_len:
            data_dict[key].append(None)

    # Convert dictionary to DataFrame
    all_data = pd.DataFrame(data_dict)

    # Save DataFrame to CSV file
    if not all_data.empty:
        file_path = os.path.join('data', f'partial_trends_data_{start_index}_to_{end_index}.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved partial data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    csv_file_path = os.getenv('/Users/yavaren/Documents/Documents/Spirex/spirex-data/product-list/apparel_and_clothes-eng.csv')
    start_index = int(os.getenv('START_INDEX', '1'))
    end_index = int(os.getenv('END_INDEX', '250'))

    # Read keywords from the CSV file
    kw_list = read_keywords_from_csv(csv_file_path, start_index, end_index)

    # Fetch trends data for the keywords in the specified index range
    us_state_geocode = 'US'
    fetch_trends_data(kw_list, us_state_geocode, timeframe='2020-06-04 2024-06-04', start_index=start_index, end_index=end_index)
