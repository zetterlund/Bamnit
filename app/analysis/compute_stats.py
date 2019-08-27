import os
import sys
import json
import configparser
import logging
import sqlalchemy
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
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



# Helper function for 'update_job_count'
def get_daily_count(df, dimension):
    df2 = df.drop(df[df[dimension] == ''].index)
    df2 = df2.groupby([dimension, 'begin_date']).count()
    df3 = np.array(df2)[:, 0]
    df2 = np.array(df2.index.values)
    daily_count = dict()
    k = np.array([[a, b.isoformat()] for (a, b) in df2])
    for u in np.unique(k[:, 0]):
        daily_count[u] = []
    for i, j in enumerate(k):
        daily_count[j[0]].append((j[1], int(df3[i])))
    return daily_count

def update_job_counts():
    listings = session.query(Listing.begin_date, Listing.end_date, Listing.multiday, Listing.grade, Listing.subject).filter(Listing.end_date > (datetime.now() - timedelta(days=32)), Listing.begin_date < (datetime.now() + timedelta(days=9))).all()

    df = pd.DataFrame(listings)
    df['begin_date'] = df['begin_date'].apply(lambda x: x.date())
    df['end_date'] = df['end_date'].apply(lambda x: x.date())

    added_days = []
    for index, row in df.iterrows():
        if row['multiday'] == True:
            date_range = pd.date_range(row['begin_date'], row['end_date'])
            for i in date_range[1:]:
                added_days.append([i.date(), i.date(), row['multiday'], row['grade'], row['subject']])

    added_df = pd.DataFrame(added_days, columns=df.columns)
    df = pd.concat([df, added_df])
    df.reset_index(inplace=True)
    df.drop(['end_date', 'multiday'], axis=1, inplace=True)

    today_date = datetime.now().date()
    df.drop(df[(df['begin_date'] > (today_date + timedelta(days=7))) | (df['begin_date'] < (today_date - timedelta(days=28)))].index, inplace=True)
    df.drop(df[df['begin_date'].apply(lambda x: x.weekday()) > 4].index, inplace=True)

    total_daily_count = list()
    for a, b in df['begin_date'].value_counts().items():
        total_daily_count.append((a.isoformat(), b))

    grade_daily_count = get_daily_count(df, 'grade')
    subject_daily_count = get_daily_count(df, 'subject')

    daily_counts = {
        'total_daily_count': total_daily_count,
        'grade_daily_count': grade_daily_count,
        'subject_daily_count': subject_daily_count
    }

    return(daily_counts)



def update_all():
    stats_dict = {}
    stats_dict['weekday_count'] = update_weekday_count()
    stats_dict['time_available'] = update_time_available()
    with open('app/analysis/stats_dict.txt', 'w') as outfile:
        json.dump(stats_dict, outfile)

    daily_counts = update_job_counts()
    with open('app/analysis/daily_counts.txt', 'w') as outfile:
        json.dump(daily_counts, outfile, ensure_ascii=False)


try:
    session = Session()
    update_all()
except Exception as e:
    logger.error(e)
finally:
    session.close()
