import json
import os
from .databases.sqlite import SQLite
from .databases.mysql import MySQL
from .random_mapper import RandomMapper


class GoodCrap:
    seed = None

    def __init__(
        self,
        size,
        seed,
        template_table=None,
        to_csv=None,
        to_json=None,
        database_config=None,
        template_database=None,
        table_sql=None,
        table_crap_labels=None,
        database_sql=None,
        database_crap_labels=None
    ) -> None:
        GoodCrap.seed = seed
        self.size = size
        self.to_csv = to_csv
        self.to_json = to_json
        self.template_table = template_table
        self.template_database = template_database
        self.table_sql = table_sql
        self.table_crap_labels = table_crap_labels
        self.database_sql = database_sql
        self.database_crap_labels = database_crap_labels

        out_str = 'Starting goodcrap with ' + str(size) + ' ' + str(seed)
        print(out_str)

        self.database_instance = None

        if database_config is not None:
            if type(database_config) is str:
                fdatabase_config = open(database_config+'.json', 'r')
                database_config = json.load(fdatabase_config)
                fdatabase_config.close()
            database_config['to_csv'] = self.to_csv
            database_config['to_json'] = self.to_json
            self.database_config = database_config
            if database_config['db_type'] == 'sqlite':
                self.database_instance = SQLite(database_config)
            elif database_config['db_type'] == 'mysql':
                self.database_instance = MySQL(database_config)

            if self.database_instance is not None:
                self.database_instance.set_size(self.size)
                self.database_instance.set_seed(self.seed)

    # The function will generate crap data given that only one of the following is supplied:
    # - table_sql and table_crap_labels, or
    # - database_sql and database_crap_labels, or
    # - template_table, or
    # - template_database
    def run(self):
        from . import templates
        path = os.path.dirname(templates.__file__)
        if self.template_table is not None and self.database_instance is not None:
            self.table_sql = path + '/tables/' + \
                self.template_table+'/'+self.template_table+'.sql'
            self.table_crap_labels = path + '/tables/' + \
                self.template_table+'/'+self.template_table+'.crap_labels.json'
            self.database_instance.run(
                table_sql=self.table_sql, table_crap_labels=self.table_crap_labels)
        elif self.template_table is not None and self.database_instance is None:
            # Generate csv files only
            self.table_crap_labels = path + '/tables/' + \
                self.template_table+'/'+self.template_table+'.crap_labels.json'
            self.write_csv(table_name=self.template_table,
                         table_crap_labels=self.table_crap_labels)
        elif self.template_database is not None and self.database_instance is not None:
            self.database_sql = path + '/databases/' + \
                self.template_database+'/'+self.template_database+'.sql'
            self.database_crap_labels = path + '/databases/' + \
                self.template_database+'/'+self.template_database+'.crap_labels.json'
            self.database_instance.run(
                database_sql=self.database_sql, database_crap_labels=self.database_crap_labels)
        elif self.table_sql is not None and self.table_crap_labels is not None and self.database_instance is not None:
            self.database_instance.run(
                table_sql=self.table_sql, table_crap_labels=self.table_crap_labels)
        elif self.table_crap_labels is not None and self.database_instance is None:
            table_name = os.path.basename(
                self.table_crap_labels).replace('.json', '')
            self.write_csv(table_name=table_name,
                         table_crap_labels=self.table_crap_labels)
        elif self.database_sql is not None and self.database_crap_labels is not None and self.database_instance is not None:
            self.database_instance.run(
                database_sql=self.database_sql, database_crap_labels=self.database_crap_labels)

    def write_csv(self, table_name=None, table_crap_labels=None, database_crap_labels=None):
        import pandas as pd
        if table_crap_labels is not None and database_crap_labels is None:
            if type(table_crap_labels) is str:
                with open(table_crap_labels, 'r') as f:
                    table_crap_labels = json.load(f)
                    f.close()
            fm = RandomMapper(
                self.seed, table_crap_labels)
            data_csv = []
            for i in range(int(self.size)):
                data_csv += [fm.get_crap()]
            df = pd.DataFrame(data_csv, columns=table_crap_labels.keys())
            df.to_csv(table_name+'.csv')
        elif table_crap_labels is None and database_crap_labels is not None:
            with open(database_crap_labels, 'r') as f:
                database_crap_labels = json.load(f)
                f.close()

    def get_dataframe(self, table_name=None, table_crap_labels=None):
        print(table_name, table_crap_labels)
        import pandas as pd
        if type(table_crap_labels) is str:
            with open(table_crap_labels, 'r') as f:
                table_crap_labels = json.load(f)
                f.close()
        fm = RandomMapper(
            self.seed, table_crap_labels)
        data_csv = []
        for i in range(int(self.size)):
            data_csv += [fm.get_crap()]
        return pd.DataFrame(data_csv, columns=table_crap_labels.keys())
