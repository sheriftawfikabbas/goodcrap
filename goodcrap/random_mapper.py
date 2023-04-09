from sqlalchemy import MetaData, Table, Column, Integer, String, select
import faker
from .crappers import crapper, crapper_unique

fake = faker.Faker('en-US')

class RandomMapper:
    """
    Maps a table column to a Faker
    """

    def __init__(self, seed, crap_labels: dict, table: Table = None, engine=None) -> None:
        self.seed = seed
        self.engine = engine
        faker.Faker.seed(self.seed)
        self.faker_generator = []
        table_columns = []
        primary_keys = []
        fks = {}
        if engine is not None and table is not None:
            for f in table.foreign_keys:
                metadata = MetaData(bind=self.engine)
                # metadata.reflect(self.engine): That's for version > 2
                rel_table = Table(f.column.table, metadata, autoload=True)
                results = self.engine.connect().execute(
                    select(rel_table.c[f.column.name])).fetchall()
                results = [x[0] for x in results]
                fks[f.column.name] = results
                # print(fks[f.column.name])
        if engine is not None and table is not None:
            for c in table.columns:
                table_columns += [c.name]
                if c.primary_key:
                    primary_keys += [c.name]
        else:
            table_columns = crap_labels.keys()

        for column_name in table_columns:
            cl = crap_labels[column_name]
            if type(cl) is str:
                if column_name in fks.keys():
                    import random
                    # Get a random key from the related table
                    self.faker_generator += [
                        lambda: random.sample(fks[column_name], 1)[0]]
                elif not cl.startswith('goodcrap_'):
                    if column_name in primary_keys:
                        self.faker_generator += [getattr(fake.unique,
                                                         cl)]
                    else:
                        self.faker_generator += [getattr(fake,
                                                         cl)]
            else:
                if column_name in primary_keys:
                    self.faker_generator += [lambda: crapper_unique(cl)]
                else:
                    self.faker_generator += [lambda: crapper(cl)]

    def get_crap(self):
        return [f() for f in self.faker_generator]

    def predict_faker(self, col):
        pass
