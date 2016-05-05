class FK(object):
    RESTRICT = 'restrict'
    CASCADE = 'cascade'
    NO_ACTION = 'no action'
    SET_NULL = 'set null'
    SET_DEFAULT = 'set default'


class Constraint(object):

    @classmethod
    def check(cls, expression):
        return 'check ({})'.format(expression)

    @classmethod
    def not_null(cls):
        return 'not null'

    @classmethod
    def unique(cls):
        return 'unique'

    @classmethod
    def primary_key(cls):
        return 'primary key'

    @classmethod
    def foreign_key(cls, table, column,
            on_delete=FK.NO_ACTION, on_update=FK.NO_ACTION):
        return 'references {} ({}) on delete {} on update {}'.format(
            table,
            column,
            on_delete,
            on_update,
            )


class Column(object):

    def __init__(self, name, type, default=None, constraints=None):
        self.name = name
        self.type = type
        self.default = default
        self.constraints = constraints or []
    @property
    def _create_sql(self):
        def yieldParts():
            yield '"{}"'.format(self.name)
            yield self.type
            if self.default:
                yield 'default {}'. format(self.default)
            for c in self.constraints:
                yield c
        return ' '.join(yieldParts())

class Index(object):
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns

class Table(object):

    def __init__(self, name, columns, indexes=None):
        self.name = name
        self.columns = columns
        self.indexes = indexes or []

    @property
    def _create_sql(self):
        def get_column_sql():
            def yield_column_sql():
                for c in self.columns:
                    yield c._create_sql
            return ''',
                '''.join(yield_column_sql())
        return '''
            create table {name}(
                {column_sql}
                );
            '''.format(
                name=self.name,
                column_sql=get_column_sql(),
                )
    @property
    def _create_index_sqls(self):
        def yield_sqls():
            for i in self.indexes:
                yield 'create index {} on {} ({});'.format(
                    i.name,
                    self.name,
                    ', '.join(i.columns),
                    )
        return list(yield_sqls())
