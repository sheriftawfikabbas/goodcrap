import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text

from ..random_mapper import RandomMapper
import json
import os
import pandas as pd


class DataBase:
    def __init__(self,
                 database_config) -> None:
        self.database_config = database_config
        self.size = 1000
        self.connection = None
        self.engine = None

    def set_size(self, size):
        self.size = size

    def set_seed(self, seed):
        self.seed = seed

    def run(self, table_sql=None, table_crap_labels=None, database_sql=None, database_crap_labels=None):
        if table_sql is not None and table_crap_labels is not None:
            table_name = os.path.basename(table_sql).split('.')[0]
            with open(table_sql, 'r') as f:
                self.table_sql = f.read()
                f.close()
            with open(table_crap_labels, 'r') as f:
                self.table_crap_labels = json.load(f)
                f.close()
            self.connection.execute(self.table_sql)
            metadata = MetaData(bind=self.engine)

            table = Table(table_name, metadata, autoload=True)

            fm = RandomMapper(self.seed, self.table_crap_labels,
                             table, engine=self.engine)

            data_csv = []
            for i in range(self.size):
                row = fm.get_crap()
                ins = table.insert().values(row)
                self.engine.execute(ins)
                if self.database_config['to_csv']:
                    data_csv += [row]
            if self.database_config['to_csv']:
                df = pd.DataFrame(data_csv, columns=table.columns)
                df.to_csv(table_name+'.csv')

        if database_sql is not None and database_crap_labels is not None:
            with open(database_sql, 'r') as f:
                self.database_sql = f.read()
                f.close()
            with open(database_crap_labels, 'r') as f:
                self.database_crap_labels = json.load(f)
                f.close()
            self.connection.execute(self.database_sql)
            metadata = MetaData(bind=self.engine)
            rounds = 10
            for i in range(rounds):
                for table_name in self.engine.table_names():
                    table = Table(table_name, metadata, autoload=True)

                    fm = RandomMapper(
                        self.seed, self.database_crap_labels[table_name], table, self.engine)

                    data_csv = []
                    for i in range(int(self.size/rounds)):
                        row = fm.get_crap()
                        ins = table.insert().values(row)
                        self.engine.execute(ins)
                        if self.database_config['to_csv']:
                            data_csv += [row]
                    if self.database_config['to_csv']:
                        df = pd.DataFrame(data_csv, columns=table.columns)
                        df.to_csv(table_name+'.csv')
