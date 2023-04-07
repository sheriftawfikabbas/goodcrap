from jinja2 import Environment, FileSystemLoader
import subprocess
import os
from ..databases.mysql import MySQL
from ..databases.sqlite import SQLite


class MageProject:
    def __init__(self, project_name, database_config, database_instance) -> None:
        from . import templates
        self.database_instance = database_instance
        self.database_config = database_config
        templates_path = os.path.dirname(templates.__file__) + '/'
        self.environment = Environment(loader=FileSystemLoader(templates_path))
        self.data_loader_template = self.environment.get_template(
            "data_loader.py")
        if isinstance(self.database_instance, MySQL):
            self.data_exporter_template = self.environment.get_template(
                "data_exporter_mysql.py")
        elif isinstance(self.database_instance, SQLite):
            self.data_exporter_template = self.environment.get_template(
                "data_exporter_sqlite.py")
        self.metadata_template = self.environment.get_template("metadata.yaml")

        print('Generating the Mage project', project_name)

        self.project_name = project_name
        retcode = subprocess.call('mage init ' + self.project_name)
        if retcode == 0:
            print('Successfully generating the Mage project', project_name)

    def generate_pipeline(self, size, seed, table_name, crap_labels) -> None:
        # Note: If you are planning to run a pipeline multiple times, then make sure that it does not
        # have columns that are generated using the faker.unique function. Those columns should be universally unique.
        self.size = size
        self.seed = seed
        self.table_name = table_name
        self.crap_labels = crap_labels
        self.data_loader_context = {
            "size": size,
            "seed": seed,
            "table_name": table_name,
            "crap_labels": crap_labels,
            "database_config": self.database_config
        }
        self.data_exporter_context = {
            "database_instance": self.database_instance,
            "table_name": table_name,
        }

        self.metadata_context = {
            "pipeline_name": self.table_name,
            "data_loader": 'data_loader_' + self.table_name,
            "data_exporter": 'data_exporter_' + self.table_name,
        }

        # Note: The conditional statement on the type of the database instance will not be made in
        # the Jinja template. Instead, it will be made here to optimize the Mage pipeline performance.

        # First write the data loader and exporter files
        data_loader = self.project_name + \
            '/data_loaders/data_loader_' + self.table_name + '.py'
        with open(data_loader, mode="w", encoding="utf-8") as results:
            results.write(self.data_loader_template.render(
                self.data_loader_context))

        data_exporter = self.project_name + \
            '/data_exporters/data_exporter_' + self.table_name + '.py'
        with open(data_exporter, mode="w", encoding="utf-8") as results:
            results.write(self.data_exporter_template.render(
                self.data_exporter_context))

        os.mkdir(self.project_name + '/pipelines/' + self.table_name)
        metadata = self.project_name + '/pipelines/' + self.table_name + '/metadata.yaml'
        with open(metadata, mode="w", encoding="utf-8") as results:
            results.write(self.metadata_template.render(self.metadata_context))
