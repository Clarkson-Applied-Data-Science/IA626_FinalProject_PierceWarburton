# IA626_FinalProject_PierceWarburton
The final project of Pierce Warburton in the Fall 2023 semester of IA 626

This final project revolves around the scraping of movie data from the website Letterboxd. This is a website that allows for users to track and rate different movies not
unsimilar to IMDb which is more well known. The big difference is that Letterboxd has more of a social media focus and as such its culture and users are
quite different than those of the more traditional sites such as IMDb. Letterboxd skews quite young and captures the input of those who are more "hip" than 
the older generations using IMDb. My interest in this data was thus to see if this difference in user base would translate to a difference in ratings for movies. Since it
would be unfeasible to compare all the movies on Letterboxd and IMDb I settled with comparing the top 1000. This decision was based mostly on the availablity of data for 
this number. IMDb has its API behind a paywall while Letterboxd is quite easy to access but doesn't compile its own rankings. However someone had uploaded a csv of data on 
the top 1000 IMDB user rated movies onto Kaggle (including both average user ratings and average critic ratings) and a Letterboxd user had made a list on Letterboxd of its respective 1000 highest ranked movies. So all I had to do was combine the two by parsing the csv file and scrapping the Letterboxd list for data. The last thing to note is that the way I combined these two lists is by comparing all the IMDb movies to the Letterboxd rankings, not the other way around. This meant that if a movie was on the Letterboxd list but not the IMDb list than I didn't try to go track down the IMDb ranking. I made this decision because again, the IMDb website was much harder to scape because they wanted people to buy their API.

## The Data
This project leveraged two dataset both centered around film data. The first data set was a personally compiled dataset that combined Letterboxd movie data with data scrapped from a Letterboxd list titled 'Letterboxd’s Top 1,000 Narrative Feature Films' made by user diego andaluz (https://letterboxd.com/thediegoandaluz/list/letterboxds-top-1000-narrative-feature-films). The other dataset was a csv file uploaded three years ago on Kaggle by user Omar Hany (https://www.kaggle.com/datasets/omarhanyy/imdb-top-1000/) which compiled the Top 1000 films as ranked by average IMDb user rating. 

#### LetterboxdTop1000Movies.json
The data here is stored in a json dictionary with the following structure. Note that the primary key is a particularly formatted version of the movie's name. 
```example-film-1:                                                              Name in the Letterboxd Format
          normal_name: 'Example Film 1'                                      Name as normally typed
          movie_page_link: '/film/example-film-1'                            Link to the movie's specific page from https:/Letterboxd.com
          year: '2000'                                                       Year of release for the movie
          letterboxd_rating: '4.43'                                          Average user rating out of 5
          runtime: '124'                                                     Movie runtime in minutes
```
#### IMDb_Top_1000.csv
The data here is stored in a tabular excel format with 1000 rows of 7 columns. These columsn are the title, certification (PG, PG-13, etc), duration, genre, rate (user rating), metascore (critic score), and description for the Top 1000 films on IMDb as ranked by average user rating. 

## My Process
In this repository are three python files: FinalProject_MainCode, Visualizations, and Letterboxd Functions. I will describe each in turn here. Note that only Visualizations.py requires any extra packages to be installed (pandas and matplotlib). This file only creates the images I will attach further below and is not necesary to run again except for validation of the images. 
#### Final Project_MainCode.py
This is the file in which the brunt of my work and process is stored. It begins by scrapping the Letterboxd Top 1000 list for names and links to each movies specific page on Letterboxd (a string that is happily enough stored with the name of the movie in the list). I then visit each of these pages to get further data about the movies such as their year of release, their length, and of course, their average rating. All of this data is stored in a dictionary with a very particular key used. Letterboxd stores all movie names in a very specific format that I found hard to achieve in default python. Rather than try to convert various names into this format (or hope unformatted names would match) I decided to simply piggyback on this format since Letterboxd provides the names themselves on almost every page.. So the keys for the dictionary of Letterboxd movies are the names of the movies in the Letterboxd format. To give you an example here a couple different names for a movie compared to the letter box format:

<center>Unformatted Names:
  The Godfather: Part 2
The GodFather: Part II
TheGodFatherPartII

Letterboxd Formating:
the-godfather-part-ii</center>

Overall formatting is obviously more consistent than no formating and since I couldn't easily extract names from Letterboxd's formatting but could place them into the formatting I used it as a universe way to write names. 

Once the dictionary of Letterboxd's Top 1000 films were compiled I loaded into the csv of the IMDb data and combined the two. This was done by iterating through the movies in the IMDb database and testing whether they already existed in the Letterboxd list or not. After all since both lists were compiled by different users but based around the same thing it wasn't unrealistic to expect lots of overlap. In fact the two lists shared most of the same movies. In total only 138 movies from the IMDb list were not represented in the Letterboxd list. A little less than 90% overlap. For those 138 movies on the IMDb list but not on the Letterboxd list I searched for them on the Letterboxd site and scraped their data to add to the list. Thus each movie had the average user ratings from Letterboxd, IMDb users, and the IMDb Metascore (the average critic ratings), as well as a little bit of other data such as year and runtime and so forth. This compiled dictionary of 1138 movies was then saved to a json file under the name "CombinedTop1000Movies.json".

Finally throughout this process in the couple of cases where average rating was not able to be found for one of the three ratings used, either because there were no reviews for it on Letterboxd or no Metascore value given in the csv, a null value of -1 was inputted as an obvious flag for erroneous data.

#### LetterboxdFunctions.py
This file contains all the functions used in the query of the Letterboxd website. Chief amoung them are the function used to search for a movie on Letterboxd (using their own search engine) and the function to scrape data from a movie's specific website, LetterboxdMovieSearch and LetterboxdPageScrapping respectively. Both of these functions are heavily commented and follow the structure of this process laid out in class. The one other function of note is the FormatName function. This gets a given string as close to the Letterboxd format as I could get without hard coding numerous special cases. The function is used when comparing the IMDb movies against the Letterboxd movies. Rather than sending a request to the website to search their database of movies and then scrape the formatted name for every movie I can use this function for 95% of the movies and only use Letterboxd's search engine for the special cases this function doesn't catch. This speeds up the process of comparing the two movies tremendously. Bring the time down from 45 minutes to around 3 minutes (further improvements were made from there).

#### Visualizations.py
Finally this file is where I did some analyzation of the combined dataset. Using the pandas library I converted the data from dictionary to DataFrame to leverage the graphing functions in the matplotlib library. To answer my original question of how the different user bases would agree or disagree over their Top 1000 movies I generated basic scatter plots of one type of rating vs another, iterating through all three combinations. The most surprising thing that I discovered was how varying the range of the scores were. When converted to a 10 point scale the critics (metascore) score ranged from around 6 to 10 while the IMDb user score only went from 8 to 10. Clearly the critics disagree on the IMDb user's picks for best movies. The Letterboxd users also seemed to disagree as their scores ranged form around 7 to 10 when compared on a 10 point scale. The other interesting thing was that even though the sample size was 1000 for both sites the final count of movies was 1139 films. Meaning that both user bases had an almost 90% overlap for their pick of best 1000 films. Clearly the ratings were most likely jumbled around between the two but its interesting they agreed this much to begin with. 
