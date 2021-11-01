
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
import time

# Years and Leagues
leagues=[('premier-league', 'GB1'), ('laliga', 'ES1'), ('bundesliga', 'L1'), ('serie-a', 'IT1'), ('ligue-1', 'FR1')]
start=2014
years=[i for i in range(start, datetime.datetime.now().year)]

l=[]
for year in years:
    for league in leagues:
        url='https://www.transfermarkt.com/{}/transfers/wettbewerb/{}/plus/?saison_id={}&s_w=&leihe=0&intern=0'.format(league[0],league[1],year)
        print(url)
        page=requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup=BeautifulSoup(page.content, 'html.parser')
        all_teams=soup.find(class_='large-8')
        all_teams = all_teams.find_all(class_='box')[3:]
        for team in all_teams:
            team_name=team.find(class_='table-header').h2.a.text
            for index, in_out in enumerate(team.find_all('table')):
                for row in in_out.find_all('tr')[1:]:
                    tds=row.find_all('td')
                    try:
                        player_name=tds[0].div.span.a.text
                        print(player_name, end=' ')
                        age=tds[1].text
                        print(age, end=' ')
                        pos=tds[3].text
                        print(pos, end=' ')
                        if 'Retired' in tds[7].text:
                            from_club = 'retired'
                        else:
                            from_club=tds[7].a.text
                        print(from_club, end=' ')
                        fee=tds[8].a.text
                        print(fee, end=' ')
                        to_club=team_name
                        print(to_club, end=' ')
                        transfer_direction='in' if index == 0 else 'out'
                        season='{}/{}'.format(year,str(year+1)[-2:])
                        print(season, end='')
                        key=player_name+fee+season
                        print(transfer_direction, end=' ')
                        l.append([player_name,age,pos,from_club,to_club,fee,transfer_direction,season,league[0],key])
                        print('')
                    except:
                        print(league[0], year, tds[0].text) 
        print(league, year)
        time.sleep(5)


df = pd.DataFrame(l)
print(df.head())
print(len(df['Key'].unique()))
df.columns=['Player Name', 'Age', 'Position', 'Team 2', 'Team 1', 'Fee', 'Direction', 'Season', 'League', 'Key']
df = df.drop_duplicates(subset='Key', keep='first')
df.to_csv('historic_transfers.csv')





