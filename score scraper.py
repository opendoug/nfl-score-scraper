import requests
import json

url = 'https://www.espn.com/nfl/game/_/gameId/401326317&xhr=1'
response = requests.get(url)
site_json = json.loads(response.text)
scoring_plays = (site_json['gamepackageJSON']['scoringPlays'])
teams = (site_json['gamepackageJSON']['boxscore']['teams'])
home_team = teams[1]['team']['abbreviation']
away_team = teams[0]['team']['abbreviation']
margin = []
for play in scoring_plays:
    margin.append(play['homeScore'] - play['awayScore'])
hlc = {'home': home_team, 'home_high': (max(margin)), 'home_low': (min(margin)), 'home_close': (margin[-1])
    , 'away': away_team, 'away_high': 0-(min(margin)), 'away_low': 0-(max(margin)), 'away_close': 0-(margin[-1])}
print(hlc['home'])