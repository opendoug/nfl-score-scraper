from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests
import json

# Scrape the scoring play data from ESPN
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

# Push the scoring play data into Google Sheets
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15eozXKseiAJUskONRWc7OgAp1CUfeOj9JQ_rUq4UwyY'
SAMPLE_RANGE_NAME = 'Sheet1!A1'
VALUE_INPUT_OPTION = 'RAW'
INSERT_DATA_OPTION = 'INSERT_ROWS'
VALUE_RANGE_BODY = {
  "values": [
    [
      hlc['home'], hlc['home_high'], hlc['home_low'], hlc['home_close']
    ],
    [
      hlc['away'], hlc['away_high'], hlc['away_low'], hlc['away_close']
    ]
  ]
}

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

# Call the Sheets API
sheet = service.spreadsheets()
request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID
    , range=SAMPLE_RANGE_NAME
    , valueInputOption=VALUE_INPUT_OPTION
    , insertDataOption=INSERT_DATA_OPTION
    , body=VALUE_RANGE_BODY)
response = request.execute()