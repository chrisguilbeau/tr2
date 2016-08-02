from itertools import cycle

from lib.tag import Tag as t
from json import dumps as json_encode

import pandas as pd

COLORS = ['black', 'grey', 'red']
COLORS = [
    'rgb(255, 187, 120)',
    'rgb(255, 127, 14)',
    'rgb(174, 199, 232)',
    'rgb(44, 160, 44)',
    'rgb(31, 119, 180)',
    'rgb(255, 152, 150)',
    'rgb(214, 39, 40)',
    'rgb(197, 176, 213)',
    'rgb(152, 223, 138)',
    'rgb(148, 103, 189)',
    'rgb(247, 182, 210)',
    'rgb(227, 119, 194)',
    'rgb(196, 156, 148)',
    'rgb(140, 86, 75)',
    'rgb(127, 127, 127)',
    'rgb(219, 219, 141)',
    'rgb(199, 199, 199)',
    'rgb(188, 189, 34)',
    'rgb(158, 218, 229)',
    'rgb(23, 190, 207)',
    ]

def getPage(content, barval=None):
    def getBar():
        return t.div(
            # t.a(
            #     t.div('&#x3B6;', _class='flex-col center'),
            #     href='/',
            #     id='tr_home',
            #     _class='tight flex-row center tr_icon',
            #     ),
            t.a('Home', href='/', _class='tr_home tight'),
            # t.input(
            #     # _class='awesomplete',
            #     # **{
            #     #     'data-list': 'aaaa, asd, axxx, abbb',
            #     #     }
            #     id='tr_search',
            #     # # placeholder='Chapter, Verse or Word',
            #     # # onblur='''
            #     # #     $(this).val('');
            #     # #     ''',
            #     # # # value=barval,
            #     ),
            # t.a(
            #     t.div('A', _class='flex-col center tr_little'),
            #     href='/',
            #     id='tr_little',
            #     _class='tight flex-row center tr_icon',
            #     ),
            # t.a(
            #     t.div('A', _class='flex-col center tr_big'),
            #     href='/',
            #     id='tr_big',
            #     _class='tight flex-row center tr_icon',
            #     ),
            id='tr_bar',
            _class='flex-row center tight',
            )
    return t._(
        '<!DOCTYPE html>',
        t.html(
            t.head(
                t.title(
                    'taproot'
                    ),
                t.link(rel='stylesheet', href='/s/flex.css'),
                t.link(rel='stylesheet', href='/s/tr.css'),
                t.link(rel='shortcut icon', href='/s/favicon.ico'),
                t.script(src='/s/Chart.min.js'),
                t.script(src='/s/jquery-2.2.3.min.js'),
                t.script(src='/s/tr.js'),
                t.meta(_name='viewport',
                    content='width=device-width, initial-scale=0.8',),
                ),
            t.body(
                getBar(),
                t.div(content, id='tr_content'),
                _class='flex-col stretch',
                ),
            ),
        )

def books(_books):
    def get_book_tiles():
        for book in _books:
            yield t.a(
                book.name,
                href='/{}'.format(book.book_id),
                _class='tr_tile',
                )
    return getPage(
        t.div(
            get_book_tiles(),
            _class='flex-row wrap',
            ),
        )

def book(_book):
    def get_chap_tiles():
        for i in xrange(1, _book.chap_count + 1):
            yield t.a(
                str(i),
                href='/{}/{}'.format(_book.book_id, i),
                _class='tr_tile',
                )
    return getPage(
        t.div(get_chap_tiles(), _class='flex-row wrap'),
        barval=_book.name,
        )

def chap(book, chap, words, verse):
    def get_verses():
        verse = 0
        for word in words:
            if word.verse > verse:
                yield t.p()
                yield '{} '.format(word.verse)
            verse = word.verse
            if not word.strongs_id:
                yield word.text
            else:
                yield t.a(
                    word.text,
                    href='/strongs/{}'.format(word.strongs_id),
                    _class='wordlink',
                    )
            yield ' '
    return getPage(
        content=(
            t.div(' '.join((book.name, chap)), _class='tr_head'),
            t.i(
                'Tap an underlined word for source text',
                _class='fg_deemp',
                ),
            get_verses()
            ),
        # barval=' '.join((book.name, chap)),
        )

def get_word_chart(word_stats):
    def getDf():
        df = pd.DataFrame(word_stats)
        df.text = df.text.str.lower().str.rstrip(',.;?!\';:')
        return df.groupby(
            'text').agg('sum').reset_index().sort('use_count', ascending=False)
    df = getDf()
    def getWords():
        colors = cycle(COLORS)
        for i, row in df.iterrows():
            yield t.div(
                t.div(row.text),
                t.div(
                    _class='tight',
                    _style='''
                        height:2em;
                        width:0.3em;
                        margin-left: 0.5em;
                        margin-right: 0.5em;
                        background-color:{};
                        '''.format(colors.next()),
                    ),
                t.div(str(row.use_count), _class='tight', _style='width:3em;'),
                _class='flex-row center',
                )
    def getChart():
        def getData():
            def getLabels():
                for i, row in df.iterrows():
                    yield row.text
            def getDataset():
                def _getData():
                    for i, row in df.iterrows():
                        yield row.use_count
                def getBackgroundColor():
                    colors = cycle(COLORS)
                    for i, row in df.iterrows():
                        yield colors.next()
                return dict(
                    data=list(_getData()),
                    backgroundColor=list(getBackgroundColor()),
                    )
            return dict(
                labels=list(getLabels()),
                datasets=[getDataset()],
                )
        def getOptions():
            return dict(
                responsive=False,
                )
        return t.div(
            t.div(),
            t.canvas(id='pie', _class='tight', style='max-height: 15em;'),
            t.div(),
            t.script('''
                Chart.defaults.global.legend = false;
                var ctx = document.getElementById("pie").getContext("2d");
                var myDoughnutChart = new Chart(ctx, {{
                    type: 'doughnut',
                    data: {},
                    options: {}
                }});
                '''.format(
                    json_encode(getData()),
                    json_encode(getOptions()),
                    )),
            _style='min-height: 15em;',
            _class='flex-row center',
            )
    return t.div(
        t.div(
            getWords(),
            # _style='margin-right: 1em',
            _class='tight',
            ),
        t.div(
            getChart(),
            # _class='flex-container',
            ),
        _style='margin-top: 1em',
        _class='flex-row',
        )

def strongs(strong, word_stats, verses):
    def get_verse_links():
        strongs_id = strong.strongs_id
        for book, words in sorted(verses.iteritems(), key=lambda a: a[0][0]):
            order, book_id, name, chap, verse = book
            def getItems():
                yield t.a(
                    '{} {}:{}'.format(name, chap, verse),
                    href='/{}/{}/{}'.format(book_id, chap, verse),
                    )
                yield '&nbsp;' * 3
                for word in sorted(words, key=lambda a: a.order):
                    if word.strongs_id == strongs_id:
                        yield t.b(word.text)
                    else:
                        yield word.text
                    yield ' '
            yield t.div(getItems(), _style='margin-bottom: 1em;')
    # return getPage(
    #     content=t.div(
    #         t.div('defs'),
    #         t.div('vis'),
    #         t.seq(get_verse_links()),
    #         _style='border: 1px solid blue',
    #         _class='flex-col stretch',
    #         ),
    #     )
    return getPage(
        content=t.div(
            t.div(
                t.div(
                    t.div(strong.xlit, _class='tr_head'),
                    t.div(strong.lemma, _class='tr_head fg_deemp'),
                    _class='tight',
                    ),
                t.div(_style='min-width: 3em; position:relative', _class='tight'),
                t.div(
                    t.div(strong.description, style='width:10em;',),
                    _class='flex-row'),
                _class='flex-row',
                ),
            t.div(get_word_chart(word_stats), _style='margin-bottom:1em;'),
            t.div(get_verse_links(), _class='flex-col'),
            _class='flex-col',
            ),
        )
