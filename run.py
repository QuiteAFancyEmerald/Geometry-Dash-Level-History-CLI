import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
import pandas as pd
from matplotlib.ticker import FuncFormatter, MaxNLocator

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
sorted_online_ids, sorted_estimations = zip(*sorted_data)

fig, ax = plt.subplots()
ax.plot(sorted_online_ids, sorted_estimations, marker='o', linestyle='-', color='b', alpha=0.5)
ax.set_xlabel('Approx. Online ID')
ax.set_ylabel('Estimation Date')
ax.set_title('Yearly Geometry Dash Level ID Pool')

ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

ax.yaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_yticks(pd.date_range(start=min(sorted_estimations), end=max(sorted_estimations), freq='Y'))

for tick in ax.get_xticklabels():
    tick.set_rotation(45)
    
ax.set_xlim(0, max(sorted_online_ids) + 100000)
ax.set_ylim(min(sorted_estimations) - timedelta(days=365), max(sorted_estimations) + timedelta(days=365))

plt.show()
