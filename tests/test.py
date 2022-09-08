import random
import requests

AIRPORTS = ['DCA', 'LAX', 'IAD', 'MSP', 'PHL', 'ATL', 'IAH', 'MCO', 'JFK', 
     'ORD', 'MDW', 'DFW', 'LAS', 'SFO', 'PHX', 'PDX', 'BWI', 'DTW', 'TPA', 
     'CLT', 'LGA', 'MIA', 'SEA', 'SAN', 'SLC', 'EWR', 'FLL', 'DEN', 'BOS']
ITERATIONS = 1000
APP_URL = 'http://localhost:8000'

for i in range(ITERATIONS):
    airport = random.choice(AIRPORTS)
    year = random.randint(2003, 2016)
    month = random.randint(1, 12)
    url = f"{APP_URL}/cancellations/airports/{airport}/{year}/{month}"
    requests.get(url)

url = f"{APP_URL}/metrics"
print(requests.get(url).json())