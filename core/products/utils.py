import requests
from bs4 import BeautifulSoup

def scrape_books():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    for article in soup.select('article.product_pod'):
        title = article.h3.a['title']
        price = article.select_one('p.price_color').text
        availability = article.select_one('p.instock').text.strip()
        
        books.append({
            'title': title,
            'price': price,
            'availability': availability
        })
    
    return books