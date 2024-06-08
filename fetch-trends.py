from pytrends.request import TrendReq
import pandas as pd
import time
import os

def fetch_trends_data(keywords, geo='US', timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='en-US', tz=360)
    all_data = pd.DataFrame()

    for keyword in keywords:
        try:
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')
            interest_over_time_df = pytrends.interest_over_time()
            if not interest_over_time_df.empty:
                interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                all_data[keyword] = interest_over_time_df[keyword]
                print(f"Collected data for {keyword}")
            else:
                print(f"No data for {keyword}.")
            time.sleep(60)  # Wait for 60 seconds to avoid hitting the rate limit
        except Exception as e:
            print(f"An error occurred for keyword {keyword}: {e}")
            time.sleep(60)  # Wait for 60 seconds before retrying with the next keyword

    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop", "headphones", "tablet", "smartwatch", 
        "gaming console", "VR headset", "smart home", "wireless charger", 
        "action camera", "4K TV", "drone", "Bluetooth speaker", 
        "electric scooter", "fitness tracker", "robot vacuum", 
        "portable projector", "3D printer", "AI assistant", "wearable tech"]    
    fetch_trends_data(kw_list, geo='US', timeframe='2020-06-04 2024-06-04')
