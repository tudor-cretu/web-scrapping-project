from _ast import Lambda
from bs4 import BeautifulSoup
import requests
import re

product = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?d={product}&N=4131" # the f is because of the variable in the link
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_text = doc.find(class_ = "list-tool-pagination-text").strong
#print(page_text)
pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
# print(pages)

items_found = {}

for page in range(1, pages + 1): # so to not start at 0
    url = f"https://www.newegg.ca/p/pl?d={product}&N=4131&page={page}"  # the f is because of the variable in the link
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    div = doc.find(class_ = "item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(product)) # without re.compile it would take just strings with "product_name" not "product_name word" for example

    for item in items:
        parent = item.parent
        if parent.name != "a":
            continue

        link = parent['href']
        #print(link)

        next_parent = item.find_parent(class_= "item-container")
        try:
            price = next_parent.find(class_ = "price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
            #print(price)
        except:
            pass

#print(items_found)

#sorting products prices

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("--------------------------------------------")