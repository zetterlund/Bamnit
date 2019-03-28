import os
import sys
import json
import configparser
import logging
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
os.chdir('../..')
sys.path.append(os.getcwd())

from app.models import Listing



logging.basicConfig(filename='logs/update_fields.log',
                    level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('app/notifications/CREDENTIALS.INI')
engine = create_engine(config.get('DEFAULT', 'creds'))
Session = sessionmaker(bind=engine)



def update_field_dict():
    grades = set()
    subjects = set()
    languages = set()
    campuses = set()

    field_topics = [
        ('grade', grades),
        ('subject', subjects),
        ('language', languages),
        ('campus', campuses),
    ]
    field_dict = {x:[] for (x,y) in field_topics}
    
    bad_list = ['', None]
    
    for (x, y) in field_topics:
        for instance in session.query(Listing):
            y.add(getattr(instance, x))
        y = [h for h in y if h not in bad_list]
        for i in sorted(y):
            field_dict[x].append((i, i))
        field_dict[x].insert(0, ('---ANY---', '---ANY---'))
    
    with open('app/notifications/field_dict.txt', 'w') as outfile:
        json.dump(field_dict, outfile)



try:
    session = Session()
    update_field_dict()
except Exception as e:
    logger.error(e)
finally:
    session.close()