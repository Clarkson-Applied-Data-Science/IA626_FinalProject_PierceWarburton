# Importing Libraries. I tried to use only default python libraries
import csv, json

# Import the Functions I wrote to scrap Letterboxd data
from LetterboxdFunctions import *

# Get the names of the 1000 highest rated movies on Letterboxd from this already curated list
letterboxd_movies = LetterBoxd_1000List()
# Now get the release year, unformatted title, average rating, and runtime for these movies
# Takes around 5 minutes to run
i = 0
for movie in letterboxd_movies:
    letterboxd_movies[movie]['year'], \
    letterboxd_movies[movie]['normal_name'], \
    letterboxd_movies[movie]['letterboxd_rating'], \
    letterboxd_movies[movie]['runtime'] = LetterboxdPageScrapping(letterboxd_movies[movie]['movie_page_link'])
    i +=1

    # Now initialize other key-value pairs for the future data set
    letterboxd_movies[movie]['imdb_rating'] = '-1'
    letterboxd_movies[movie]['metascore_rating'] = '-1'
    letterboxd_movies[movie]['certificate'] = 'N/A'
    letterboxd_movies[movie]['gross'] = 'N/A'

#Save the Letterboxd dataset to json
with open('LetterboxdTop1000Movies.json', 'w') as fp:
    json.dump(letterboxd_movies, fp)

# Load in the IMDb and Metascore data from the csv file 
with open('IMDb_Top_1000.csv',encoding="utf8") as f:
    imdb_raw_movie_data = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

# Reformat the data into a dictionary that will be easier to index and use
imdb_movies = {}
for row in imdb_raw_movie_data:
    movie_name = row['Title'].split('. ')[1].split(' (')[0]
    movie_imdb_rating = row['Rate']
    movie_metascore_rating = row['Metascore']
    movie_gross = row['Info'].split('Gross: $')[-1].split('M')[0]
    movie_certification = row['Certificate']
    movie_year = row['Title'].split('. ')[-1].split('(')[-1].split(')')[0]
    imdb_movies[movie_name] = {'imdb_rating': movie_imdb_rating, 'metascore_rating': movie_metascore_rating, \
                               'gross': movie_gross, 'certificate': movie_certification, 'year':movie_year}


# Go through and match the two dictionarys (IMDb and Letterboxd) together. This is done by seeing if
# either the formatted or unformatted name of a movie in the IMDb database is the same as the name
# of a movie in the Letterboxd dataset. If it is then the data from the IMDb dataset is simply added
# to the Letterboxd dataset. If the IMDb movie is NOT represented in the Letterboxd dataset however
# than the Letterboxd website is queried and the corresponding data brought over and added to the 
# Letterboxd dataset. Any movie in the IMDb dataset NOT found on Letterboxd at all is recorded in the
# rejectmovies list. 
# Takes about 1 minutes
rejectmovies = []

for movie in imdb_movies:
    # Try and convert movie name into letterboxd name format and also try that with the year added. 
    # These two options will usually cover most movies. If one doesn't work this code simply tries
    # the other
    first_name_option = FormatName(movie)
    second_name_option = first_name_option + '-' + imdb_movies[movie]['year']
    # See if the first name optoin is an instant match between Letterboxd and IMDb
    if first_name_option in letterboxd_movies.keys():
        letterboxd_movies[first_name_option]['imdb_rating'] = imdb_movies[movie]['imdb_rating']
        letterboxd_movies[first_name_option]['metascore_rating'] = imdb_movies[movie]['metascore_rating']
        letterboxd_movies[first_name_option]['gross'] = imdb_movies[movie]['gross']
        letterboxd_movies[first_name_option]['certificate'] = imdb_movies[movie]['certificate']
    # See if the second name option is an match 
    elif second_name_option in letterboxd_movies.keys():
        letterboxd_movies[second_name_option]['imdb_rating'] = imdb_movies[movie]['imdb_rating']
        letterboxd_movies[second_name_option]['metascore_rating'] = imdb_movies[movie]['metascore_rating']
        letterboxd_movies[second_name_option]['gross'] = imdb_movies[movie]['gross']
        letterboxd_movies[second_name_option]['certificate'] = imdb_movies[movie]['certificate']
    # If not then search the movie name on Letterboxd to get more information so it can be added to the
    # final data structure
    else:
        # Search for movie on Letterboxd to get their naming format
        letterboxd_name, letterboxd_link = LetterboxdMovieSearch(movie)
        if letterboxd_link != 'N/A':
            letterboxd_movies[letterboxd_name] = {}
            letterboxd_movies[letterboxd_name]['year'], \
            letterboxd_movies[letterboxd_name]['normal_name'], \
            letterboxd_movies[letterboxd_name]['letterboxd_rating'], \
            letterboxd_movies[letterboxd_name]['runtime'] = \
                LetterboxdPageScrapping(letterboxd_link)
            # Finally add imdb and metascore data to the new entry
            letterboxd_movies[letterboxd_name]['imdb_rating'] = imdb_movies[movie]['imdb_rating']
            letterboxd_movies[letterboxd_name]['metascore_rating'] = imdb_movies[movie]['metascore_rating']
            letterboxd_movies[letterboxd_name]['gross'] = imdb_movies[movie]['gross']
            letterboxd_movies[letterboxd_name]['certificate'] = imdb_movies[movie]['certificate']
        else:
            rejectmovies.append(movie)


# Save combined dictionary to json
with open('CombinedTop1000Movies.json', 'w') as fp:
    json.dump(letterboxd_movies, fp)

















