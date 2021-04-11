from riotwatcher import LolWatcher
import pandas as pd
import sys
import requests.exceptions

# global variables
api_key = 'RGAPI-7f9937af-3c79-4ff4-bf3a-e8092bc53045' # must get new riot api key every 24 hours
watcher = LolWatcher(api_key)
my_region = 'na1'

# check if summoner name exists
try:
    summoner_name = input("Enter in your summoner name: \n")
    me = watcher.summoner.by_name(my_region, summoner_name)
except requests.exceptions.HTTPError:
    print("Summoner name does not exist")
    sys.exit()

# check if summoner has match data
try:
    my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
except requests.exceptions.HTTPError:
    print("No match data found")
    sys.exit()

# check league's latest version
latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# fetch last match detail
last_match = my_matches['matches'][0]
match_detail = watcher.match.by_id(my_region, last_match['gameId'])

pd.set_option('display.max_columns', 16)
pd.set_option('display.width', 2000)

participants = []
for row in match_detail['participants']:
    participants_row = {}
    participants_row['champion'] = row['championId']
    participants_row['win'] = row['stats']['win']
    participants_row['kills'] = row['stats']['kills']
    participants_row['deaths'] = row['stats']['deaths']
    participants_row['assists'] = row['stats']['assists']
    participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
    participants_row['goldEarned'] = row['stats']['goldEarned']
    participants_row['champLevel'] = row['stats']['champLevel']
    participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
    participants_row['Item1'] = row['stats']['item0']
    participants_row['item2'] = row['stats']['item1']
    participants_row['Item3'] = row['stats']['item2']
    participants_row['item4'] = row['stats']['item3']
    participants_row['Item5'] = row['stats']['item4']
    participants_row['item6'] = row['stats']['item5']
    participants_row['item7'] = row['stats']['item6']
    participants.append(participants_row)

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']
for row in participants:
    row['champion'] = champ_dict[str(row['champion'])]


# team data
team_number = 1
teams = []
for row in match_detail['teams']:
    teams_row = {}
    teams_row['Team'] = team_number
    teams_row['TowerKills'] = row['towerKills']
    teams_row['FirstBlood'] = row['firstBlood']
    teams_row['InhibitorKills'] = row['inhibitorKills']
    teams_row['BaronKills'] = row['baronKills']
    teams_row['DragonKills'] = row['dragonKills']
    teams_row['Win'] = row['win']
    teams.append(teams_row)
    team_number = team_number + 1


participant_df = pd.DataFrame(participants)
teams_df = pd.DataFrame(teams)

print(participant_df)
print()
print(teams_df)
