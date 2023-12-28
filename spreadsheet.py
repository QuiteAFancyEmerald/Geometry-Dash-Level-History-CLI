import requests
import csv
from datetime import datetime, timedelta
import random
import pandas as pd

def generate_random_date(year, month):
    if month == 0:
        year -= 1
        month = 12

    end_of_month = datetime(year, month % 12 + 1, 1) - timedelta(days=1)
    random_day = random.randint(1, end_of_month.day)
    return f"{year}-{(month % 12) + 1:02d}-{random_day:02d}"

start_date = datetime(2013, 7, 1)
end_date = datetime.now()
date_list = [generate_random_date(date.year, date.month) for date in pd.date_range(start=start_date, end=end_date, freq='MS')]

all_online_ids = []
all_estimations = []

for random_date in date_list:
    api_url = f"https://history.geometrydash.eu/api/v1/date/date/{random_date}"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        approx = data.get('approx')
        if approx is not None:
            online_id = int(approx.get('online_id', 0))
            estimation = pd.to_datetime(approx.get('estimation')).date()

            all_online_ids.append(online_id)
            all_estimations.append(estimation)

            print(f"GD History Data Output: {estimation.strftime('%Y-%m-%d')} - {online_id}")
        else:
            print(f"No 'estimated' entries found for {random_date}.")
    else:
        print(f"Error for {random_date}: Unable to fetch data from the API. Status code: {response.status_code}")

sorted_data = sorted(zip(all_online_ids, all_estimations), key=lambda x: x[0])

csv_file = 'output/output_data.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Approximate Online ID', 'Estimated Date'])
    writer.writerows(sorted_data)

print(f"Data saved to {csv_file}.")
