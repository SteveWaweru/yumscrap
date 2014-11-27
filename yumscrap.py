__author__ = 'steve_w'

from urllib2 import urlopen
from bs4 import BeautifulSoup


def get_locations(url):
    """
    Function gets the url of yum website and gets the locations of the restuarants and convert them to linkable url
    :param url: link to yum webiste
    :return: list of locations
    """
    soup = BeautifulSoup(urlopen(url))
    locations = soup.find_all("option")
    locations = [location.text.encode(soup.original_encoding).lower().replace(' ', '-').replace('--', '').replace('(', '').replace(')', '').replace('/', '').replace('.', '') for location in locations]
    locations.pop(0)
    return locations


def get_restruarants(url):
    """
    Function to get all the restuarant names and links from the yum website yum.co.ke/neigbourhood/<location>
    :param url: Url of website
    :return: list tuple of restuarant name and its href link
    """
    soup = BeautifulSoup(urlopen(url))
    content = soup.findAll("p", {"class": "name"})
    restuarant_link = []
    for cont in content:
        restuarant = cont.text.encode(soup.original_encoding)
        link = cont.findAll("a", href=True)[0]['href']
        restuarant_link.append((restuarant, link))
    return restuarant_link


# TODO: Getting categories with the food items
def get_menu(url):
    """
    Funtion that loops to all menu menu items on a location url given and returns a list tuple of the name, description
    and price of the food
    :param url: location url
    :return: list tuple of name, description and price of food.
    """
    soup = BeautifulSoup(urlopen(url))
    items = soup.find_all('li', {'class': 'menuItem'})
    menu = []
    for item in items:
        food_name = item['itemname']
        food_description = item['description'].replace('\r\n', ' ')
        food_price = item['price']
        # print item.find_all('p', {'class': 'name'})
        # food_name = item.find_all('p', {'class': 'name'})[0].text.encode(soup.original_encoding)
        # food_description = item.find_all('p', {'class': 'info'})[0].text.encode(soup.original_encoding)
        # food_price = item.find_all('span', {'class': 'pricenr'})[0].text.encode(soup.original_encoding)
        menu.append((food_name, food_description, food_price))
    return menu


yum_neigborhood = 'http://yum.co.ke/neighborhood/'
yum = 'http://yum.co.ke'

locations = get_locations(yum)
for location in locations:
    print location
    restuarants = get_restruarants(yum_neigborhood + location)
    print restuarants
    for restuarant in restuarants:
        print restuarant[0]  # First element of a tuple that represents that name of the restuarant
        menu = get_menu(yum + restuarant[1])  #
        print menu