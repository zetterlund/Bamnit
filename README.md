# Bamnit
### Bamnit is a service for substitute teachers to receive notifications when their preferred jobs become available.


There are two main components to the project:
* Flask backend
* Scrapy web scraping script


In addition, several cron jobs are in place to keep the data up-to-date.  Every 10 minutes:
* Scraper crawls and collects data
* Stats are computed and saved
* Notifications are emailed to users


Visit www.Bamnit.com to learn more and play around with the project.