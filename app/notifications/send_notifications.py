import os
import sys
import ast
import configparser
import logging
import sqlalchemy
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
os.chdir('../..')
sys.path.append(os.getcwd())

from app.models import Listing, Notification, User
from app.notifications.notification_helper import topic_list



def get_email_body(user):    
    header = """You have {} new notifications from Bamnit!

Jobs now available:\n\n------------------\n\n""".format(len(message_dict[user]))
    
    jobs = ""
    for l in sorted(list(message_dict[user]), key=lambda x: x.begin_date):
        jobs += ''.join(['Date: ', str(l.begin_date.strftime("%A, %b %d %Y")),
                        '\nGrade: ', str(l.grade),
                        '\nSubject: ', str(l.subject),
                        '\nLanguage: ', str(l.language),
                        '\nCampus: ', str(l.campus),
                        '\n\n------------------\n\n'])
    
    footer = """\n\n(This is not a valid email address, no replies will be answered)

You are receiving this email because you signed up for notifications from www.Bamnit.com"""
    
    body = header + jobs + footer
    return body



logging.basicConfig(filename='logs/send_notifications.log',
                    level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('app/notifications/CREDENTIALS.INI')
engine = create_engine(config.get('DEFAULT', 'emailcreds'))
Session = sessionmaker(bind=engine)
gmail_user = config.get('DEFAULT', 'gmail_user')
gmail_password = config.get('DEFAULT', 'gmail_password')



session = Session()

listings = session.query(Listing).filter(Listing.notification_sent == False).all()
notifications = session.query(Notification).all()



''' Remove bad notifications '''
for n in list(notifications): # Iterate over a COPY of the notifications list
    try:
        if getattr(n, 'receiver') is None:
            notifications.remove(n)
    except:
        logger.error("Problem occurred in the 'Remove bad notifications' section for n: ", n)



message_dict = {}
for listing in listings:
    for notification in notifications:
        should_send = True

        try:
            for topic in topic_list:
                
                '''Convert string safely to list'''
                to_check = getattr(notification, topic)
                if to_check == None:
                    to_check = []
                    continue # If nothing was selected, assume the user meant "Any"
                else:
                    to_check = ast.literal_eval(to_check)
                
                '''If "Any" is selected, mark as OK and go to next topic'''
                if '---ANY---' in to_check:
                    continue
                
                '''If a listing's specifications not covered in the notification, break the loop'''
                if getattr(listing, topic) not in to_check:
                    should_send = False
                    break
                    
            if should_send == True:
                
                '''Add the listing to the user's list to be emailed'''
                if notification.receiver not in message_dict.keys():
                    message_dict[notification.receiver] = set()
                message_dict[notification.receiver].add(listing)

        except Exception as e:
            print(e)
            logger.error("Problem occurred while checking each notification with:\nListing: {}\nNotification: {}\nTopic: {}\n\n\n".format(listings.index(listing),
                                                                                                                                          notifications.index(notification),
                                                                                                                                          topic))
            print("Listing: ", listings.index(listing), "  Notification: ", notifications.index(notification), "  Topic: ", topic)



for user in list(message_dict):
    if user.notifications_enabled == False:
        del message_dict[user]



try:

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
    
    for user in message_dict:
        
        msg = MIMEMultipart()
        
        msg['From'] = gmail_user
        msg['To'] = user.email
        msg['Subject'] = '[Bamnit] {} New Jobs Available!  Notification for {}'.format(len(message_dict[user]),
                                                                                       datetime.now().strftime("%m/%d/%y %I:%M:%S %p"))  
        
        body = get_email_body(user)
        msg.attach(MIMEText(body, 'plain'))
        
        
        server.send_message(msg)
        del msg
        
    server.close()
    
    '''Mark listings as having their notifications sent so they are not sent again'''
    try:
        for l in listings:
            l.notification_sent = True
        session.commit()
    except Exception as e1:
        session.rollback()
        logger.error(e1)

except Exception as e2:
    logger.error(e2)

finally:
    session.close()