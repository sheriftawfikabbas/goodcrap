import json
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.sql import text

from ..random_mapper import RandomMapper
from ..crappers import queries


class DataBase:
    def __init__(self,
                 database_config) -> None:
        self.database_config = database_config
        self.size = 1000
        self.connection = None
        self.engine = None
        self.native = False

    def set_size(self, size):
        self.size = size

    def set_seed(self, seed):
        self.seed = seed

    def insert(self, table_name: str, row, table: Table = None):
        if table is not None:
            ins = table.insert().values(row)
            self.engine.execute(ins)

    def execute_sql(self, table_sql):
        self.connection.execute(table_sql)

    def run(self, table_sql=None, table_crap_labels=None,
            database_sql=None, database_crap_labels=None):
        if table_sql is not None and table_crap_labels is not None:
            table_name = os.path.basename(table_sql).split('.')[0]
            with open(table_sql, 'r') as f:
                self.table_sql = f.read()
                f.close()

            # sqlalchemy.inspect(self.engine).has_table(table_name)

            self.execute_sql(self.table_sql)

            metadata = MetaData(bind=self.engine)
            table = Table(table_name, metadata, autoload=True)

            fm = RandomMapper(self.seed, table_crap_labels,
                              table, engine=self.engine)
            data_csv = []
            for _ in range(self.size):
                row = fm.get_crap()
                if not self.database_config['bulk_upload']:
                    self.insert(table_name=table_name, row=row, table=table)
                if self.database_config['to_csv'] or self.database_config['bulk_upload']:
                    data_csv += [row]
            if self.database_config['to_csv'] or self.database_config['bulk_upload']:
                df = pd.DataFrame(data_csv, columns=table_crap_labels.keys())
                df.to_csv(table_name+'.csv')
            if self.database_config['bulk_upload']:
                self.bulk_upload(df, table_name)

        elif database_sql is not None and database_crap_labels is not None:
            if self.database_config['bulk_upload']:
                import sys
                sys.exit('Write a database to Snowflake is not yet supported.')

            with open(database_sql, 'r') as f:
                self.database_sql = f.read()
                f.close()
            self.connection.execute(self.database_sql)
            metadata = MetaData(bind=self.engine)
            rounds = 10
            for _ in range(rounds):
                for table_name in self.engine.table_names():
                    table = Table(table_name, metadata, autoload=True)

                    fm = RandomMapper(
                        self.seed, database_crap_labels[table_name], table, self.engine)

                    data_csv = []
                    for _ in range(int(self.size/rounds)):
                        row = fm.get_crap()
                        self.insert(table_name=table_name, row=row, table=table)
                        if self.database_config['to_csv']:
                            data_csv += [row]
                    if self.database_config['to_csv']:
                        df = pd.DataFrame(data_csv, columns=table.columns)
                        df.to_csv(table_name+'.csv')
        if 'queries' in self.database_config.keys():
            with open('queries.sql', 'w') as f:
                for _ in range(self.database_config['queries']):
                    f.write(str(queries.crapper(self.engine))+'\n')
                    f.flush()
                f.close()

    def bulk_upload(self, df, table_name):
        print('Bulk upload is not implemented yet for',
              self.database_config['db_type'])

    def execute(self, sql):
        return self.engine.execute(sql)
