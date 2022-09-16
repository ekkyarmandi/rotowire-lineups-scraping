# Rotowire Scraping Script

Rotowire lineups scraping script writen in Python

### Install dependencies
```
pip install -r requirements.txt
```

### How to use
```^python
from rotowire import Rotowire

rw = Rotowire()

url = "https://www.rotowire.com/soccer/lineups.php"
rw.get(url)
rw.export_as("csv")
```

Import the Rotowire class from [rotowire.py](rotowire.py). Use `get` method to scrape the lineups data right  away then configure the output file format. There are two kind of output format: csv and json.