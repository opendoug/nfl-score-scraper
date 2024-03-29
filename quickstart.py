from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import json
from datetime import datetime
from datetime import timedelta

# Connect to Google Sheets API
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
  creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
  else:
      flow = InstalledAppFlow.from_client_secrets_file(
          'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open('token.json', 'w') as token:
      token.write(creds.to_json())
service = build('sheets', 'v4', credentials=creds)

# Define the season and week variables
first_week_start = datetime(2023, 1, 4)
year = 2022
season_type = 2 # preseason is 1, regular season is 2
how_many_weeks = 1

# Initiate a while loop starting at week 1
week = 1
while week <= how_many_weeks:
  start_date = (first_week_start + timedelta(weeks=(week - 1)))
  start_date_clean = start_date.strftime('%Y%m%d')
  print(start_date_clean)
  end_date_clean = (start_date + timedelta(days=6)).strftime('%Y%m%d')
  print(end_date_clean)

  # Scrape the game IDs from ESPN
  scoreboard_url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=' + str(start_date_clean) + '-' + str(end_date_clean)
  # old one was scoreboard_url = 'https://www.espn.com/nfl/scoreboard/_/year/' + str(year) + '/seasontype' + '/' + str(season_type) + '/week/' + str(week) + '?xhr=1'
  game_response = requests.get(scoreboard_url)
  print('Scoreboard retrieved')
  game_json = json.loads(game_response.text)
  game_list = (game_json['events'])
  # game_list = (game_json['content']['sbData']['events'])
  game_ids = []
  for game in game_list:
    game_ids.append(game['id'])
  print('Game IDs retrieved')

  # Scrape the scoring play data from ESPN
  for game_id in game_ids:
    game_url = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=' + game_id
    # old one was game_url = 'https://www.espn.com/nfl/game/_/gameId/' + game_id + '&_xhr=1'
    print(game_url)
    scoring_response = requests.get(game_url)
    print('Game data retrieved')
    print(scoring_response.text)
    scoring_json = json.loads(scoring_response.text)
    scoring_plays = (scoring_json['scoringPlays'])
    teams = (scoring_json['boxscore']['teams'])
    home_team = teams[1]['team']['abbreviation']
    away_team = teams[0]['team']['abbreviation']
    margin = []
    for play in scoring_plays:
      margin.append(play['homeScore'] - play['awayScore'])
    hlc = {'home': home_team, 'home_high': (max(margin)), 'home_low': (min(margin)), 'home_close': (margin[-1])
      , 'away': away_team, 'away_high': 0-(min(margin)), 'away_low': 0-(max(margin)), 'away_close': 0-(margin[-1])}
    print('HLC data built')

   # Construct the data being sent to Google Sheets
    SAMPLE_SPREADSHEET_ID = '15eozXKseiAJUskONRWc7OgAp1CUfeOj9JQ_rUq4UwyY'
    SAMPLE_RANGE_NAME = str(year) + '!A1'
    VALUE_INPUT_OPTION = 'USER_ENTERED'
    INSERT_DATA_OPTION = 'INSERT_ROWS'
    VALUE_RANGE_BODY = {
      "values": [
        [
          year, week, hlc['home'], hlc['home_high'], hlc['home_low'], hlc['home_close']
        ],
        [
          year, week, hlc['away'], hlc['away_high'], hlc['away_low'], hlc['away_close']
        ]
      ]
    }

    # Call the Sheets API
    sheet = service.spreadsheets()
    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID
      , range=SAMPLE_RANGE_NAME
      , valueInputOption=VALUE_INPUT_OPTION
      , insertDataOption=INSERT_DATA_OPTION
      , body=VALUE_RANGE_BODY)
    response = request.execute()
    print('Data sent to Google Sheets')

  # Increment week by 1
  week +=1

# Tell me you're done
else:
  print('All done!')
