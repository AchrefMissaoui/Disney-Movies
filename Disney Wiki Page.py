import requests
from bs4 import BeautifulSoup

LINK = 'https://en.wikipedia.org/wiki/Disney_Channel'
page = requests.get(LINK)
soup = BeautifulSoup(page.content,'html.parser')
infobox = soup.find(class_='infobox vcard')
labels = infobox.find_all(class_='infobox-label')
data = infobox.find_all(class_='infobox-data')
box = {}
i = 0
while i < len(labels) - 1 :
    box[labels[i].get_text(" ",strip=True)] = data[i].get_text(" ",strip=True).replace('\xa0',' ')
    i+=1

for item in box :
    print(item,':',box[item])