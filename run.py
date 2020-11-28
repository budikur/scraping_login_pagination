import requests
import bs4

def login():
    print('login...')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }

    res = requests.post('http://localhost:5000/')
    f = open('./res.html', 'w+')
    f.write(res.text)
    f.close()

def get_urls():
    print('getting urls...')

def get_detail():
    print('getting detail...')

def create_csv():
    print('csv generated...')

def run():
    login()
    get_urls()
    get_detail()
    create_csv()

if __name__ == '__main__':
    run()
