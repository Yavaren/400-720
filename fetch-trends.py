from pytrends.request import TrendReq
import pandas as pd
import time
import os

# List of US state geocodes
us_state_geocodes = [
    'US-AL', 'US-AK', 'US-AZ', 'US-AR', 'US-CA', 'US-CO', 'US-CT', 'US-DE', 'US-FL', 'US-GA',
    'US-HI', 'US-ID', 'US-IL', 'US-IN', 'US-IA', 'US-KS', 'US-KY', 'US-LA', 'US-ME', 'US-MD',
    'US-MA', 'US-MI', 'US-MN', 'US-MS', 'US-MO', 'US-MT', 'US-NE', 'US-NV', 'US-NH', 'US-NJ',
    'US-NM', 'US-NY', 'US-NC', 'US-ND', 'US-OH', 'US-OK', 'US-OR', 'US-PA', 'US-RI', 'US-SC',
    'US-SD', 'US-TN', 'US-TX', 'US-UT', 'US-VT', 'US-VA', 'US-WA', 'US-WV', 'US-WI', 'US-WY'
]

def fetch_trends_data(keywords, states, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='en-US', tz=360)
    all_data = pd.DataFrame()

    for state in states:
        for keyword in keywords:
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=state, gprop='')
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                    interest_over_time_df['state'] = state
                    interest_over_time_df['keyword'] = keyword
                    all_data = pd.concat([all_data, interest_over_time_df])
                    print(f"Collected data for {keyword} in {state}")
                else:
                    print(f"No data for {keyword} in {state}.")
                time.sleep(60)  # Wait for 60 seconds to avoid hitting the rate limit
            except Exception as e:
                print(f"An error occurred for keyword {keyword} in {state}: {e}")
                time.sleep(60)  # Wait for 60 seconds before retrying with the next keyword

    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data_by_state.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop", "headphones", "tablet", "smartwatch", 
        # "gaming console", "VR headset", "smart home", "wireless charger", 
        # "action camera", "4K TV", "drone", "Bluetooth speaker", 
        # "electric scooter", "fitness tracker", "robot vacuum", 
        # "portable projector", "3D printer", "AI assistant", "wearable tech"
    ]
    fetch_trends_data(kw_list, us_state_geocodes, timeframe='2020-06-04 2024-06-04')
