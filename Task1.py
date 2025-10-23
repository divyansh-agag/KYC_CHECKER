import datetime

import pathway as pw



class SimpleTypesInputSchema(pw.Schema):
    bool_column: bool
    str_column: str
    bytes_column: bytes
    int_column: int
    float_column: float

example_table = pw.debug.table_from_markdown(
    '''
      | bool_column | str_column | bytes_column | int_column | float_column
    1 | True        | example    | example      | 42         | 42.16
    2 | False       | text       | text         | 16         | -16.42
    ''', schema = SimpleTypesInputSchema
).with_columns(id_in_column = pw.this.id)

pw.debug.compute_and_print(example_table, include_id = False)
