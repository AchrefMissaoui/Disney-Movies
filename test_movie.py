import requests
from bs4 import BeautifulSoup

#class to use to test error

LINK = 'https://en.wikipedia.org/wiki/Westward_Ho_the_Wagons!'
page = requests.get(LINK)
soup = BeautifulSoup(page.content, 'html.parser')
infobox = soup.find(class_='infobox vevent')
labels = infobox.find_all(class_='infobox-label')
data = infobox.find_all(class_='infobox-data')
box = {}
i = 0
while i < len(labels) - 1:
    all_breaks = data[i].find_all('br')
    if len(all_breaks) > 1:
        print('found br')
        temp = []
        for item in all_breaks:
            string_to_put = item.nextSibling.get_text(" ", strip=True).replace('\xa0', '')
            while '[' and ']' in string_to_put:
                one = string_to_put.find('[')
                two = string_to_put.find(']')
                string_to_put = string_to_put[:one] + string_to_put[two + 1:]
            temp.append(string_to_put)
    else:
        temp = data[i].get_text(" ", strip=True).replace('\xa0', '')
        while '[' and ']' in temp:
            one = temp.find('[')
            two = temp.find(']')
            temp = temp[:one] + temp[two + 1:]
    box[labels[i].get_text()] = temp
    i += 1


print(box)

