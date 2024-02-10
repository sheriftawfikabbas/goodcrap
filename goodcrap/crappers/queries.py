import random
from sqlalchemy import MetaData, Table, select, desc
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.sql.sqltypes import String, DateTime, NullType, Date

# PY3 = str is not bytes
# text = str if PY3 else unicode
# int_type = int if PY3 else (int, long)
# str_type = str if PY3 else (str, unicode)

text = str
int_type = int
str_type = str

'''
Literalizing statement strings is obtained from the answer of: 
https://stackoverflow.com/questions/5631078/sqlalchemy-print-the-actual-query
'''


class StringLiteral(String):
    def literal_processor(self, dialect):
        super_processor = super(StringLiteral, self).literal_processor(dialect)

        def process(value):
            if isinstance(value, int_type):
                return text(value)
            if not isinstance(value, str_type):
                value = text(value)
            result = super_processor(value)
            if isinstance(result, bytes):
                result = result.decode(dialect.encoding)
            return result
        return process


class LiteralDialect(DefaultDialect):
    colspecs = {
        # prevent various encoding explosions
        String: StringLiteral,
        # teach SA about how to literalize a datetime
        DateTime: StringLiteral,
        # don't format py2 long integers to NULL
        NullType: StringLiteral,
        Date: StringLiteral,
    }


def random_operation(a, b):
    condition = random.randint(1, 6)
    if condition == 1:
        return a > b
    if condition == 2:
        return a >= b
    if condition == 3:
        return a < b
    if condition == 4:
        return a <= b
    if condition == 5:
        return a == b
    if condition == 6:
        return a != b


def crapper(engine):
    '''
    Generates one of 10 possible random SQL queries
    TODO: Generate a sample table to enable generation of queries with comparison operators
    '''
    stmt = None
    choice = random.randint(1, 2)
    if choice == 1:
        '''
        Query multiple column from a table
        '''
        table_name = random.sample(engine.table_names(), 1)[0]
        metadata = MetaData(bind=engine)
        table = Table(table_name, metadata, autoload=True)
        number_of_columns = random.randint(1, len(table.columns.items()))
        columns = random.sample(table.columns.items(), number_of_columns)
        column_names = [c[0] for c in columns]
        stmt = select([table.c[i] for i in column_names])

    elif choice == 2:
        '''
        Query multiple columns from a table given one of the columns satisfy a single condition
        '''
        table_name = random.sample(engine.table_names(), 1)[0]
        metadata = MetaData(bind=engine)
        table = Table(table_name, metadata, autoload=True)
        number_of_columns = random.randint(1, len(table.columns.items()))
        columns = random.sample(table.columns.items(), number_of_columns)
        column_names = [c[0] for c in columns]
        stmt_col = select(table.c[column_names[-1]])
        col_values = engine.connect().execute(stmt_col).fetchall()
        random_value = col_values[random.randint(0, len(col_values)-1)][0]
        if len(column_names) > 2:
            stmt = select([table.c[i] for i in column_names[:-1]]).\
                where(random_operation(table.c[column_names[-1]], random_value)
                      )\
                .order_by(table.c[column_names[-2]], desc(table.c[column_names[-1]]))
        else:
            stmt = select([table.c[i] for i in column_names[:-1]]).\
                where(random_operation(table.c[column_names[-1]], random_value)
                      )\
                .order_by(table.c[column_names[-1]], desc(table.c[column_names[-1]]))

    return stmt.compile(dialect=LiteralDialect(), compile_kwargs={"literal_binds": True})
