import requests
from bs4 import BeautifulSoup
import json
import Movie

LINK = 'https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films'
all_movies = {}
movies = []


def save_data(data):
    with open('collectedMovies.json', 'w', encoding='utf-8') as f:
        json.dump(data,f,indent=2)


def load_data():
    with open('collectedMovies.json', 'r', encoding='utf-8') as f:
        return json.load(f)



page = requests.get(LINK)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.select('.wikitable.sortable i a')
for item in tables:
    current_movie = Movie.Movie(item['title'], 'https://en.wikipedia.org' + item['href'])
    current_box = current_movie.box
    my_box = {}
    for item in current_box :
        my_box[item]=current_box[item]
    all_movies[current_box.get('name')]=my_box

print(all_movies)
print(movies)
save_data(all_movies)

#TODO : https://www.youtube.com/watch?v=Ewgy-G9cmbg&t=236s |||| clean data task
