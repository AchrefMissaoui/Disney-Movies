import requests
from bs4 import BeautifulSoup


class Movie:
    link = str
    name = str
    box = {}

    def get_info(self):
        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, 'html.parser')
        infobox = soup.find(class_='infobox vevent')
        if infobox is not None and len(infobox) > 0:
            labels = infobox.find_all(class_='infobox-label')
            data = infobox.find_all(class_='infobox-data')
            self.box['name'] = self.name
            self.box['link'] = self.link
            i = 0
            while i < len(labels) - 1:
                self.box[labels[i].get_text(" ",strip=True)] = data[i].get_text(" ",strip=True).replace('\xa0',' ')
                i += 1
            return True
        else:
            return False

    def print_info(self):
        print('####################')
        print(self.name)
        print('--------------------')
        for item in self.box:
            print(item, ':', self.box[item])
        print('####################')

    def __init__(self, name, link):
        self.name = name
        self.link = link
        if self.get_info():
            print('got info on movie with name', self.name, 'from', self.link)
            print(self.box)
        else:
            print(self.name, 'is not a movie!')
