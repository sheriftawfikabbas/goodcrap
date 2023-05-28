import json
import os
from .databases.sqlite import SQLite
from .databases.mysql import MySQL
from .databases.snowflake import Snowflake
from .random_mapper import RandomMapper
from .pipelines.mage import MageProject
from . import templates


class GoodCrap:
    seed = None

    def __init__(
        self,
        size,
        seed,
        template_table=None,
        to_csv=False,
        to_json=False,
        to_parquet=False,
        database_config=None,
        template_database=None,
        table_sql=None,
        table_crap_labels=None,
        database_sql=None,
        database_crap_labels=None,
        mage_project_name=None,
        mage_pipeline=None,
        queries=False,
        bulk_upload=False
    ) -> None:
        GoodCrap.seed = seed
        self.size = size
        self.to_csv = to_csv
        self.to_json = to_json
        self.to_parquet = to_parquet
        self.template_table = template_table
        self.template_database = template_database
        self.table_sql = table_sql
        self.table_crap_labels = table_crap_labels
        self.database_sql = database_sql
        self.database_crap_labels = database_crap_labels
        self.mage_project_name = mage_project_name
        self.mage_pipeline = mage_pipeline
        self.queries = queries
        self.bulk_upload = bulk_upload

        self.templates_path = os.path.dirname(templates.__file__)

        if self.table_crap_labels:
            with open(self.table_crap_labels, 'r') as f:
                self.table_crap_labels = json.load(f)
                f.close()
        if self.database_crap_labels:
            with open(self.database_crap_labels, 'r') as f:
                self.database_crap_labels = json.load(f)
                f.close()
        out_str = 'Starting goodcrap with table size ' + \
            str(size) + ' and random seed ' + str(seed)
        print(out_str)

        self.database_instance = None

        if database_config is not None:
            if isinstance(database_config, str):
                fdatabase_config = open(database_config+'.json', 'r')
                database_config = json.load(fdatabase_config)
                fdatabase_config.close()
            database_config['to_csv'] = self.to_csv
            database_config['to_json'] = self.to_json
            database_config['to_parquet'] = self.to_parquet
            database_config['queries'] = self.queries
            database_config['bulk_upload'] = self.bulk_upload
            self.database_config = database_config
            if database_config['db_type'] == 'sqlite':
                self.database_instance = SQLite(database_config)
            elif database_config['db_type'] == 'mysql':
                self.database_instance = MySQL(database_config)
            elif database_config['db_type'] == 'snowflake':
                self.database_instance = Snowflake(database_config)

            if self.database_instance is not None:
                self.database_instance.set_size(self.size)
                self.database_instance.set_seed(self.seed)

    def run(self):
        '''
        The function will generate random data given that 
        only one of the following is supplied:
        - table_sql and table_crap_labels, or
        - database_sql and database_crap_labels, or
        - template_table, or
        - template_database
        '''
        if self.template_table is not None:
            self.run_template_table()
        elif self.template_database is not None:
            self.run_template_database()
        elif self.table_crap_labels is not None:
            self.run_table()
        elif self.database_sql is not None and self.database_crap_labels is not None:
            self.run_database()
        elif self.table_sql is None and self.table_crap_labels is not None\
                and self.database_instance is None:
            table_name = os.path.basename(
                self.table_crap_labels).replace('.json', '')
            self.write_file(table_name=table_name,
                            table_crap_labels=self.table_crap_labels)

    def run_template_table(self):
        if self.database_instance is not None:
            self._set_template_table_variables()
            with open(self.table_crap_labels, 'r') as f:
                self.table_crap_labels = json.load(f)
                f.close()
            if self._is_run_with_mage():
                self.run_mage(table_sql=self.table_sql,
                              table_crap_labels=self.table_crap_labels)
            else:
                self.database_instance.run(
                    table_sql=self.table_sql, table_crap_labels=self.table_crap_labels)
        else:
            # Generate csv files only
            self.table_crap_labels = self.templates_path + '/tables/' + \
                self.template_table+'/'+self.template_table+'.crap_labels.json'
            with open(self.table_crap_labels, 'r') as f:
                self.table_crap_labels = json.load(f)
                f.close()
            self.write_file(table_name=self.template_table,
                            table_crap_labels=self.table_crap_labels)

    def _set_template_table_variables(self):
        self.table_sql = self.templates_path + '/tables/' + \
            self.template_table+'/'+self.template_table+'.sql'
        self.table_crap_labels = self.templates_path + '/tables/' + \
            self.template_table+'/'+self.template_table+'.crap_labels.json'

    def _set_template_database_variables(self):
        self.database_sql = self.templates_path + '/databases/' + \
            self.template_database+'/'+self.template_database+'.sql'
        self.database_crap_labels = self.templates_path + '/databases/' + \
            self.template_database+'/'+self.template_database+'.crap_labels.json'

    def run_template_database(self):
        if self.database_instance is not None:
            self._set_template_database_variables()
            with open(self.database_crap_labels, 'r') as f:
                self.database_crap_labels = json.load(f)
                f.close()
            if self._is_run_with_mage():
                self.run_mage(database_sql=self.database_sql,
                              database_crap_labels=self.database_crap_labels)
            else:
                self.database_instance.run(
                    database_sql=self.database_sql,
                    database_crap_labels=self.database_crap_labels)
        else:
            print("WOOPS: You should provide a database configuration file.")

    def run_table(self):
        if self.database_instance is not None:
            if self._is_run_with_mage():
                self.run_mage(table_sql=self.table_sql,
                              table_crap_labels=self.table_crap_labels)
            elif self.table_sql is not None:
                self.database_instance.run(
                    table_sql=self.table_sql,
                    table_crap_labels=self.table_crap_labels)
            else:
                print(
                    "WOOPS: You should provide the table CREATE statement sql file (--table_sql).")
        else:
            print(
                "WOOPS: You should provide a database configuration file (--database_config).")

    def run_database(self):
        if self.database_instance is not None:
            if self._is_run_with_mage():
                self.run_mage(database_sql=self.database_sql,
                              database_crap_labels=self.database_crap_labels)
            else:
                self.database_instance.run(
                    database_sql=self.database_sql,
                    database_crap_labels=self.database_crap_labels)
        else:
            print("WOOPS: You should provide a database configuration file.")

    def run_mage(self, table_sql=None, table_crap_labels=None, database_sql=None,
                 database_crap_labels=None):
        '''
        Choosing Mage means that the data will not be generated using goodcrap,
        but will be generated in Mage pipelines by the user.
        However, the tables will be created in the target database.

        Mage can create the table on the fly if the table doesn't exist,
        so no need for the sql create statement.
        '''
        if self.mage_project_name is not None:
            # If the mage project doesn't exist, create it then add the
            # pipeline to it. Otherwise, just add the pipeline
            # to the existing mage project.
            if self.mage_project is None:
                self.create_mage_project()
            if table_sql is not None and table_crap_labels is not None:
                table_name = os.path.basename(
                    table_sql).replace('.sql', '')
                with open(table_sql, 'r') as f:
                    table_sql = f.read()
                    f.close()
                self.database_instance.execute(table_sql)
                self.create_mage_pipeline(table_name, table_crap_labels)
            elif database_sql is not None and database_crap_labels is not None:
                with open(database_sql, 'r') as f:
                    database_sql = f.read()
                    f.close()
                self.database_instance.execute(database_sql)
                for table_name in database_crap_labels.keys():
                    self.create_mage_pipeline(
                        table_name, database_crap_labels[table_name])

        else:
            # Set the project name as the database name plus a random string
            self.mage_project_name = self.database_config['database']
            self.mage_project_name += '-' + self.get_random_filename()
            self.create_mage_project()
            if table_sql is not None and table_crap_labels is not None:
                table_name = os.path.basename(
                    table_sql).replace('.sql', '')
                with open(table_sql, 'r') as f:
                    table_sql = f.read()
                    f.close()
                self.database_instance.execute(table_sql)
                self.create_mage_pipeline(table_name, table_crap_labels)
            elif database_sql is not None and database_crap_labels is not None:
                with open(database_sql, 'r') as f:
                    database_sql = f.read()
                    f.close()
                self.database_instance.execute(database_sql)
                for table_name in database_crap_labels.keys():
                    self.create_mage_pipeline(
                        table_name, database_crap_labels[table_name])

    def get_random_filename():
        import uuid
        return str(uuid.uuid4())[:8]

    def _is_run_with_mage(self):
        return self.mage_pipeline is not None

    def write_file(self, table_name=None,
                   table_crap_labels=None,
                   database_crap_labels=None):
        import pandas as pd
        if table_crap_labels is not None and database_crap_labels is None:
            fm = RandomMapper(
                self.seed, table_crap_labels)
            data_csv = []
            for _ in range(int(self.size)):
                data_csv += [fm.get_crap()]
            df = pd.DataFrame(data_csv, columns=table_crap_labels.keys())
            if self.to_json:
                with open(table_name+'.json', 'w') as f:
                    f.write(df.to_json())
                print('Data written to a json file')
            elif self.to_parquet:
                df.to_parquet(table_name + '.parquet',
                              engine='pyarrow', compression='gzip')
                print('Data written to a parquet file')
            else:
                df.to_csv(table_name+'.csv')
                print('Data written to a csv file')
        elif table_crap_labels is None and database_crap_labels is not None:
            pass

    def get_dataframe(self, table_name=None,
                      table_crap_labels=None):
        import pandas as pd
        if self.template_table is not None:
            table_name = self.template_table
            self._set_template_table_variables()
            table_crap_labels = self.table_crap_labels
        if isinstance(table_crap_labels, str):
            with open(table_crap_labels, 'r') as f:
                table_crap_labels = json.load(f)
                f.close()
        if self.database_instance is not None:
            from sqlalchemy import MetaData, Table
            metadata = MetaData(bind=self.database_instance.engine)
            table = Table(table_name, metadata, autoload=True)
            fm = RandomMapper(self.seed, table_crap_labels,
                              table, engine=self.database_instance.engine)
        else:
            fm = RandomMapper(
                self.seed, table_crap_labels)
        data_csv = []
        for _ in range(int(self.size)):
            data_csv += [fm.get_crap()]
        return pd.DataFrame(data_csv, columns=table_crap_labels.keys())

    def create_mage_project(self):
        self.mage_project = MageProject(
            project_name=self.mage_project_name,
            database_config=self.database_config,
            database_instance=self.database_instance)

    def create_mage_pipeline(self, table_name, crap_labels):
        self.mage_project.generate_pipeline(
            seed=self.seed, size=self.size,
            table_name=table_name,
            crap_labels=crap_labels)
    
    def generate_like(self, df):
        pass
