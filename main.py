import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

db_login = 'postgres'
db_password = '********'
db_name = 'netology_homework'

DSN = f'postgresql://{db_login}:{db_password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(engine)
session = Session()

create_tables(engine)


def import_data():
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

        for record in data:
            model = {
                'publisher': Publisher,
                'shop': Shop,
                'book': Book,
                'stock': Stock,
                'sale': Sale,
            }[record.get('model')]
            session.add(model(id=record.get('pk'), **record.get('fields')))
        session.commit()


def publisher_search_name():
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите имя (name) издателя: ')
    query_result = query_join.filter(Publisher.name == query_publisher_name)
    for result in query_result.all():
        print(f'Издатель "{query_publisher_name}" реализуется в магазине "{result.name}" с идентификатором {result.id}')


def publisher_search_id():
    query_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    query_publisher_name = input('Введите идентификатор издателя: ')
    query_result = query_join.filter(Publisher.id == query_publisher_name)
    for result in query_result.all():
        print(
            f'Издатель c id: {query_publisher_name} реализуется в магазине "{result.name}" '
            f'с идентификатором {result.id}')


if __name__ == '__main__':
    import_data()
    publisher_search_name()
    publisher_search_id()
