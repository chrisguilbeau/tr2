from lib.sql import Column
from lib.sql import Constraint
from lib.sql import FK
from lib.sql import Index
from lib.sql import Table

tr_tables = []

class TrTable(Table):

    def __init__(self, *args, **kwargs):
        tr_tables.append(self)
        return super(TrTable, self).__init__(*args, **kwargs)


book = TrTable(
    name='book',
    columns=[
        Column(
            name='book_id',
            type='text',
            constraints=[
                Constraint.primary_key(),
                Constraint.not_null(),
                Constraint.unique(),
                ],
            ),
        Column(
            name='name',
            type='text',
            constraints=[
                Constraint.not_null(),
                Constraint.unique(),
                ],
            ),
        Column(
            name='order',
            type='integer',
            constraints=[
                Constraint.not_null(),
                Constraint.unique(),
                ],
            ),
        Column(
            name='testament',
            type='text',
            constraints=[
                Constraint.not_null(),
                Constraint.check(
                    expression="testament in ('old', 'new')",
                    ),
                ],
            ),
        Column(
            name='chap_count',
            type='integer',
            constraints=[
                Constraint.not_null(),
                ],
            ),
        ],
    )

strongs = TrTable(
    name='strongs',
    columns=[
        Column(
            name='strongs_id',
            type='text',
            constraints=[
                Constraint.primary_key(),
                Constraint.unique(),
                ],
            ),
        Column(
            name='lemma',
            type='text',
            constraints=[
                ],
            ),
        Column(
            name='xlit',
            type='text',
            constraints=[
                ],
            ),
        Column(
            name='pronounce',
            type='text',
            constraints=[
                ],
            ),
        Column(
            name='description',
            type='text',
            constraints=[
                ],
            ),
        Column(
            name='part_of_speech',
            type='text',
            constraints=[
                ],
            ),
        Column(
            name='language',
            type='text',
            constraints=[
                ],
            ),
        ],
    )

word = TrTable(
    name='word',
    columns=[
        Column(
            name='book_id',
            type='text',
            constraints=[
                Constraint.foreign_key('book', 'book_id'),
                ],
            ),
        Column(
            name='chapter',
            type='integer',
            constraints=[
                Constraint.not_null(),
                ],
            ),
        Column(
            name='verse',
            type='integer',
            constraints=[
                Constraint.not_null(),
                ],
            ),
        Column(
            name='text',
            type='text',
            constraints=[
                Constraint.not_null(),
                ],
            ),
        Column(
            name='strongs_id',
            type='text',
            ),
        Column(
            name='order',
            type='integer',
            constraints=[
                Constraint.not_null(),
                ],
            ),
        ],
    indexes=[
        Index('ix_a', ('book_id', 'chapter', 'verse')),
        ],
    )
