import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'parsegarfieldby.settings'
django.setup()

import json
from parsed.models import Site, Animal, Category, Product

URL_GARFIELD = 'https://garfield.by/'
DATA_FOLDER = 'parsed_from_garfield/'
NAV_LINKS_PATH = DATA_FOLDER + 'nav_links.json'
CATEGORIES_LINKS_PATH = DATA_FOLDER + 'categories_links.json'
PRODUCTS_FILE_NAME = 'products.json'

# insert site info

# s = Site(name='Garfield', url=URL_GARFIELD)
# s.save()

# insert animal types

# with open(NAV_LINKS_PATH, 'r') as file:
#     animals_nav_links = json.load(file)
#
# print(animals_nav_links)
#
# site = Site.objects.get(name='Garfield')
# print(site)
# for name, url in animals_nav_links.items():
#     a = Animal(type=name, url=url)
#     a.save()
#     a.site.set([site])
#     a.save()
#     print(a)

# insert categories

# with open(CATEGORIES_LINKS_PATH, 'r') as file:
#     categories_by_animal = json.load(file)

# animals = Animal.objects.all()
#
# animals_dict = {}
# for animal in animals:
#     animals_dict[animal.type] = animal

# for animal_type, categories in categories_by_animal.items():
#     a = animals_dict[animal_type]
#     for name, url in categories_by_animal[animal_type]['categories'].items():
#         c = Category(name=name, url=url, animal=a)
#         c.save()
#         print(c)

# insert products

animals = Animal.objects.all()
animals_dict = {}
for animal in animals:
    animals_dict[animal.type] = {'obj': animal, 'categories': {}}

categories = Category.objects.all()
for category in categories:
    animals_dict[category.animal.type]['categories'][category.name] = category

file_number = 11
count = 0
while True:
    file_path = f'{DATA_FOLDER}{file_number:04d}_{PRODUCTS_FILE_NAME}'
    try:
        file = open(file_path, 'r')
        print(f'Parsing {file_path}...')
        products_dict = json.load(file)
    except FileNotFoundError:
        print('All files loaded.')
        break
    finally:
        file.close()

    animal = animals_dict[iter(products_dict.keys()).__next__()]['obj']
    for category_name in products_dict[animal.type]:

        category = animals_dict[animal.type]['categories'][category_name]
        for product in products_dict[animal.type][category_name]['products']:

            cost_list = product['cost'].split()
            cost = 0
            if len(cost_list) > 0:
                cost = float(cost_list[0].replace(',', '.'))

            p = Product(
                name=product['name'],
                description=product['description'],
                image_url=product['image_url'],
                amount=product['amount'],
                cost=cost,
                category=category
            )

            p.save()

            count += 1
            if count % 50 == 0:
                print(f'50 more products added to {category_name} for {animal.type}')

    file_number += 1

print(f'{count} products inserted.')
