import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import os

class Rotowire:

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
        self.lineup_rows = []
        lineups = html.find("div",class_="lineups").find_all("div",class_="lineup")
        for lineup in lineups:
            if all([x not in lineup['class'] for x in ['is-ad','is-tools']]):
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

                game = lineup.find("div",class_="lineup__main")

                game_class = ["is-home","is-visit"]
                teams = [row['home'],row['away']]
                for gc, team in zip(game_class,teams):
                    injury = False
                    row['status'] = None
                    game_pos = game.find("ul",class_=gc)
                    players = game_pos.select("li[class*='lineup']")
                    for player in players:
                        new_row = dict(team=team)
                        if "lineup__player" in player['class']:
                            new_row['position'] = player.find("div",class_="lineup__pos").text.strip()
                            new_row['player'] = player.find("a").text.strip()
                            player_status = player.find("span",class_="lineup__inj")
                            if injury:
                                new_row['playing'] = "NO"
                            elif player_status:
                                new_row['playing'] = "MAYBE"
                            else:
                                new_row['playing'] = "YES"

                            new_row.update(row)
                            self.lineup_rows.append(new_row)

                        elif not row['status']:
                            row['status'] = player.text.strip()

                        elif player.text.lower().strip() == "injuries":
                            injury = True

    def save(self):
        '''
        Export scraped lineups data as a csv/json
        '''

        league = self.league.lower().replace(" ","_")
        filename = f"{league}_rotowire.csv"

        prev_df = [] 
        if os.path.exists(filename):
            prev_df = pd.read_csv(filename)

        df = pd.DataFrame(self.lineup_rows)
        columns = ['scraping_timestamp','league','date','time','home','away','status','team','position','player','playing']
        try:
            df = df[columns]
            if len(prev_df) > 0:
                df = pd.concat([prev_df,df])
            df.to_csv(filename,index=False)
        except:
            print('Error: the table was Empty')