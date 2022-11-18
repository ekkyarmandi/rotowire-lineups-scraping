# Rotowire Scraping Script

Rotowire lineups scraping is collecting lineups data, especially for Football games. The script will go through the list of URL, collecting the data and save it as one output file.

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
rw.save()
```

Import the Rotowire class from [rotowire.py](rotowire.py). Use `get` method to scrape the lineups data right away from the url then save it as csv using `save` method.