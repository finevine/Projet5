<img src="img/logo.png" alt="Foodstitute" title="Foodstitute" align="right" width="100px" />

Foodstitute
=================

Foodstitute is a class exercise for becoming a python developper.
It aims at finding food substitute using the terminal and all of that
amongst a few food categories which are stored (and customizable) in `settings.py`

The product's architecture can be found on [Open Food Facts wiki](https://en.wiki.openfoodfacts.org/API/Read/Product).

## Table of content

- [Setup](#setup)
- [Run Foodstitute](#running-it)
- [License](#license)
- [Links](#links)

## Setup

### Customize settings.py

To customize the categories you want to explore (**you can add as many categories as you want** please note that the more categories you add, the longer it will take to feed the local database!), simply change the categories in `settings.py`. Add (or replace) a category using its tag in [word.openfoodfact.org](https://world.openfoodfacts.org/). The full list of categories is available [on their website](https://world.openfoodfacts.org/categories.xml).

### Grant access to local database

[MySQL](https://dev.mysql.com/doc/refman/8.0/en/installing.html) must be installed and you must know the login and password to connect to this client.
`CREATE USER 'id'@'localhost' IDENTIFIED BY 'mypassword';`

Then run setup.py Password
```bash
python setup.py mypassword
```

**Caution:** running `setup.py` will discard all the Products TABLE in the database and feed it again with products of categories in `settings.py` 

## Running it

Simply download the repo and run main
```bash
python controller.py mypassword
```

## Features

You can find products that are sold in France.

Using the terminal select "Substitute a product." or "Manage favourites."

You can save favourites, display them in the terminal or delete them.

## License

Foodstitute python script is licensed under the terms of the GPL Open Source
license and is available for free.

## Links

* [Open Classroom](https://openclassrooms.com)
* [Open Food Facts](https://world.openfoodfacts.org/)
