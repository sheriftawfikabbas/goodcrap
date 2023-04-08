from sqlalchemy import create_engine
from .database import DataBase

class MySQL(DataBase):
    def __init__(self, database_config) -> None:
        super().__init__(database_config)

        self.engine = create_engine("mysql://"+database_config["user"] +
                                    ":"+database_config["passwd"] +
                                    "@"+database_config["host"] +
                                    "/"+database_config["database"], echo=False)
        self.connection = self.engine.connect()
