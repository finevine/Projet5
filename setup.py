'''
Setup of Foodstitute
'''
import settings
import model

def main():
    db = model.DataBase()
    db.create_tables()
    for category in settings.CATEGORIES:
        db.feed_database(model.Category(category))
    # breakpoint()
    # print(Category('nuts').get_api_products())
    db.connection.commit()
    db.connection.close()


if __name__ == "__main__":
    main()
