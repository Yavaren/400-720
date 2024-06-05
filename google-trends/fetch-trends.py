import time
import random
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import pandas as pd
from proxy_list import get_proxies  # Import the proxy list

def fetch_trends_data(keywords, geo='US', timeframe='today 12-m', retries=5):
    proxy_list = get_proxies()
    keyword_data = []

    for keyword in keywords:
        proxy_attempts = 0
        while proxy_attempts < len(proxy_list):
            try:
                # Choose a proxy from the list
                proxy = proxy_list[proxy_attempts]
                print(f"Using proxy: {proxy} for keyword: {keyword}")
                pytrends = TrendReq(hl='en-US', tz=360, proxies={"http": proxy, "https": proxy})

                # Build the payload for the current keyword
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop='')

                # Fetch interest over time
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df['keyword'] = keyword
                    keyword_data.append(interest_over_time_df)

                # Save the interest over time data
                interest_over_time_df.to_csv(f'interest_over_time_{keyword}.csv')

                print(f"\nData for keyword '{keyword}' has been saved to CSV file.")
                break  # Break the proxy loop if successful

            except TooManyRequestsError:
                proxy_attempts += 1
                if proxy_attempts < len(proxy_list):
                    wait_time = random.randint(60, 120)  # Wait before switching to the next proxy
                    print(f"Too many requests error for proxy: {proxy}. Switching to the next proxy in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"All proxies failed for keyword '{keyword}'. Moving to the next keyword.")
                    break
            except Exception as e:
                proxy_attempts += 1
                print(f"An error occurred: {e}")
                if proxy_attempts < len(proxy_list):
                    wait_time = random.randint(60,60)  # Wait before switching to the next proxy
                    print(f"Retrying with the next proxy in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"All proxies failed for keyword '{keyword}'. Moving to the next keyword.")
                    break

    # Combine all data into a single DataFrame and save
    if keyword_data:
        combined_df = pd.concat(keyword_data)
        combined_df.to_csv('combined_interest_over_time.csv')

if __name__ == "__main__":
    kw_list = ["smartphone", "laptop", "headphones"]
    fetch_trends_data(kw_list, geo='US', timeframe='2020-06-04 2024-06-04')
