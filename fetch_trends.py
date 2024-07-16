import os
import random
import time
from pytrends.request import TrendReq
import pandas as pd

def read_keywords_from_csv(file_path, start_index, end_index):
    df = pd.read_csv(file_path)
    keywords = df.loc[(df['Index'] >= start_index) & (df['Index'] <= end_index), 'Product'].tolist()
    return keywords

def fetch_trends_data(keywords, geo, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='en-US', tz=360)
    data_dict = {'Product': []}

    for keyword in keywords:
        data_dict['Product'].append(keyword)
        attempts = 0
        success = False
        while not success and attempts < 5:  # Retry up to 5 times
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
                success = True
                delay = random.randint(120, 160)  # Random delay between 120 and 160 seconds
                print(f"Sleeping for {delay} seconds")
                time.sleep(delay)
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts}: An error occurred for keyword {keyword} in {geo}: {e}")
                if '429' in str(e):
                    print(f"Rate limit error. Sleeping for 3 minutes before retrying.")
                    time.sleep(180)  # Sleep for 3 minutes before retrying
                else:
                    for timestamp in data_dict.keys():
                        if timestamp != 'Product':
                            data_dict[timestamp].append(None)
                    break  # Exit loop on non-rate-limit error

    # Ensure all lists in the dictionary are of the same length
    max_len = max(len(lst) for lst in data_dict.values())
    for key in data_dict:
        while len(data_dict[key]) < max_len:
            data_dict[key].append(None)

    # Convert dictionary to DataFrame
    all_data = pd.DataFrame(data_dict)

    # Save DataFrame to CSV file
    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data_1_to_250.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    # Use environment variables or default values
    csv_file_path = os.getenv('CSV_FILE_PATH', 'product-list/apparel_and_clothes.csv')
    start_index = int(os.getenv('START_INDEX', 1))
    end_index = int(os.getenv('END_INDEX', 250))

    # Ensure the CSV file exists at the specified path
    if not os.path.isfile(csv_file_path):
        raise FileNotFoundError(f"The specified CSV file does not exist: {csv_file_path}")

    # Read keywords from the CSV file
    kw_list = read_keywords_from_csv(csv_file_path, start_index, end_index)

    # Fetch trends data for the keywords in the specified index range
    us_state_geocode = 'US'
    fetch_trends_data(kw_list, us_state_geocode, timeframe='2020-06-04 2024-06-04')
