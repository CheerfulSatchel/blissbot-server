from models import Article
from database import Base, sql_engine


def create_tables(table_names):
    for table_name in table_names:
        if not sql_engine.dialect.has_table(sql_engine, table_name):
            if table_name == 'articles':
                Article.__table__.create(sql_engine)
        else:
            print('Table {} already exists!'.format(table_name))


if __name__ == '__main__':
    table_names = ['articles']
    create_tables(table_names)
