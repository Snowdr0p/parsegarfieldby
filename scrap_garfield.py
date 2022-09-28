import requests
import json
from bs4 import BeautifulSoup
from time import sleep
from random import random

URL_GARFIELD = 'https://garfield.by/'
DATA_FOLDER = 'parsed_from_garfield/'
NAV_LINKS_PATH = DATA_FOLDER + 'nav_links.json'
CATEGORIES_LINKS_PATH = DATA_FOLDER + 'categories_links.json'
PRODUCTS_FILE_NAME = 'products.json'


# get links to page with products for animal type

# print(f'Requesting "{URL_GARFIELD}"')
# r = requests.get(URL_GARFIELD)
# soup = BeautifulSoup(r.text, 'html.parser')
#
# print('Getting nav links')
# links_container_class = 'header-container'
# link_class = 'header-nav__link'
# nav_links = soup.select(f'.{links_container_class} > a.{link_class}')
#
# print('Creating nav dictionary')
# links_dict = {}
# for tag in nav_links:
#     key = tag.string
#     if not key:
#         continue
#     key = key.strip()
#     url = tag['href'].strip()
#     links_dict[key] = URL_GARFIELD + url[1:]
#
# print(f'\nSaving nav links to "{NAV_LINKS_PATH}"')
# with open(NAV_LINKS_PATH, 'w') as file:
#     json.dump(links_dict, file, indent=4, ensure_ascii=False)
# print('Links saved.')
#
#
# # get links for products categories for each animal types
#
# print('Getting links for categories...')
#
# links_dict = {}
# with open(NAV_LINKS_PATH, 'r') as file:
#     links_dict = json.load(file)
#
#
# products_by_categories = {}
# for name, link in links_dict.items():
#     r = requests.get(link)
#
#     soup = BeautifulSoup(r.content, 'html.parser')
#
#     nav_menu = soup.select('ul.item-selected-list > li > a')
#
#     categories = {}
#     for a in nav_menu:
#         categories[a.get_text(strip=True)] = URL_GARFIELD + a.get('href')[1:]
#
#     products_by_categories[name] = {
#         'url': link,
#         'categories': categories,
#     }
#
# with open(CATEGORIES_LINKS_PATH, 'w') as file:
#     json.dump(products_by_categories, file, ensure_ascii=False, indent=4)
#
# print(f'Links to categories saved to {CATEGORIES_LINKS_PATH}')

# get products cards

categories_links = {}
with open(CATEGORIES_LINKS_PATH, 'r') as file:
    categories_links = json.load(file)


# one iteration counts as parsing all products in single category
iter_number = 0
skip_iterations = 0
for name in categories_links:

    for category_name, category_url in categories_links[name]['categories'].items():
        iter_number += 1
        if iter_number <= skip_iterations:
            continue

        products_dict = {name: {}}
        print(f'Parsing products from "{category_name}".')

        products_dict[name][category_name] = {'url': category_url}

        r = requests.get(category_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        last_page_li = soup.select('div.bx_pagination_page > ul > li:nth-last-child(2)')
        number_of_pages = 1
        if last_page_li:
            number_of_pages = int(last_page_li[0].get_text(strip=True))

        print(f'{category_name} has {number_of_pages} pages with products.')

        products_in_category = []
        for page_number in range(1, number_of_pages + 1):
            print(f'Parsing page {page_number}/{number_of_pages} from "{category_name}"')
            # delay = round(0.5 + random()  * 2, 2)
            # print(f'Request delayed by {delay} seconds.')
            # sleep(delay)
            page_url = category_url + f'?PAGEN_1={page_number}&SIZEN_1=18'

            r_page = None
            while not r_page:
                try:
                    r_page = requests.get(page_url, timeout=5)
                except requests.exceptions.ConnectTimeout:
                    print('Connection timeout. Resending request...')

            page_soup = BeautifulSoup(r_page.content, 'html.parser')

            products_containers = page_soup.select('div.product-item-container')

            for product in products_containers:
                product_name = product.find(class_='product-item-title').a.get_text(strip=True)
                product_description = product.find(class_='product-item-preview-text').get_text(strip=True)
                product_image_url = URL_GARFIELD + \
                                    product.find(class_='product-item-image-wrapper').img.get('src')[1:]

                p_amount = product.find(class_='product-item-list-proposal__pack')
                product_amount = 'за 1 ед.'
                if p_amount:
                    product_amount = p_amount.get_text(strip=True)

                proposal = product.find(class_='product-item-list-proposal__discount_new') or \
                           product.find(class_="product-item-list-proposal__discount") or \
                           product.find(class_="product-item-price-current") or \
                           product.find(class_="product-item-list-proposal__cost") or \
                           product.find(class_="product-item-list")

                product_cost = proposal.get_text(strip=True)

                products_in_category.append({
                    'name': product_name,
                    'description': product_description,
                    'image_url': product_image_url,
                    'amount': product_amount,
                    'cost': product_cost,
                })

        products_dict[name][category_name]['products'] = products_in_category

        with open(f'{DATA_FOLDER}{iter_number:04d}_{PRODUCTS_FILE_NAME}', 'w') as file:
            json.dump(products_dict, file, ensure_ascii=False, indent=4)
