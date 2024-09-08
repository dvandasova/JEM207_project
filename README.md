# JEM207_project
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

Then, the user input containing a unique match code inserted by the user is loaded. The code then checks whether the match code is valid and whether it points to a date in the future (there will be no flights and accommodation options for dates that occured in the past).

Finally, the code extracts the primary match code and subsequently the corresponding line in the internal database.

##### How to use
For the input to work it is necessary to download the input .txt file from the repository "02_Datasets" and replace the filepath leading to the file in your repository. The internal database of matches is uploaded directly from the git repository and does not require further attention.

To make an input, open the input .txt file and select your desired match from the list of matches. Then insert the match code on the 2nd line in the input .txt file.

Now you are good to proceed with the rest.

#### Scraping
##### Flights
[to be finalized upon finishing the code]
- What library/ API was used?
- What site was scraped?
- What were some interesting aspects of the scraping? Eg. what components had to be scraped or overcame
- What attributes were obtained?

#### Accomodation Possibilities
[to be finalized upon finishing the code]
- What library/ API was used?
- What site was scraped?
- What were some interesting aspects of the scraping? Eg. what components had to be scraped or overcame
- What attributes were obtained?

#### Geo-locations
[to be finalized upon finishing the code]
- What library/ API was used?
- How were locations obtained
- How were distances obtained

#### Combination Algorythm
[to be finalized upon finishing the code]
- What weights were placed at each attributes?
- What travel packages were built?

#### Output & Visualization
[to be finalized upon finishing the code]
- How does the output look like?
- Visualizations???
