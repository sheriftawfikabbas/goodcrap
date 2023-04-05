from .database import DataBase
from sqlalchemy import create_engine
import sqlite3
from sqlite3 import Error

class SQLite(DataBase):
    def __init__(self, database_config) -> None:
        super().__init__(database_config)
        self.connection = None
       
        self.engine = create_engine('sqlite:///'+database_config['database']+'.db', echo = False)
        self.connection = self.engine.connect()
