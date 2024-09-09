# JEM207_project
## HOW TO RUN
In the 04_RUN file there are the following files:
1. RUN_main.ipynb
2. RUN_full-scrape.ipynb
3. full-scrape.xlsx
4. iternal-data.xlsx
5. input.txt

To run the main part of the project, it is necessary to run the RUN_full-scrape.ipynb to obtain the full-scrape.xlsx dataset that is essential to plot the visuals. For time purposes, we provide the full-scrape.xlsx dataset ready for importing into the main notebook.

After obtaining the full-scrape.xlsx dataset, proceed to the main part of the project.

To provide your input, download the input.txt file to your device, copy the filepath and insert it to the highlighted place in the RUN_main.ipynb file. This highlighted place is located at the top of the notebook.
In your input.txt, write a code of a match on the 2nd line. You cannot enter a code related to a match that is about to happen in less then 2 weeks time - if you try to use it, the RUN_main.ipyn notebook will notify you.

Now you are ready to proceed to the RUN_main.ipynb notebook and run it from the top.

## Spectators Unlimited Ltd. (Final project of subject JEM207)

### Motivation for the Project
Sports tourism refers to travel which involves either observing or participating in a sporting event while staying apart from the tourists' usual environment ([Wikipedia](https://en.wikipedia.org/wiki/Sports_tourism)). It is also one of the fastest-growing segments of tourism (estimated growth rate of 17.5% between 2023-2030) generating around 10% of the world’s expenditure on tourism ([UN Tourism](https://www.unwto.org/sport-tourism)).
In Europe, however, this segment still remains rather unsaturated. And that is where spectators Unlimited Ltd. enter the game.

### Spectators Unlimited Ltd. Solution
We bring sports tourism to the public such that once someone secures their ticket, he can select pre-made packages with travel and accommodation options based on package attributes and his budget. Our use case will be demonstrated on the case of [XX] which will take place after the project's deadline and will therefore ensure smooth performance of the code.

### Technology Toolkit
[to be finalized upon finishing the code] Can this be replaced by the requirements.txt file?
- What libraries and components of them we used and something about them - version, why? etc.
- In case of geopy, mention that it uses openmaps (or what)

### Project Components
Spectators Unlimited Ltd. solution contains the following components:
1. Input
2. Scraping (flights & accommodation possibilitiesú
5. Geo-locations
6. Combination Algorithm
7. Output

Each component and its functionalities are further described below.

#### Input
The input section of the code loads the internal database from the git repository, checks for correct form the file (correct content and prder of columns) and saves the data as a data frame with the date in date-time format. 

Then, the user input containing a unique match code inserted by the user is loaded. The code then checks whether the match code is valid and whether it points to a date at least 2 weeks in the future (there will be no flights and accommodation options for dates that occured in the past or that are too close to today).

Finally, the code extracts the primary match code and subsequently the corresponding line in the internal database.

##### How to use
For the input to work it is necessary to download the input .txt file from the repository "02_Datasets" and replace the filepath leading to the file in your repository. The internal database of matches is uploaded directly from the git repository and does not require further attention.

To make an input, open the input .txt file and select your desired match from the list of matches. Then insert the match code on the 2nd line in the input .txt file.

Now you are good to proceed with the rest.

#### Scraping
Our project involves web scraping of both flight and accomodation options. We use Selenium to interact with the web elements and to also reduce the risk of being locked out by CAPTCHA due to Selenium imitating human behavior (imitating pressing keyboard and clicking) as well as BeautifulSoup for HTML parsing.

Overall scraping is set to be as consistent and replicable as possible, resulting in higher scraping times. Feel free to adjust sleep parametres in our code to reduce the scraping time.
##### Flights
For scraping flights we specificaly used Selenium, BeautifulSoup, Pandas (for data manipulation) and Time (for adding delays during scraping). 

The scraped site is the flight section of kayak.com 

##Key aspect of the scraping: 
Code closes any popup windows which might or might not appear after opening the website, possibly limiting the full content from loading. Further ensuring that all the necessary scrapable elements are loaded, we use sleep statements, which surprisingly led to more consistent result than using "WebDriverWait", which appears to be universally the more popular option. Lastly, we ensure that no layover flights are present, by removing flights featuring "multiple airlines".

Using our scraping mechanism we are able to consistently obtain
The flight destination
Departure and return dates
Flight prices
And inherently also the cheapest flight by further processing the obtained flight prices (it would be possible to also account for the quality of the flight, e.g. airline, departure time, with flights in the night being less desirable etc.), but even though adding this feature would not be difficult, the complexity was already high to not include it.

#### Accomodation Possibilities
We use the same combination of packages for accommodation scraping as for flight scraping. 

Scraping accommodation was a little bit difficult with running into multiple issues: 
Accommodation either not having rating, price or being not able to be located via used geolocation packages: solved by omitting these entries from the newly created dataset completely in each scraping iteration

Accommodation not being fully displayed on the page: partially solved by "Keys.PAGE_DOWN" loop, which sent the webdriver to the bottom of the page

Captcha challenge: CAPTCHA sometimes appearing after longer periods of scraping (usually 15-20 minutes), which on a few hour scrape poses an issue. We partially solved it by reloading the WebDriver after each scraping iteration, essentially clearing the cache and lowering the chances of being caugth by captcha, reloading the page multiple times, which on multiple occasions was able to bypass the captcha completely, and lastly using Selenium which imitates human behavior, i.e. further decreasing the risk of CAPTCHA. 
To be completely honest, there is still a risk of CAPTCHA, but we did our best to limit the risks. 

We were able to obtain Location, Name, Rating and Price of each hotel in each scraping iteration, which is then later used for further manipulation and package bundling. 

#### Geo-locations
Geo-location, i.e., distance between accommodation and the match venue, is one of the criteria used to sort and create the accommodation bundles. 

To calculate the distances, we used the geopy library to first obtain coordinates of the accommodation possibilites and the match venue, then we calculated the distance between them and sorted from nearest to furthest. After that, a range of all the distances was created and the accommodation possibilities were ranked into 3 categories based on percentiles within that range.

#### Combination Algorythm
[to be finalized upon finishing the code]
- What weights were placed at each attributes?
- What travel packages were built?

#### Output & Visualizations
##### Visualizations
Visulizations in this project aim to show the user the demand around other matches based on accommodation type (Standard, Superior, Luxurious), and potentially help him when selecting future stays. The project contains 2 types of visualizations - bar chart and heat maps.

The bar chart shows mean price of each accommodation type in each match day, essentially showing which match day is the cheapest to book.

Heat maps are plotted for each accommodation type separately and show the mean price for each combination of teams, essentially showing which combination of team is the least and most premium. As a byproduct, the heatmap can indicate which teams are most likely scoring the highest since the demand to see them will be the strongest.
