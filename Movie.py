import requests
from bs4 import BeautifulSoup


class Movie:
    link = str
    name = str
    box = dict

    @property
    def get_info(self):
        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, 'html.parser')
        infobox = soup.find(class_='infobox vevent')


        if infobox and len(infobox) > 0:
            rows = infobox.find_all('tr')
            for index, row in enumerate(rows):
                if index == 0 or index == 1:
                    continue
                elif row.find('th') and row.find('td'):
                    key = row.find('th').get_text(" ", strip=True).replace('\xa0', " ")
                    value = row.find('td')
                    self.box[key] = self.get_text(value)
            return True
        else:
            return False

    def print_info(self):
        print('####################')
        for item in self.box:
            print(item, ':', self.box[item])


    def __init__(self, name, link):
        self.name = name
        self.link = link
        self.box = {}
        self.box['name']=self.name
        self.box['link']=self.link
        self.get_info
        self.print_info()

    def get_text(self, tag):
        if tag.find('li'):
            temp = [self.clean_string_from_references(
                item.get_text(" ", strip=True).replace('\xa0', " "))
                for item in tag.find_all('li')]
            if len(temp) > 1 : return temp
            else: return temp[0]
        elif tag.find('br'):
             temp = [self.clean_string_from_references(
                item) for item in tag.stripped_strings]
             if len(temp) > 1:
                 return temp
             else:
                 return temp[0]
        else:
             return self.clean_string_from_references(
                tag.get_text(" ", strip=True).replace('\xa0', " "))

    def clean_string_from_references(self, string):
        my_string = string
        while '[' and ']' in my_string:
            one = my_string.find('[')
            two = my_string.find(']')
            my_string = my_string[:one] + my_string[two + 1:]
        return my_string
