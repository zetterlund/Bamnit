''' Set up logging '''
import logging

logger = logging.getLogger('Riot_Logger')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(logging_formatter)
stream_handler.setFormatter(logging_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



''' Import modules and initialize global variables '''
import numpy as np
import random
import requests
import time

MATCH_CRAWL_LIMIT = 100000
total_matches_crawled = 0



''' Import API credentials '''
import configparser
config = configparser.ConfigParser()
config.read('CONFIG.INI')
api_key = config['RIOT']['api_key']
my_username = config['RIOT']['my_username']



''' Instantiate connection to database '''
from pymongo import MongoClient
client = MongoClient()
db = client['riot_games']
games = db.games
record_stats = db.record_stats

# # (Wipe all game info during testing)
# db.drop_collection('games')
# db.drop_collection('record_stats')



''' Instantiate record stats if none exist '''
if record_stats.find_one({}) is None:
    new_record = dict()
    record_keys = [
        'deaths',
        'kills',
        'pentaKills',
        'totalTimeCrowdControlDealt',
        'totalDamageTaken',
        'totalDamageDealtToChampions',
        'deathsPerSecond',
        'killsPerSecond',
        'pentaKillsPerSecond',
        'totalTimeCrowdControlDealtPerSecond',
        'totalDamageTakenPerSecond',
        'totalDamageDealtToChampionsPerSecond',
        'teamKills',
        'teamKillsPerSecond',
        'totalKills',
        'totalKillsPerSecond',
        'gameDuration',
    ]
    for r in record_keys:
        new_record[r] = {'value': 0}
    record_stats.insert_one(new_record)



''' Define recursive scraping function '''
def process_match(match):

    global MATCH_CRAWL_LIMIT
    global total_matches_crawled



    # Get match info
    gameId = match['gameId']
    r = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(gameId, api_key))
    gameInfo = r.json()



    ''' Check that match should be captured '''

    # Check that match matches desirable criteria
    if gameInfo['gameMode'] != 'ARAM':
        logger.info('Encountered non-ARAM game mode: "{}"'.format(gameInfo['gameMode']))
        return False
    if gameInfo['mapId'] != 12:
        logger.info('Encountered incorrect "mapId" value: "{}"'.format(gameInfo['mapId']))
        return False
    if gameInfo['platformId'] != 'NA1':
        logger.info('Encountered incorrect "platformId" value: "{}"'.format(gameInfo['platformId']))
        return False

    # Check if we've captured the match before
    if games.find_one({'_id': gameId}) is not None:
        logger.info('Encountered gameId previously crawled: {}'.format(gameId))
        return False



    ''' Capture match info '''
    matchInfo = dict()
    matchInfo['_id'] = gameInfo['gameId']
    matchInfo['gameDuration'] = gameInfo['gameDuration']
    matchInfo['gameVersion'] = gameInfo['gameVersion']
    matchInfo['gameCreation'] = gameInfo['gameCreation']

    for team in gameInfo['teams']:
        if team['win'] == 'Win':
            matchInfo['victoriousTeam'] = team['teamId']

    matchInfo['team100champions'] = list()
    matchInfo['team200champions'] = list()
    for player in gameInfo['participants']:
        if player['teamId'] == 100:
            matchInfo['team100champions'].append(player['championId'])
        if player['teamId'] == 200:
            matchInfo['team200champions'].append(player['championId'])

    # Save match info to database
    logger.debug("Inserting matchInfo to database")
    games.insert_one(matchInfo)



    ''' Check for record-breaking stats '''
    record = record_stats.find_one({}) # (Get current record)

    # Check for individual records
    for player in gameInfo['participants']:

        stats = dict()

        # Extract only certain stats from all available
        stats['deaths'] = player['stats']['deaths']
        stats['kills'] = player['stats']['kills']
        stats['pentaKills'] = player['stats']['pentaKills']
        stats['totalTimeCrowdControlDealt'] = player['stats']['totalTimeCrowdControlDealt']
        stats['totalDamageTaken'] = player['stats']['totalDamageTaken']
        stats['totalDamageDealtToChampions'] = player['stats']['totalDamageDealtToChampions']

        # Engineer new stats from existing data
        stats['deathsPerSecond'] = stats['deaths'] / matchInfo['gameDuration']
        stats['killsPerSecond'] = stats['kills'] / matchInfo['gameDuration']
        stats['pentaKillsPerSecond'] = stats['pentaKills'] / matchInfo['gameDuration']
        stats['totalTimeCrowdControlDealtPerSecond'] = stats['totalTimeCrowdControlDealt'] / matchInfo['gameDuration']
        stats['totalDamageTakenPerSecond'] = stats['totalDamageTaken'] / matchInfo['gameDuration']
        stats['totalDamageDealtToChampionsPerSecond'] = stats['totalDamageDealtToChampions'] / matchInfo['gameDuration']

        # Update database if stats surpass the current record
        for stat_key in stats.keys():
            if stats[stat_key] > record[stat_key]['value']:
                record_stats.update_one({}, {'$set': {'{}.value'.format(stat_key): stats[stat_key]}})
                record_stats.update_one({}, {'$set': {'{}.gameId'.format(stat_key): gameInfo['gameId']}})
                record_stats.update_one({}, {'$set': {'{}.participantId'.format(stat_key): player['participantId']}})
                record_stats.update_one({}, {'$set': {'{}.championId'.format(stat_key): player['championId']}})
                record = record_stats.find_one({})


    # Check for team records
    team100kills = 0
    team200kills = 0
    for player in gameInfo['participants']:
        if player['teamId'] == 100:
            team100kills += player['stats']['kills']
        if player['teamId'] == 200:
            team200kills += player['stats']['kills']
    totalKills = team100kills + team200kills
    team100killsPerSecond = team100kills / matchInfo['gameDuration']
    team200killsPerSecond = team200kills / matchInfo['gameDuration']
    totalKillsPerSecond = totalKills / matchInfo['gameDuration']

    for killCount in [team100kills, team200kills]:
        if killCount > record['teamKills']['value']:
            record_stats.update_one({}, {'$set': {'teamKills.value': killCount}})
            record_stats.update_one({}, {'$set': {'teamKills.gameId': gameInfo['gameId']}})
            record = record_stats.find_one({})

    for killCountPerSecond in [team100killsPerSecond, team200killsPerSecond]:
        if killCountPerSecond > record['teamKillsPerSecond']['value']:
            record_stats.update_one({}, {'$set': {'teamKillsPerSecond.value': killCountPerSecond}})
            record_stats.update_one({}, {'$set': {'teamKillsPerSecond.gameId': gameInfo['gameId']}})
            record = record_stats.find_one({})

    if totalKills > record['totalKills']['value']:
        record_stats.update_one({}, {'$set': {'totalKills.value': totalKills}})
        record_stats.update_one({}, {'$set': {'totalKills.gameId': gameInfo['gameId']}})
        record = record_stats.find_one({})

    if totalKillsPerSecond > record['totalKillsPerSecond']['value']:
        record_stats.update_one({}, {'$set': {'totalKillsPerSecond.value': totalKillsPerSecond}})
        record_stats.update_one({}, {'$set': {'totalKillsPerSecond.gameId': gameInfo['gameId']}})
        record = record_stats.find_one({})


    # Check for match records
    if matchInfo['gameDuration'] > record['gameDuration']['value']:
        record_stats.update_one({}, {'$set': {'gameDuration.value': matchInfo['gameDuration']}})
        record_stats.update_one({}, {'$set': {'gameDuration.gameId': gameInfo['gameId']}})
        record = record_stats.find_one({})



    ''' Finish processing match '''
    total_matches_crawled += 1
    logger.debug("Match successfully added.  Now adding +1 to total_matches_crawled.")



    ''' FIND A NEW MATCH TO PROCESS '''

    ''' Select new player and new set of matches to choose from '''
    player = random.choice(gameInfo['participantIdentities'])['player']

    # (If encountering disparity in player info, log it)
    if player['accountId'] != player['currentAccountId']:
        logger.info('Curiosity: Player found with different "accountId" and "currentAccountId" values.\n\
        Continuing to process as normal.\n\
        accountId: {}\n\
        currentAccountId: {}'.format(player['accountId'], player['currentAccountId']))

    # Get info on new player
    playerId = player['currentAccountId']
    r = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}'.format(playerId, api_key))
    matches = r.json()['matches']

    # Shuffle matches for randomness
    np.random.shuffle(matches)

    local_error_counter = 0
    for match in matches:

        # Make sure we're not taking the scraper too far
        if total_matches_crawled < MATCH_CRAWL_LIMIT:

            # (Sleep to rate-limit the API calls)
            time.sleep(2)

            ''' Recurse through match processing '''
            try:
                result = process_match(match)
                if result == False:
                    local_error_counter += 1
                    if local_error_counter > 3:
                        logger.warning("Encountered more than the maximum number of permitted local errors.")
                        return
                    continue
                else:
                    continue
            except Exception as e:
                logger.error("Encountered error in try/except loop trying to fetch results: {}".format(e))
    # (Add in some code here in case the For loop exhausts all of a player's recent matches)



if __name__ == '__main__':

    ''' Initialize crawl with call to my own account '''

    # Get my matches
    r = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(my_username, api_key))
    my_account_id = r.json()['accountId']
    r = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}'.format(my_account_id, api_key))
    matches = r.json()['matches']

    # Shuffle matches for randomness
    np.random.shuffle(matches)

    # ... and BEGIN!
    for match in matches:
        process_match(match)
