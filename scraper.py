import requests
from bs4 import BeautifulSoup

class Site:
    def __init__(self, name, link, name_finder, price_finder, review_finder, link_finder, image_finder):
        self.name = name
        self.link = link
        self.name_finder = name_finder
        self.price_finder = price_finder
        self.review_finder = review_finder
        self.link_finder = link_finder
        self.image_finder = image_finder

class Category:
    def __init__(self, name):
        self.name = name

class ItemData:
    def __init__(self, name, category, site, link):
        self.name = name
        self.category = category
        self.site = site
        self.link = link
        

class SoupFinder:
    def __init__(self, tag, attrs, formatter):
        self.tag = tag
        self.attrs = attrs
        self.formatter = formatter

class Item:
    def __init__(self, name, price, review, link, image):
        self.name = name
        self.price = price
        self.review = review
        self.link = link
        self.image = image
        self.score = price/review

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

sites = {
    "JL": Site("John Lewis", "https://www.johnlewis.com",
                SoupFinder("span",{"class": "product-card__title-inner"}, lambda a : a.text), 
                SoupFinder("span",{"class": "product-card__price-span"}, lambda a : float(a.text.replace(",","")[1:a.text.index('.')+3])), 
                SoupFinder("span",{"class": "review-indicator-sprites"}, lambda a : float(a.text[39:43])),
                SoupFinder("a",{"class": "product-card__wrap-link"}, lambda a : "https://www.johnlewis.com"+a.get('href')),
                SoupFinder("img",{"class": "product-card__image"}, lambda a : a.get('src'))),
    "AZ": Site("Amazon", "https://www.amazon.co.uk",
                SoupFinder("h2",{"class": "a-text-normal"}, lambda a : a.text), 
                SoupFinder("span",{"class": "a-size-base a-color-price s-price a-text-bold"}, lambda a : float(a.text.replace(",","")[1:a.text.index('.')+3])), 
                SoupFinder("i",{"class": "a-icon-star"}, lambda a : float(a.text[:a.text.index(" ")])),
                SoupFinder("a",{"class": "s-color-twister-title-link"}, lambda a : a.get('href')),
                SoupFinder("img",{"class": "s-access-image"}, lambda a : a.get('src'))),
    "AG": Site("Argos", "https://www.argos.co.uk",
                SoupFinder("div",{"class": "ac-product-name"}, lambda a : a.text), 
                SoupFinder("span",{"class": "ac-product-price__amount"}, lambda a : float(a.text.replace(",","")[1:a.text.index('.')+3])), 
                SoupFinder("div",{"class": "ac-star-rating"}, lambda a : float(a.get('data-star-rating'))),
                SoupFinder("a",{"class": "ac-product-link ac-product-card__image"}, lambda a : "https://www.argos.co.uk"+a.get('href')),
                SoupFinder("div",{"class": "ac-product-image__proportion--square"}, lambda a : a.find("img").get('src')))
}
categories = {
    "TVs": Category("TVs"),
    "Headphones": Category("Headphones"),
    "Water Bottles": Category("Waterbottles")
}
item_data = {
    "JLTVs": ItemData("John Lewis TVs",
                      categories["TVs"],
                      sites["JL"],
                      "https://www.johnlewis.com/browse/electricals/televisions/all-tvs/_/N-6srf"),
    "JLHPs": ItemData("John Lewis Headphones",
                      categories["Headphones"],
                      sites["JL"],
                      "https://www.johnlewis.com/browse/electricals/headphones/headphones/_/N-al9"),
    "JLWBs": ItemData("John Lewis Waterbottles",
                      categories["Water Bottles"],
                      sites["JL"],
                      "https://www.johnlewis.com/browse/sport-leisure/gym-accessories/water-bottle/_/N-eyuZ1z075od"),
    "AZTVs": ItemData("Amazon TVs",
                      categories["TVs"],
                      sites["AZ"],
                      "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=TV"),
    "AZHPs": ItemData("Amazon Headphones",
                      categories["Headphones"],
                      sites["AZ"],
                      "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=Headphones"),
    "AZWBs": ItemData("Amazon Waterbottles",
                      categories["Water Bottles"],
                      sites["AZ"],
                      "https://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=Waterbottle"),
    "AGTVs": ItemData("Argos TVs",
                      categories["TVs"],
                      sites["AG"],
                      "https://www.argos.co.uk/search/tv/"),
    "AGHPs": ItemData("Argos Headphones",
                      categories["Headphones"],
                      sites["AG"],
                      "https://www.argos.co.uk/search/headphones/"),
    "AGWBs": ItemData("Argos Waterbottles",
                      categories["Water Bottles"],
                      sites["AG"],
                      "https://www.argos.co.uk/search/water-bottle/")
}

def getItems(i_data):
    page = requests.get(i_data.link, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")
    
    names = soup.find_all(i_data.site.name_finder.tag, attrs=i_data.site.name_finder.attrs)
    prices = soup.find_all(i_data.site.price_finder.tag, attrs=i_data.site.price_finder.attrs)
    reviews = soup.find_all(i_data.site.review_finder.tag, attrs=i_data.site.review_finder.attrs)
    links = soup.find_all(i_data.site.link_finder.tag, attrs=i_data.site.link_finder.attrs)
    images = soup.find_all(i_data.site.image_finder.tag, attrs=i_data.site.image_finder.attrs)
    items = []
    for i in range(min([len(names),len(prices),len(reviews),len(links),len(images)])):
        if not (i_data.site.name_finder.formatter(names[i])[1:10] == "Sponsored"):
            items.append(Item(i_data.site.name_finder.formatter(names[i]), i_data.site.price_finder.formatter(prices[i]), i_data.site.review_finder.formatter(reviews[i]), i_data.site.link_finder.formatter(links[i]), i_data.site.image_finder.formatter(images[i])))
    return items




def getAllItems(category):
    items = []
    for item in item_data:
        if item_data[item].category == category:
            items += getItems(item_data[item])
    return items

# items = getItems(item_data["AGHPs"])



if __name__ == "__main__":
    items = getAllItems(categories["Headphones"])

    sorted_items = sorted(items, key=lambda x: x.score)
    for item in sorted_items:
        print(item.name[0:10]+ " | " + "{:<12}".format(str(item.price)) + " | " + "{:<4}".format(str(item.review))+ " | "+str(item.score)[:5]+ " | "+str(item.link)[:20]+ " | "+str(item.image)[:20])