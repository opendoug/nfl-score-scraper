# NFL Score Scraper
 Scrapes scoring play data from ESPN and sends it to a Google Sheet
 
# Motivation
 Somewhere around 2006 or 2007, as "big data" was reaching the level of regular end users at their home PCs, I started to dabble with sports analytics. There was a long and well-documented history of sports analytics, most notably Bill James (of Moneyball fame) and his fellow sabermetricians who were pouring over baseball statistics. But there were plenty of eyes on football statistics as well and by that time anyone with Excel could access vast amounts of data via the web, or start creating their own databases.
 
 I tried to find my own novel way of looking at the game. The general idea, the common intersection between all of the various sports analytics models, was that if you could break wins and losses into some smaller elements, and you had some way of measuring those elements, that 1) wins and losses could be better explained, and 2) wins and losses could be better controlled/predicted. Some people went toward the "fundamental" analysis - use statistical methods to measure the correlations between the elements they were tracking and see which could help you form probabilities. I went with a "technical" analysis. In hindsight, I'm sure that the majority of what I produced was just finding random patterns in statistical noise. But one thing I'm still stuck on is predicting wins and losses by looking at how teams win - there's a big difference between a team that comes from behind to win games and a team that wins by dominating the entire time.
 
 My work led me to a set of metrics that measure the largest lead, largest deficit, and final margin for each team in each game. Was the final margin closer to the largest lead, or closer to the largest deficit? I can use this to create a value for how "stable" the team was. Teams with an average margin closer to their average largest lead receive a higher score than teams with an average margin closer to their average largest deficit. I also look at the largest lead by any time during the season, as well as the largest deficit by any team during the season, to put all of the game metrics in a larger context. A team that consistently wins in comeback fashion - perhaps falling behind by large deficits, but scratching out comeback wins - lacks stability. Their score will be middling. A dominant + stable 7-2 team would be expected to defeat an instable 7-2 team that frequently falls behind. That's the hypothesis, anyway.
 
![fig1-779212](https://user-images.githubusercontent.com/11572875/190671876-8bdb7c10-aefd-4dd9-8457-0a6cdc8ee738.jpg)

 What you get, after measuring all of this and performing some calculations, is a descriptive metric that says how many games a team *should* have won or lost. And you can plot the individual game measurements on a candlestick or other chart to look for patterns. This is all very similar to the "Pythagorean" method of determining wins and losses using points for and points against - it just goes to another level by factoring in how "stable" a team's wins were.
 
# So...about the script...
 
 This script is written in Python. The main file you'll use is quickstart.py.
 
 What this script does is scrape game data from ESPN's [hidden API](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b). You start by entering in a season (YYYY) as well as the date of the first Thursday game during that season (YYYYmmdd) and the number of weeks during the season. You also note which week to begin scraping at. The script then requests data about the first week you requested, and produces a list of game IDs. Those game IDs are fed into the second request that the script makes, which produces the largest lead, largest deficit, and final margin of the game for each team. Those values are written into a Google Sheet. The script will iterate through every week of the season, depending on the starting week you feed in.

 You'll need to create a credentials.json file for your Google Apps integration to work. You'll also generate a token.json file when you run the Google OAuth process, which saves a local token and aids in creating refresh tokens.
