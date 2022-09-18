from rotowire import Rotowire

rw = Rotowire()

urls = [
    "https://www.rotowire.com/soccer/lineups.php",
    "https://www.rotowire.com/soccer/lineups.php?league=FRAN",
    "https://www.rotowire.com/soccer/lineups.php?league=LIGA",
    "https://www.rotowire.com/soccer/lineups.php?league=SERI",
    "https://www.rotowire.com/soccer/lineups.php?league=BUND",
    "https://www.rotowire.com/soccer/lineups.php?league=MLS",
    "https://www.rotowire.com/soccer/lineups.php?league=UCL",
    "https://www.rotowire.com/soccer/lineups.php?league=LMX"
]

for url in urls:
    rw.get(url)

rw.save()