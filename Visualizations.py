import json
import pandas as pd
import matplotlib.pyplot as plt

# Load in the dictionary saved previously
json_file_path = "CombinedTop1000Movies.json"

with open(json_file_path, 'r') as j:
     letterboxd_movies = json.loads(j.read())

# The Letterboxd dictionary now has the Letterboxd AND IMDb data in it so its converted into a pandas
# dataframe and saved as a csv
names = []
years = []
runtime = []
certificate = []
rating_l = []
rating_i = []
rating_m = []
for movie in letterboxd_movies:
    # Get a list of all the values out of the dictionary to make columns from
    names.append(letterboxd_movies[movie]['normal_name'])
    certificate.append(letterboxd_movies[movie]['certificate'])
    years.append(letterboxd_movies[movie]['year'])
    runtime.append(letterboxd_movies[movie]['runtime'])
    rating_l.append(letterboxd_movies[movie]['letterboxd_rating'])
    rating_i.append(letterboxd_movies[movie]['imdb_rating'])
    if letterboxd_movies[movie]['metascore_rating'] != '':
        rating_m.append(letterboxd_movies[movie]['metascore_rating'])
    else:
        rating_m.append('0')
# Initialize the Dataframe and then add the columns collected above into it
movie_data = pd.DataFrame(columns=['MovieName', 'Year', 'Certificate', 'Runtime', 'Let_Rating', 'IMDb_Rating', 'Meta_Rating'])
values = [names, years, certificate, runtime, rating_l, rating_i, rating_m]
i = 0
for column in movie_data.columns:
    movie_data[column] = values[i]
    i += 1
# Change the columns into the correct type for later visualizations
movie_data['Let_Rating'] = pd.to_numeric(movie_data['Let_Rating'],errors='coerce')
movie_data['IMDb_Rating'] = pd.to_numeric(movie_data['IMDb_Rating'],errors='coerce')
movie_data['Meta_Rating'] = pd.to_numeric(movie_data['Meta_Rating'],errors='coerce')

# Save the new combined dataset to csv just because

movie_data.to_csv('CombinedTop1000Movies.csv')

# Now visualize the data
LetvsIMDb = movie_data.plot.scatter(x='Let_Rating',y='IMDb_Rating')
LetvsIMDb.set_ylim(7.9,10)
LetvsIMDb.set_title('Letterboxd Ratings vs IMDb Ratings \non {} highest rated Movies'.format(len(letterboxd_movies)))
plt.savefig('LetterboxdvsIMDb')

LetvsMeta = movie_data.plot.scatter(x='Let_Rating',y='Meta_Rating')
LetvsMeta.set_ylim(60,101)
LetvsMeta.set_title('Letterboxd Ratings vs Metascore Ratings \non {} highest rated Movies'.format(len(letterboxd_movies)))
plt.savefig('LetterboxdvsMetascore')

MetavsIMDb = movie_data.plot.scatter(x='Meta_Rating',y='IMDb_Rating')
MetavsIMDb.set_xlim(60,101)
MetavsIMDb.set_ylim(7.9, 10)
MetavsIMDb.set_title('Metascore Ratings vs IMDb Ratings \non {} highest rated Movies'.format(len(letterboxd_movies)))
plt.savefig('MetascorevsIMDb')
