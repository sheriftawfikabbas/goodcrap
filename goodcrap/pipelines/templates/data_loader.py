if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from goodcrap import GoodCrap

@data_loader
def load_data(*args, **kwargs):
    database_config = {{ database_config }}
    gc = GoodCrap(size={{ size }},seed= {{ seed }}, database_config=database_config)
    crap_labels = {{ crap_labels }}
    return gc.get_dataframe("{{ table_name }}",crap_labels)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
