import requests

def get_book_details(isbn):
    x = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+isbn).json()
    output = dict()
    if x['totalItems'] >= 1:
        output['title'] = x['items'][0]['volumeInfo']['title']
        output['authors'] = ', '.join(x['items'][0]['volumeInfo']['authors'])
        output['pageCount'] = x['items'][0]['volumeInfo']['pageCount']
        output['maturityRating'] = x['items'][0]['volumeInfo']['maturityRating']

    return output