# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from scrapy.exceptions import DropItem
from datetime import datetime

import re
from aesop.models import ListingDB, db_connect, create_table



class AesopPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        listing_exists = session.query(exists().where(ListingDB.aesop_id==item['aesop_id'])).scalar()

        try:

            if listing_exists:
                the_listing = session.query(ListingDB).filter(ListingDB.aesop_id==item['aesop_id']).first()
                the_listing.date_removed = datetime.now()

            else:
                listingdb = ListingDB()
                listingdb.aesop_id = item['aesop_id']
                listingdb.teacher = item['teacher']
                listingdb.position = item['position']
                listingdb.subject = item['subject']
                listingdb.campus = item['campus']
                listingdb.begin_date = item['begin_date']
                listingdb.end_date = item['end_date']
                listingdb.multiday = item['multiday']
                listingdb.fullday = item['fullday']
                listingdb.notes = item['notes']
                listingdb.date_posted = item['date_posted']
                listingdb.date_removed = item['date_removed']
                listingdb.language = item['language']
                listingdb.grade = item['grade']
                listingdb.notification_sent = False
                session.add(listingdb)

            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item



class HelperPipeline(object):

    grade_list = [
        '(PRE-K)',
        '(KINDER)',
        '(FIRST GRADE)',
        '(SECOND GRADE)',
        '(THIRD GRADE)',
        '(FOURTH GRADE)',
        '(FIFTH GRADE)',
        '(6)(?=(?:TH|\W))',
        '(7\/8)',
        '(HS)',
        '(ELEM)E?N?T?A?R?Y?',
        '(MS)'
    ]    
    for i in range(len(grade_list)):
        grade_list[i] = re.compile(grade_list[i])

    def get_language(x):    
        pattern = re.compile('^(?:.*\W)?(BIL|ESL)(?:\W.*)?$')
        if re.match(pattern, x):
            return(re.match(pattern, x).group(1))
        else:
            return "ENGLISH"
        
    def get_grade(x):
        for grade in HelperPipeline.grade_list:
            pattern = re.compile('(?:^|\W)' + grade.pattern + '(?:\W|$)')
            if re.search(pattern, x):
                return re.search(pattern, x).group(1)    

    def get_class(x):
        for grade in HelperPipeline.grade_list:
            pattern = re.compile('^.*?' + grade.pattern + '\W?')
            x = re.sub(pattern, '', x)
            pattern = r'^(?:.*\W)?(BIL|ESL)(?:\W.*)?$'
            x = re.sub(pattern, '', x)
        return x.strip()

    def process_item(self, item, spider):
        item['begin_time'] = re.sub(r'^.*?(\d.*?(?:AM|PM)).*$', r'\1', item['times'], flags=re.DOTALL)
        item['begin_time'] = datetime.strptime(item['begin_time'], '%I:%M %p').time()
        item['begin_date'] = re.sub(r'^.*?(\d.*\d).*$', r'\1', item['begin_date'])
        item['begin_date'] = datetime.strptime(item['begin_date'], '%m/%d/%Y').date()
        item['begin_date'] = datetime.combine(item['begin_date'], item['begin_time'])

        item['end_time'] = re.sub(r'^.*\-.*?(\d.*?(?:AM|PM)).*$', r'\1', item['times'], flags=re.DOTALL)
        item['end_time'] = datetime.strptime(item['end_time'], '%I:%M %p').time()
        item['end_date'] = re.sub(r'^.*?(\d.*\d).*$', r'\1', item['end_date'])
        item['end_date'] = datetime.strptime(item['end_date'], '%m/%d/%Y').date()
        item['end_date'] = datetime.combine(item['end_date'], item['end_time'])

        item['position'] = re.sub(r'^(.*?)\-.*$', r'\1', item['title'])
        item['subject'] = re.sub(r'^.*?\-(.*)$', r'\1', item['title'])
        item['date_posted'] = datetime.now()
        item['date_removed'] = datetime.now()

        item['language'] = HelperPipeline.get_language(item['subject'])
        item['grade'] = HelperPipeline.get_grade(item['subject'])

        item['subject'] = re.sub(r'(^.*)\-.*$', r'\1', item['subject'])
        item['subject'] = HelperPipeline.get_class(item['subject'])

        return item