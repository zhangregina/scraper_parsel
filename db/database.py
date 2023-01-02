from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from db.models import Base
from decouple import config


class Database:
    def __init__(self, connection_url: str = config("DB_URL")):
        if not database_exists(connection_url):
            create_database(connection_url)
        else:
            self.engine = create_engine(connection_url)

        self.conn = self.engine.connect()
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)
        self.session.commit()

    def add_auto(self, objects):
        self.session.add(objects)
        self.session.commit()
