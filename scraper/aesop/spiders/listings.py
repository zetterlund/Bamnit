# -*- coding, utf-8 -*-
import scrapy
from aesop.items import ListingItem
import os
import re
import time
import random
from urllib.request import urlretrieve
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.utils.project import get_project_settings



def get_fields(listing, job, field_dict):
    for i in range(len(field_dict)):
        field = list(field_dict.keys())[i]
        extract = list(field_dict.values())[i]
        attribute = extract[1]
        if attribute == 'text':
            try:
                value = job.find_element_by_xpath(extract[0]).text
            except:
                value = ""
            finally:
                listing[field] = value
        else:
            # For any non-text attributes, add logic here:
            listing[field] = ""
    return listing



class ListingsSpider(scrapy.Spider):
    name = 'listings'
    start_urls = get_project_settings().get("START_URL")

    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless") # Keep this to ensure Chrome runs properly
        self.chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"')

    def parse(self, response):
        driver1 = webdriver.Chrome(executable_path=os.path.abspath("/home/sven/scrape/chromedriver237"), chrome_options=self.chrome_options)
        try:
            driver1.get(response.url)
            time.sleep(3)

            usr = driver1.find_element_by_xpath("//form//input[@name='Username']")
            pwd = driver1.find_element_by_xpath("//form//input[@name='Password']")
            username = get_project_settings().get("ACCOUNT_LOGIN")
            password = get_project_settings().get("ACCOUNT_PASSWORD")
            usr.send_keys(username)
            pwd.send_keys(password)

            logbtn = driver1.find_element_by_xpath("//button[@type='submit']")
            logbtn.click()
            # time.sleep(10)


            ''' Wait for listings to load on page '''
            try:
                element = WebDriverWait(driver1, 30).until(
                    EC.presence_of_element_located((By.ID, "availableJobs"))
                )
            finally:
                pass


            ''' Close popup window if it exists '''
            try:
                time.sleep(1)
                close_button = driver1.find_element_by_xpath("//button[@type='button' and contains(@class, 'titlebar-close')]")
                close_button.click()
                time.sleep(1)
            finally:
                pass


            # ''' Take Screenshot '''
            # driver1.save_screenshot('screenshots/test1.png')


            # ''' Get job list '''
            jobs = driver1.find_elements_by_xpath("//div[@id='availableJobs']//tbody[contains(@class, 'job')]")
            # jobs = jobs[:10] # limit job list during testing


            ''' Extract info from each job '''
            for job in jobs:
                listing = ListingItem()
                field_dict = {
                'teacher': (".//span[@class='name']", 'text'),
                'title': (".//span[@class='title']", 'text'),
                'times': (".//td[@class='times']", 'text'),
                'fullday': (".//span[@class='durationName']", 'text'),
                'campus': (".//div[@class='locationName']", 'text'),
                }
                get_fields(listing, job, field_dict)

                listing['aesop_id'] = str(job.get_attribute("id"))

                try:
	                if "multiday" in job.get_attribute("class"):
	                    listing['multiday'] = True
	                    listing['begin_date'] = job.find_element_by_xpath(".//td[@class='date']//span[@class='itemDate']").text
	                    listing['end_date'] = job.find_element_by_xpath(".//td[@class='date']//span[@class='multiEndDate']").text
	                else:
	                    listing['multiday'] = False
	                    listing['begin_date'] = job.find_element_by_xpath(".//td[@class='date']//span[@class='itemDate']").text
	                    listing['end_date'] = listing['begin_date']
                except:
                	listing['multiday'] = "ERROR_FOUND1"
                	listing['begin_date'] = "ERROR_FOUND1"
                	listing['end_date'] = "ERROR_FOUND1"

                try:
                    job.find_element_by_xpath(".//a[contains(@class, 'hasNotes')]").click()
                    time.sleep(.8)
                
                    note_content = driver1.find_element_by_xpath("//div[@class='ui-dialog-content ui-widget-content']").text
                    listing['notes'] = note_content
                    close_button = driver1.find_element_by_xpath("//button[@type='button' and contains(@class, 'titlebar-close')]")
                    close_button.click()
                    time.sleep(.5)

                except Exception as e:
                    listing['notes'] = ""

                yield listing

        finally:
            driver1.close()