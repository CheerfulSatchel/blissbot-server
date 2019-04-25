from .models import Article
from .database import Base, sql_engine, Database_Session
from sqlalchemy.sql.expression import func, select


def create_tables(table_names):
    for table_name in table_names:
        if not sql_engine.dialect.has_table(sql_engine, table_name):
            if table_name == 'articles':
                Article.__table__.create(sql_engine)
        else:
            print('Table {} already exists!'.format(table_name))


def fetch_random_article():
    row = None
    retrieved_entry = Database_Session.query(
        Article).order_by(func.random()).first()
    if retrieved_entry:
        rowId = retrieved_entry.id
        row = Database_Session.query(Article).get(rowId)

    return row


if __name__ == '__main__':
    table_names = ['articles']
    create_tables(table_names)

    fetch_random_article()
