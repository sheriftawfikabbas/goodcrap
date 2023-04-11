from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
import snowflake.connector
from .database import DataBase


class Snowflake(DataBase):
    def __init__(self, database_config) -> None:
        super().__init__(database_config)
        self.native = False
        if not self.native:
            self.engine = create_engine(
                'snowflake://' +
                database_config['snowflake_user']+':' +
                database_config['snowflake_password']+'@' +
                database_config['snowflake_account'] +
                '/'+database_config['snowflake_database'] +
                '/'+database_config['snowflake_schema'] +
                '?warehouse='+database_config['snowflake_warehouse'] +
                '&role='+database_config['snowflake_role']
            )
            self.connection = self.engine.connect()
        else:
            self.connection = snowflake.connector.connect(
                user=self.database_config['snowflake_user'],
                password=self.database_config['snowflake_password'],
                account=self.database_config['snowflake_account'],
                warehouse=self.database_config['snowflake_warehouse'],
                database=self.database_config['snowflake_database'],
                schema=self.database_config['snowflake_schema']
            )
            self.cursor = self.connection.cursor()

        print('Successfully connected to Snowflake warehouse',
              database_config['snowflake_warehouse'])
        self.warehouse = database_config['snowflake_warehouse']

    def insert(self, table_name: str, row, table: Table = None):
        super().insert(table_name, row, table)

    def execute_sql(self, sql):
        super().execute_sql(sql)

    def bulk_upload(self, df, table_name):
        from snowflake.connector.pandas_tools import write_pandas
        # Must convert all column names to upper
        df.columns = [c.upper() for c in df.columns]
        # Must use raw_connection to get access to cursor()

        # TODO:
        # The function write_pandas below is unable to upload the df when engine.raw_connection() of sqlalchemy is used.
        # As a quick and dirty fix, the native connection is used instead.
        # This must be amended.
        # if not self.native:
        #     success, nchunks, nrows, _ = \
        #         write_pandas(self.engine.raw_connection(),
        #                      df,
        #                      table_name.upper(),
        #                      schema=self.database_config['snowflake_schema'].upper(
        #         ),
        #             database=self.database_config['snowflake_database'].upper(
        #         )
        #         )
        # else:
        self.connection = snowflake.connector.connect(
            user=self.database_config['snowflake_user'],
            password=self.database_config['snowflake_password'],
            account=self.database_config['snowflake_account'],
            warehouse=self.database_config['snowflake_warehouse'],
            database=self.database_config['snowflake_database'],
            schema=self.database_config['snowflake_schema']
        )
        success, nchunks, nrows, _ = \
            write_pandas(self.connection,
                            df,
                            table_name.upper(),
                            schema=self.database_config['snowflake_schema'].upper(
                            ),
                            database=self.database_config['snowflake_database'].upper(
                            )
                            )
        if success:
            print('Successfully wrote', nrows,
                  'records to Snowflake table', table_name)
        else:
            print('Error while writing to Snowflake table', table_name)
