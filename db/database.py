from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from db.models import Base
from decouple import config
from .models import AutoRiaModel


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
        exists = (
            self.session.query(AutoRiaModel)
            .filter_by(current_url=objects.current_url)
            .first()
            is not None
        )
        print(exists)
        if exists:
            # print("no data")
            return None
        else:
            # print(f'new_data: {objects.title}')
            self.session.add(objects)
            self.session.commit()


