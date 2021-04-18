import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import Movie
import imdb

ia = imdb.IMDb()
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
        all_movies[current_movie.box.get('name')] = current_movie.box



#Cleans up 'Running Time'
def clean_time():
    for item in all_movies:
        try:
            if '–' in all_movies[item]['Running time']:my_time = all_movies[item]['Running time'].split('–',1)
            else: my_time = all_movies[item]['Running time'].split(' ',1)
            print(my_time[0])
            all_movies[item]['Running time'] = int(my_time[0])
        except AttributeError:
            my_time=all_movies[item]['Running time'][0]
            my_time = my_time.split(' ', 1)
            print(my_time[0])
            all_movies[item]['Running time'] = int(my_time[0])
        except KeyError:
            print(item,'does not have running time key')

#cleans up 'Budget' and 'box office'
#uses USD
def clean_money():
    for item in all_movies:
        if 'Budget' in all_movies[item]:
            if type(all_movies[item]['Budget']) is str:
                clean = clean_string_usd(all_movies[item]['Budget'])
                if clean : all_movies[item]['Budget'] = clean
                else : print('failed budget string',all_movies[item]['Budget'])
            if type(all_movies[item]['Budget']) is list:
                clean = clean_list(all_movies[item]['Budget'])
                if clean :all_movies[item]['Budget'] = clean
                else : print('failed list',all_movies[item]['Budget'])
        if 'Box office' in all_movies[item]:
            if type(all_movies[item]['Box office']) is str:
                temp = clean_string_usd(all_movies[item]['Box office'])
                if temp :
                    all_movies[item]['Box office'] = temp
                else: print('failed',all_movies[item]['Box office'])
            if type(all_movies[item]['Box office']) is list:
                temp = clean_list(all_movies[item]['Box office'])
                if temp:
                    all_movies[item]['Box office'] = clean
                else : print('failed list',all_movies[item]['Box office'])

def clean_string_usd(my_string):
    if '$' in my_string:
        while '(' in my_string and '$' in my_string[my_string.find('(')+1:my_string.find(')'):]:
            my_string= my_string[my_string.find('(')+1:my_string.find(')'):]
        start = my_string.find('$')
        end = my_string.find('million')
        if end == -1:
            end = my_string.find('billion')
        if end == -1: end = len(my_string)
        my_string = my_string[start:end:].replace(' ','').replace('\n','').replace('\xa0','').\
            replace('to','-').replace('–','-').replace('$','').replace('est.','')
        if '-' in my_string:
            my_string = my_string.split('-',3)[0]
        if ',' in my_string:
            if len(my_string) > 7 :
                my_string = my_string[0:2].replace(',','.')
            else : my_string = '0.' + my_string[0:my_string.find(','):]
    try:
        my_float = float(my_string) * 1000000
        print(int(my_float))
        return int(my_float)
    except ValueError:
        return clean_string_other_currency(my_string)
def clean_list(my_list):
    summe = False
    for item in my_list:
        current = clean_string_usd(item.replace('\xa0',' '))
        if current:
            summe += current
    return summe

def clean_string_other_currency(my_string):
    if '–' in my_string:
        my_string = my_string.split('–')[0]
    while '(' in my_string:
        my_string = my_string[my_string.find('('):my_string.find(')'):]
        return clean_string_usd(my_string)
    if ( '₹' and 'million' )in my_string:
        return int(my_string[my_string.find('₹')+1:my_string.find('million'):].replace(' ',''))*13285
    if ( '₹' and 'billion' )in my_string:
        return int(my_string[my_string.find('₹')+1:my_string.find('billion'):].replace(' ','').replace('.',''))*1328500
    if ( '₹' and 'crore' )in my_string:
        return int(my_string[my_string.find('₹')+1:my_string.find('crore'):].replace(' ','').replace(',','.'))*132850
    if 'crore' in my_string:
        return int(my_string.replace('crore','').replace(' ', '')) * 132850
    else:
        return False


def clean_date_simple():
    for date_item in all_movies:
        my_date =  datetime.now()
        date_dict ={}
        if 'Release date' in all_movies[date_item]:
            my_release_date_string =  all_movies[date_item]['Release date']
            if type(all_movies[date_item]['Release date']) is list :
                my_release_date_string = all_movies[date_item]['Release date'][0].replace('\xa0','-')
            if '(' in my_release_date_string:
                start =my_release_date_string.find('(')
                try:
                    my_release_date_string = my_release_date_string[0:start:1].replace(' ','-').replace(',','-').replace('--','-')
                    my_release_date_string = my_release_date_string[0:len(my_release_date_string)-1]
                    date_array = my_release_date_string.split('-',3)
                    for item in date_array:
                        if item in months:
                            date_array[date_array.index(item)] = months[item]
                            date_dict['m'] = months[item]
                    for item in date_array:
                        if type(item) is int and date_array.index(item) != 0:
                            temp = date_array[0]
                            in_temp = date_array.index(item)
                            date_array[0] = item
                            date_array[in_temp] = temp
                        if type(item) is str and len(item)>2:
                            date_dict['y'] = int(item)
                        else : date_dict['d'] = int(item)
                    all_movies[date_item]['Release date'] = str(datetime.strptime(str(date_dict['d'])+'/'+str(date_dict['m'])+'/'+str(date_dict['y']),'%d/%m/%Y').date())
                    print(all_movies[date_item]['Release date'])
                except TypeError:
                    print('error',my_release_date_string)
                except KeyError as exception:
                    if exception.args == ('d',):
                        all_movies[date_item]['Release date'] = str(datetime.strptime(str(date_dict['y']),'%Y').date())
                    else : print(exception)

def clean_titles():
    for movie in all_movies:
        temp = all_movies[movie]['name']
        if ('(' and ')') in temp:
            temp = temp[0:temp.find('('):]
            print(temp)
            all_movies[movie]['name'] = temp
def imdb_search():
    for movie in all_movies:
        title = all_movies[movie]['name']
        try:
            year = int(all_movies[movie]['Release date'][0:4:])
            table = ia.search_movie(title)
            #print(table)
            for item in table:
                if item['title'] == title and item.values()[2] == year :
                    movie_imdb = ia.get_movie(item.movieID)
                    print(title,year,movie_imdb['rating'])
                    all_movies[movie]['Rating']=movie_imdb['rating']
                    break
        except ValueError:
            for item in table:
                if item['title'] == title:
                    #print(item.values())
                    print('NO MATCHING DATE|| ID', item.movieID, item['title'], item.values()[2])
                    pass

        except KeyError:
            print('will skip', movie)
            pass

all_movies = load_data()
imdb_search()