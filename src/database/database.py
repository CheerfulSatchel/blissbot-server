import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pymysql.install_as_MySQLdb()

Base = declarative_base()

db_username = os.environ.get('BLISSBOT_DB_USERNAME')
db_password = os.environ.get('BLISSBOT_DB_PASSWORD')
db_name = os.environ.get('BLISSBOT_DB_NAME')
db_endpoint = os.environ.get('BLISSBOT_DB_ENDPOINT')
db_port = os.environ.get('BLISSBOT_DB_PORT')

sql_engine = create_engine(
    'mysql://{}:{}@{}/{}'.format(db_username, db_password, db_endpoint, db_name), echo=True)

Session = sessionmaker(bind=sql_engine)

Database_Session = Session()
