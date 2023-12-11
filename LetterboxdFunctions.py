import requests, string


'''
The two most important functions here are searching for a movie on the website Letterboxd 
(LetterboxdMovieSearch) and scraping the movie's page on Letterboxd (LetterboxdPageScrape). 
'''

def LetterboxdMovieSearch(movie_name):
    '''
    ----- Arguments -----
    movie_name (str): The name of a movie. Doesn't have to be a specific format but the search engine
                        of Letterboxd isn't the greatest so the closer it is the better
    
    ----- Outputs ------
    movie_name (str): This is the name that Letterboxd stores for the movie and is in a very
                        specific format. Easier to scrap off of the website than generate myself
    movie_page_link (str): This is the second half of the link to the page on Letterboxd containg
                            information about a specific movie. In the format of /film/{movie_name}/

    ----- Description -----
    This function searchs on Letterboxd with a given movie name and finds out the way that movie's
    name is stored in Letterboxd as well as the link to that movie's specific page. My rational is
    that since I am looking at the 1000 highest rated movies the first result on Letterboxd will  
    mostly likely be the the movie I desire
    '''
    # Get movie into correct format for Letterboxd search
    movie_name = movie_name.replace(' ', '+')
    # movie_page_link = 'N/A'
    # movie_name = 'N/A'
    # Search for movie and scrape data from first (most popular) result
    url = 'https://letterboxd.com/search/{}/'.format(movie_name)
    r = requests.get(url)
    if 'class="results"' in r.text:
        movie_name = r.text.split('class="results"')[1].split('data-film-slug="')[1].split('"')[0]
        movie_page_link = r.text.split('class="results"')[1].split('data-target-link="')[1].split('"')[0]
    else:
        movie_name = 'N/A'
        movie_page_link = 'N/A'
    return(movie_name, movie_page_link)

def LetterboxdPageScrapping(movie_page_link):
    '''
    ----- Arguments -----
    movie_page_link (str): This is the second half of the link to the page on Letterboxd containg
                        information about a specific movie. In the format of /film/{movie_name}/
    ----- Outputs -----
    movie_year (str): The year the movie released
    movie_normal_name (str): The unformatted name of the movie (written the way a human would type)
    movie_rating (str): Average rating of the movie on Letterboxd. Out of five. 
    movie_runtime (str): Length of the movie in minutes

    ----- Functions Used -----
    LetterboxdCalculateAverage
    
    ----- Description -----
    This function gets the specific movie page given in the movie_page_link argument and finds 
    out information about that movie. If there is no average rating calculating for a movie
    (this occurs when the movie doesn't have a lot of logged reviews) then another function is
    called to scrap through what reviews are logged and calculate the average from that

    '''
    url = 'https://letterboxd.com{}'.format(movie_page_link)
    r = requests.get(url)
    film_data = r.text.split('filmData = { ')[1]
    if 'releaseYear:' in film_data:
        movie_year = film_data.split('releaseYear: "')[1].split('"')[0]
        movie_runtime = film_data.split('runTime: ')[1].split(' ')[0]
        movie_normal_name = film_data.split('alt="')[1].split('"')[0]
    if 'content="Average rating"' in r.text:    
        movie_rating = r.text.split('content="Average rating"')[1].split('content="')[1].split(' ')[0]
    else:
        movie_rating = LetterboxdCalculateAverage(movie_page_link)
    
    return(movie_year, movie_normal_name, movie_rating, movie_runtime)


def LetterBoxd_1000List():
    '''
    ----- Arguments -----
    None
    ----- Outputs -----
    letterboxd_movies (dict): This is a dictionary containing information about all the movies on the
                                Letterboxd list "Letterboxd's Top 1,000 Narrative Feature Films". The
                                keys are the names of the movies formated as Letterboxd internally
                                formats them and the values are the normal movie name and the link 
                                to its search page (the results of searching this name on Letterboxd)
    ----- Functions Used -----
    None

    ----- Description -----
    This function goes to the list on Letterboxd with the top 1000 highest rated movies and gets the
    name for each of those movies along with the link to its specific Letterboxd page. It also finds
    the name with which Letterboxd internally uses to refer to this movie and sets that as the key 
    for the output dictionary. This might seem strange but since all movies will eventually be searched
    for on Letterboxd and Letterboxd has a very specific format for movie names it makes sense to 
    use this as the most prominent key. By using the search engine of Letterboxd any movie name 
    (as long as its reasonably close to the Letterboxd one) can be converted to the Letterboxd format
    but the opposite is not true. Thus the Letterboxd formate becomes the universe one. 
    '''
    
    # Initialize dictionary to store all movies and their information in
    letterboxd_movies = {}
    # Loop through the pages of the list
    for i in range(1, 12):
        if i == 1:
            url = 'https://letterboxd.com/thediegoandaluz/list/letterboxds-top-1000-narrative-feature-films/'
        else:
            url = 'https://letterboxd.com/thediegoandaluz/list/letterboxds-top-1000-narrative-feature-films/page/{}'.format(i)
        r = requests.get(url)
        # Format the results
        table = r.text.split('list-entries')[1].split('numbered-list-item')[1:]
        # Scrape movie name from the list page and format it correctly
        for j in range(0,len(table)):
            normal_name = table[j].split('alt="')[1].split('"')[0]
            movie_name = table[j].split('data-film-slug="')[1].split('"')[0]
            movie_page_link = table[j].split('data-target-link="')[1].split('"')[0]
        
            # Now save the movie name as a key in the dictionary that will eventually contain all movies
            letterboxd_movies[movie_name] = {'normal_name': normal_name,\
                                                'movie_page_link': movie_page_link}
    return(letterboxd_movies)


def LetterboxdCalculateAverage(movie_page_link):
    '''
    ----- Arguments -----
    movie_page_link (str): This is the second half of the link to the page on Letterboxd containg
                        information about a specific movie. In the format of /film/{movie_name}/
    ----- Outputs -----
    score (float): This is the calculated average for users ratings on a specific movie out of 5

    ----- Functions Used -----
    None

    ----- Description -----
    This function calculates the average rating of a movie denoted by the page link given to the
    funcion. It does this by making a list of all user ratings (something out of five) and then
    finding the average of that. The only complicated part is that Letterboxd does not set a limit
    itself on the number of pages of user reviews so even if there are only two pages populated with
    reviews you can still visit the empty pages up to infinity. So a check must be done to make sure
    that the function is scaping pages that actually have content on them. 
    '''

    url = 'https://letterboxd.com{}'.format(movie_page_link) + 'members/by/rating/'
    score = []
    stop = 0
    i = 0
    while stop != 1:
        stop = 1
        if i > 0:
            url = 'https://letterboxd.com{}'.format(movie_page_link) + 'members/by/rating/page/{}/'.format(i)
        r = requests.get(url)
        # Checks if the page has actual reviews or is just empty. If its empty then it
        # tells the loop to stop and that we've iterated through all the pages
        if 'class="table-person"' in r.text:
                stop = 0
        if stop != 1:
            ratings = r.text.split('rating rated')[1:]
            for row in ratings:
                stars = row.split('> ')[1].split(' <')[0]
                score.append(stars.count('★') + (0.5 *stars.count('½')))
        i += 1
    if len(score) == 0:
        return('-1')

    return('{:.2f}'.format(sum(score) / len(score)))


def FormatName(name):
    '''
    ----- Arguments -----
    name (str): The name of a movie
    ----- Outputs -----
    name (str): The name of a movie in the specific Letterboxd formatting
    ----- Functions Used -----
    None
    ----- Description -----
    This is a bit of a silly one but basically it helps to return the correct results from 
    searchs when the name of the movie is as close as possible to the stored Letterboxd name. The 
    search engine Letterboxd uses is not very good. Thus this is hard coding a couple of the rules
    that Letterboxd uses in its formating. I couldn't catch everything in default python but this
    gets close enough to then simply grab the formatted name from Letterboxd itself. 
    '''

    name = name.replace('-', ' ')
    for pun in string.punctuation:
        name = name.replace(pun, '')
    name = name.replace(' ', '-').lower()
    name = name.replace('½', '-half').replace('’', '').replace('–', '-').replace('·', '')
    # Now get rid of any weird spaces caused by removed punctation being filled with dashes
    name = name.replace('---', '-')
    name = name.replace('--', '-')

    '''
    I know this is one of the dumbest ways to do this but I wanted to work with default python
    and didn't know how else to do this without the unidecode library or something like that. 
    Just wanted to put a disclaimer that I know theres much much MUCH better ways of doing this. 
    '''
    name = name.replace('á','a')
    name = name.replace('é','e')
    name = name.replace('í','i')
    name = name.replace('ó','o')
    name = name.replace('ú','u')
    name = name.replace('ý','y')
    name = name.replace('à','a')
    name = name.replace('è','e')
    name = name.replace('ì','i')
    name = name.replace('ò','o')
    name = name.replace('ù','u')
    name = name.replace('ä','a')
    name = name.replace('ë','e')
    name = name.replace('ï','i')
    name = name.replace('ö','o')
    name = name.replace('ü','u')
    name = name.replace('ÿ','y')
    name = name.replace('â','a')
    name = name.replace('ê','e')
    name = name.replace('î','i')
    name = name.replace('ô','o')
    name = name.replace('û','u')
    name = name.replace('ã','a')
    name = name.replace('õ','o')
    name = name.replace('@','a')
    return name
