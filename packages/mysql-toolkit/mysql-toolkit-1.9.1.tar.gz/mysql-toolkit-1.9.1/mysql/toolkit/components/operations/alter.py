from tqdm import tqdm
from mysql.toolkit.utils import wrap
from mysql.toolkit.datatypes import sql_column_type


class Alter:
    def rename(self, old_table, new_table):
        """
        Rename a table.

        You must have ALTER and DROP privileges for the original table,
        and CREATE and INSERT privileges for the new table.
        """
        try:
            command = 'RENAME TABLE {0} TO {1}'.format(wrap(old_table), wrap(new_table))
        except:
            command = 'ALTER TABLE {0} RENAME {1}'.format(wrap(old_table), wrap(new_table))
        self.execute(command)
        self._printer('Renamed {0} to {1}'.format(wrap(old_table), wrap(new_table)))
        return old_table, new_table

    def backup_database(self, structure=True, data=True):
        # TODO: Create method
        pass

    def create_database(self, name):
        """Create a new database."""
        statement = "CREATE DATABASE {0} DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci".format(wrap(name))
        return self.execute(statement)

    def create_table(self, name, data, columns=None, insert_data=True, add_pk=True):
        """Generate and execute a create table query by parsing a 2D dataset then insert data."""
        # TODO: Issue occurs when bool values exist in data
        # Remove if the table exists

        # TODO: improve disconnect/reconnect
        self.disconnect()

        if name in self.tables:
            self.drop(name)

        # Set headers list
        if not columns:
            columns = data[0]

        # Validate data shape
        for row in data:
            assert len(row) == len(columns)

        # Create dictionary of column types
        # TODO: add progress bar
        # TODO: add pool processing
        col_types = {columns[i]: sql_column_type([d[i] for d in data], prefer_int=True, prefer_varchar=True)
                     for i in tqdm(range(0, len(columns)), total=len(columns),
                                   desc='Getting datatypes for {0} table'.format(wrap(name)))}

        # Join column types into SQL string
        cols = ''.join(['\t{0} {1},\n'.format(name, type_) for name, type_ in
                        tqdm(col_types.items(), total=len(col_types.items()), desc='Joining columns')])[:-2] + '\n'
        statement = 'CREATE TABLE {0} ({1}{2})'.format(name, '\n', cols)
        self.reconnect()
        self.execute(statement)

        # Insert rows into table
        if insert_data:
            self.insert_many(name, columns, data)

        # Automatically add primary key
        if add_pk:
            self.set_primary_key_auto('team')
        self._printer('\tCreated table {0}'.format(wrap(name)))
        return True
