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

To customize the categories you want to explore, simply change the category in `settings.py`. Add (or replace) a category using its tag in [word.openfoodfact.org](https://world.openfoodfacts.org/). The full list of categories is available [on their website](https://world.openfoodfacts.org/categories.xml).

### Grant access to local database

[MySQL](https://dev.mysql.com/doc/refman/8.0/en/installing.html) must be installed and you must know the login and password to connect to this client.
`CREATE USER 'id'@'localhost' IDENTIFIED BY 'password';`

Then run setup.py
```bash
python setup.py
```

## Running it

Simply download the repo and run main
```bash
python main.py
```

## Features

Using the terminal select "Find a substitute" OR "My food"

## License

Foodstitute python script is licensed under the terms of the GPL Open Source
license and is available for free.

## Links

* [Open Classroom](https://openclassrooms.com)
* [Open Food Facts](https://world.openfoodfacts.org/)
