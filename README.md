# senate-votes
Retrieving the senator's votes from the Romanian Senate website

Introduction /br
This is a training project. /br
Automating the process was quite chalenging so I've asked and received help on writing the code.

Technologies /br
Python 3.7 /br
Selenium /br
Requests /br
BeautifulSoup /br
Pandas 

Launch /br
I use Spyder and the libraries are via Anaconda.

Status /br
I scraped and saved on files the votes for years 2017 and 2018, 2019 being work in progress. 

Trivia /br
The scraper has two separate stages: getting the links to the laws pages and getting the actual votes from there. I used Selenium to navigate through the webpage and Pandas to create the database. There are some broken links that caused the code on getting_votes.py to crash. I solved the problem manualy.
