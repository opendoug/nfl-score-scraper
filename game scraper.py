import requests
import json

# Scrape the game IDs from ESPN
scoreboard_url = 'https://www.espn.com/nfl/scoreboard/_/year/2021/seasontype/2/week/1?xhr=1'
response = requests.get(scoreboard_url)
site_json = json.loads(response.text)
game_list = (site_json['content']['sbData']['events'])
game_ids = []
for game in game_list:
  game_ids.append(game['id'])
print(game_ids)