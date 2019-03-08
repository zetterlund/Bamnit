import os
import sys
import json
import configparser
import logging
import sqlalchemy
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.chdir('../..')
sys.path.append(os.getcwd())
from app.models import Listing


logging.basicConfig(filename='app/analysis/COMPUTE_STATS_ERRORS.log',
                    level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('app/analysis/CREDENTIALS.INI')
engine = create_engine(config.get('DEFAULT', 'creds'))
Session = sessionmaker(bind=engine)



def update_weekday_count():
    weekday_count = [0] * 5
    listings = session.query(Listing)
    for l in listings:
        day = l.begin_date.weekday()
        weekday_count[day] += 1
    s = sum(weekday_count)
    weekday_count = [float(i)/s for i in weekday_count]
    return weekday_count

def update_time_available():
    listings = session.query(Listing)
    df = pd.read_sql_query(listings.statement, engine)
    df['time_available'] = df['date_removed'] - df['date_posted']

    top_list = df['time_available'].value_counts().index[0:1]
    df.drop(df[df['time_available'].isin(top_list)].index, inplace=True)

    time_available = {}
    for g in df['grade'].value_counts().index:    
        time_available[g] = df.loc[df['grade'] == g, 'time_available'].median().seconds
    return time_available


def update_all():
    stats_dict = {}
    stats_dict['weekday_count'] = update_weekday_count()
    stats_dict['time_available'] = update_time_available()
    with open('app/analysis/stats_dict.txt', 'w') as outfile:
        json.dump(stats_dict, outfile)



try:
    session = Session()
    update_all()
except Exception as e:
    logger.error(e)
finally:
    session.close()