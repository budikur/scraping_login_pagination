import requests
import bs4

url = 'http://localhost:5000/'
content = requests.get(url)
#print(content.text)
asd = bs4.BeautifulSoup(content.text, "html.parser")
#print(asd)

