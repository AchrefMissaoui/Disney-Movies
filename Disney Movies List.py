import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import Movie

LINK = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'
all_movies = {}
movies = []
months ={ 'January' : 1, 'February' : 2 , 'March' : 3 , 'April':4,'May':5,'June' : 6,'July' : 7, \
'August' : 8, 'September' : 9,'October' : 10, 'November':11,'December' : 12 }

def save_data(data):
    with open('collectedMovies.json', 'w', encoding='utf-8') as f:
        json.dump(data,f,indent=2)


def load_data():
    with open('collectedMovies.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_info():
    page = requests.get(LINK)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.select('.wikitable.sortable i a')
    for item in tables:
        current_movie = Movie.Movie(item['title'], 'https://en.wikipedia.org' + item['href'])
        current_box = current_movie.box
        my_box = {}
        for item in current_box:
            my_box[item] = current_box[item]
        all_movies[current_box.get('name')] = my_box

    print(all_movies)
    print(movies)
    save_data(all_movies)
def clean_date() :
    for item in all_movies:
        print(all_movies[item]['Release date'])
        date = datetime
        if '(' in all_movies[item]['Release date']:
            date_array = all_movies[item]['Release date'].split('(', 1)[0]
            date_array = date_array.replace(',', '')
            date_array = date_array.split(' ', 2)
            date_dict = {}
            if date_array[0] in months:
                date_dict['month'] = months[date_array[0]]
                date_array.pop(0)
            if date_array[1] in months:
                date_dict['month'] = months[date_array[1]]
                date_array.pop(1)

            for spot in date_array:
                if len(spot) >= 3:
                    date_dict['year'] = spot
                else:
                    date_dict['day'] = spot

            if 'day' in date_dict and date_dict['day'] != '':
                print(date_dict['day'], '-', date_dict['month'], '-', date_dict['year'])
                date_string = str(date_dict['day']) + '/' + str(date_dict['month']) + '/' + str(date_dict['year'])
                date_string = date_string.replace(' ', '')
                print(date_string, type(date_string))
                date = datetime.strptime(date_string, '%d/%m/%Y')
                print(date.date(), type(date))
            else:
                print(date_dict['year'])
                date = datetime.strptime(date_dict['year'], '%Y')
            all_movies[item]['Release date'] = str(date.date())
get_info()
all_movies = load_data()
clean_date()
save_data(all_movies)




