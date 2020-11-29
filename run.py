import glob
import json
import requests
import bs4
import pandas as pd

session = requests.session()

def login():
    print('login....')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }
    res = session.post('http://localhost:5000/login', data=datas)
    # THIS IS FOR CHECK THE LOGIN IS SUCCESFULL OR NOT
    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_pages = len(page_item)-2
    return total_pages

def get_urls(page):
    print('getting urls.... page {}'.format(page))
    params = {
        'page': page
    }
    res = session.get('http://localhost:5000/', params=params)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)
    # THIS IS FOR CHECK THE PAGE IS SUITABLE OR NOT
    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()
    return urls

def get_urls_from_file():
    print('getting urls....')
    params = {
        'page': 1
    }
    soup = bs4.BeautifulSoup(open('./res.html'), 'html.parser')
    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []
    for title in titles:
        url = title.find('a')['href']
        urls.append(url)
    print(urls)

def get_detail(url):
    print('getting detail.... {}'.format(url))
    res = session.get('http://localhost:5000'+url)
    # THIS IS FOR CHECK THE PAGE IS SUITABLE OR NOT
    # f = open('./res.html', 'w+')
    # f.write(res.text)
    # f.close()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ','')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Desription: ','')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description
    }
    # print(dict_data)

    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)

def create_csv():
    files = sorted(glob.glob('./results/*.json'))
    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

        df = pd.DataFrame(datas)
        df.to_csv('results.csv', index=False)

    print('csv generated....')

def run():
    total_pages = login()

    total_urls = []
    for i in range(total_pages):
        page = i+1
        urls = get_urls(page)
        total_urls += urls

    # THIS IS FOR CHECK TOTAL URLS IN THE LIST AND LEN OF LIST
    # print(total_urls)
    # print(len(total_urls))

    with open('all_urls.json', 'w') as outfile:
        json.dump(total_urls, outfile)

    with open('all_urls.json') as json_file:
        all_url = json.load(json_file)

    # THIS FOR TESTING IN 1 PRODUCT
    # get_detail('/takoyakids-lyla-racer-back-dress-terracota')

    for url in all_url:
        get_detail(url)

    create_csv()
    # THIS IS FOR PROCESS ON THE FILE WE HAVE ALREADY CREATED
    # get_urls_from_file()

if __name__ == '__main__':
    run()
