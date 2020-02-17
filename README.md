#README


What is it? 

DataBiz aims to help small businesses to choose the best location possible for maximum success based on demand in the area, population, and median income levels.


How does it help?

Entrepreneurship is difficult but extremely rewarding. Ensuring business starts in the right location, with the right demand and resources is instrumental to success. Our goal was to utilize lots of the data resources we were given at VThacks to help the business world thrive, and therefore help the U.S. economy. DataBiz allows a user to input their current wealth, market they wish to enter, and desired locations for business. It then runs machine learning algorithms using various API's to determine the best locations for the price (depending on real-estate in the area) that the owner can afford.


How is it built?

-Scraped data from city-data.com of every city in the US for population, median income, cost of living, etc. using python. 
-Used Nessie API to get sample merchants and categories and linked them to locations
-Used YELP API to get merchants and categories linked to locations cleaned all data set and merged together in -Google data lab. 
-Use google cloud functions to create machine learning model of best options.
-Create flask app and hosted on Google Cloud Engine Used micro strategy for data visualization images should on app


Important Files:

-DataBiz.py
	-runs flask app that deploys data visualization and analytics to web site
	-allows users to input data to see relevant visualizations
	-deploys to front end pages found in template and static folders

-dataParser.py:
	-parses through large data files and cleans for formatting and modeling

-scrapeInfo.py
	-utilizes requests and bs4 to scrape data of over 4,000 cities from city-data.com


