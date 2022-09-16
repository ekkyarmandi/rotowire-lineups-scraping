import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

class Rotowire:

    def __init__(self) -> None:
        self.lineup_rows = []

    def get(self,url) -> None:
        '''
        Make a GET request to the URL and scrape the lineups
        '''
        
        # read the html content
        print("scraping",url)
        html = requests.get(url)
        html = BeautifulSoup(html.text,"html.parser")

        # gather initial data
        today = datetime.now()
        league = html.find("h1",class_="page-title__primary").text.strip()
        self.league = league.replace(" Lineups","")
        row = dict(
            scraping_timestamp=today.strftime("%Y-%m-%d %H:%M:%S"),
            league=self.league
        )

        # fint the lineups
        lineups = html.find("div",class_="lineups").find_all("div",class_="lineup")
        for lineup in lineups:
            if 'is-ad' not in lineup['class']:
                schedule = lineup.find("div",class_="lineup__time")
                for label,string in zip(["date","time"],schedule.strings):
                    row[label] = string.strip()
                    if label == "date":
                        date = datetime.strptime(string.strip(),"%B %d")
                        row[label] = date.replace(year=today.year)

                lineup = lineup.find("div",class_="lineup__box")
                header = lineup.find("div",class_="lineup__matchup")
                row['home'] = header.find("div",class_="is-home").text.strip()
                row['away'] = header.find("div",class_="is-visit").text.strip()
                row['status'] = None

                game = lineup.find("div",class_="lineup__main")

                game_class = ["is-home","is-visit"]
                teams = [row['home'],row['away']]
                for gc, team in zip(game_class,teams):
                    game_pos = game.find("ul",class_=gc)
                    players = game_pos.select("li[class*='lineup']")
                    for player in players:
                        new_row = dict(team=team)
                        if "lineup__player" in player['class']:
                            new_row['position'] = player.find("div",class_="lineup__pos").text.strip()
                            new_row['player'] = player.find("a").text.strip()
                            player_injury = player.find("span",class_="lineup__inj")
                            if player_injury:
                                new_row['playing'] = "NO"
                            else:
                                new_row['playing'] = "YES"

                            new_row.update(row)
                            self.lineup_rows.append(new_row)

                        elif not row['status']:
                            row['status'] = player.text.strip()
       
    def export_as(self,kind):
        '''
        Export scraped lineups data as a csv/json
        '''

        filename = datetime.now().strftime(f"%Y-%m-%d_{self.league.lower()}_rotowire")
        if kind == "csv":
            filename = filename+".csv"
            df = pd.DataFrame(self.lineup_rows)
            columns = ['scraping_timestamp','league','date','time','home','away','status','team','position','player','playing']
            df = df[columns]
            df.to_csv(filename)
        elif kind == "json":
            filename = filename+".json"
            json.dump(
                self.lineup_rows,
                open(filename),
                indent=4
            )

        if len(self.lineup_rows) > 0:
            print("lineups data has been exported as",filename)