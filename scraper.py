from rotowire import Rotowire

rw = Rotowire()

# scrape lineups
url = "https://www.rotowire.com/soccer/lineups.php"
rw.get(url)
rw.export_as("csv")