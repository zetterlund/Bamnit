# Bamnit
### Bamnit is a service for substitute teachers to receive notifications when their preferred jobs become available.

Main components:
- Flask backend
- React.js frontend
- Scrapy web scraping script

In addition, several cron jobs are in place to keep the data up-to-date.  Every 10 minutes:
- Scraper crawls and collects data
- Stats are computed and saved
- Notifications are emailed to users

Visit www.Bamnit.com to learn more and play around with the project.