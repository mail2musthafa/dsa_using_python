import csv
import os
import requests
from bs4 import BeautifulSoup

baseurl = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

r = requests.get(baseurl)

books_soup = BeautifulSoup(r.content, features="html.parser")

data = {"product_page_url": [],
       "title": [],
       "universal_product_code": [],
       "price_including_tax": [],
       "price_excluding_tax": [],
       "number_available": [],
       "category": [],
       "review_rating": []
       }

book_page_lists = books_soup.find("ol", class_="row").find_all("li")

for li in book_page_lists:
   href_split = li.a['href'].split("/")[3:]
   book_page_link = "http://books.toscrape.com/catalogue/" + "/".join(href_split)
   req = requests.get(book_page_link)
   soup = BeautifulSoup(req.content, features="html.parser")

   data['product_page_url'].append(book_page_link)

   table = soup.find("table")
   rows = table.find_all("tr")

   title = soup.find("h1").text
   desc = soup.find("article", class_= "product_page").find_all("p")[3].text.strip()
   category = soup.find("ul", class_="breadcrumb").find_all("li")[2].a.text.strip()
   review_rating = soup.find("p", class_="star-rating")['class'][1]

   data["title"].append(title)
   data["universal_product_code"].append(rows[0].find("td").text.strip())
   data["price_excluding_tax"].append(rows[2].find("td").text.strip())
   data["price_including_tax"].append(rows[3].find("td").text.strip())
   data["number_available"].append(rows[5].find("td").text.strip())
   data["category"].append(category)
   data["review_rating"].append(review_rating)

import pandas as pd 
df = pd.DataFrame(data = data)
df.to_csv("sub.csv", index = False)