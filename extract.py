import pandas as pd
import bs4
from bs4 import BeautifulSoup
from urllib import urlopen

def getBooks():
    yield 'genesis', 50
    yield 'exodus', 40
    yield 'leviticus', 27
    yield 'numbers', 36
    yield 'deuteronomy', 34
    yield 'joshua', 24
    yield 'judges', 21
    yield 'ruth', 4
    yield '1_samuel', 31
    yield '2_samuel', 24
    yield '1_kings', 22
    yield '2_kings', 25
    yield '1_chronicles', 29
    yield '2_chronicles', 36
    yield 'ezra', 10
    yield 'nehemiah', 13
    yield 'esther', 10
    yield 'job', 42
    yield 'psalms', 150
    yield 'proverbs', 31
    yield 'ecclesiastes', 12
    yield 'song_of_solomon', 8
    yield 'isaiah', 66
    yield 'jeremiah', 52
    yield 'lamentations', 5
    yield 'ezekiel', 48
    yield 'daniel', 12
    yield 'hosea', 14
    yield 'joel', 3
    yield 'amos', 9
    yield 'obadiah', 1
    yield 'jonah', 4
    yield 'micah', 7
    yield 'nahum', 3
    yield 'habakkuk', 3
    yield 'zephaniah', 3
    yield 'haggai', 2
    yield 'zechariah', 14
    yield 'malachi', 4
    yield 'matthew', 28
    yield 'mark', 16
    yield 'luke', 24
    yield 'john', 21
    yield 'acts', 28
    yield 'romans', 16
    yield '1_corinthians', 16
    yield '2_corinthians', 13
    yield 'galatians', 6
    yield 'ephesians', 6
    yield 'philippians', 4
    yield 'colossians', 4
    yield '1_thessalonians', 5
    yield '2_thessalonians', 3
    yield '1_timothy', 6
    yield '2_timothy', 6
    yield 'titus', 3
    yield 'philemon', 1
    yield 'hebrews', 13
    yield 'james', 5
    yield '1_peter', 5
    yield '2_peter', 3
    yield '1_john', 5
    yield '2_john', 1
    yield '3_john', 1
    yield 'jude', 1
    yield 'revelation', 22

root = 'http://www.apostolic-churches.net/bible/strongs/'
for book_name, num_chapters in getBooks():
    def getAllRows():
        for i in xrange(1, num_chapters + 1):
            href = '{}{}_{}.shtml'.format(root, book_name, i)
            print 'getting', href
            page = urlopen(href)
            soup = BeautifulSoup(page.read(), 'html.parser')
            def hrefToRef(href):
                def getPre():
                    if 'hebrew' in href:
                        return 'H'
                    else:
                        return 'G'
                def getNum():
                    return href.split('=')[-1].lstrip('0')
                return '{}{}'.format(getPre(), getNum())

            def getRows(book_name):
                for tr in soup.find_all('tr'):
                    if tr.find('dt'):
                        dt = tr.find('dt')
                        b = dt.b
                        for i, t in enumerate(b.next_siblings):
                            def getCols():
                                if t and t.string and t.string.strip():
                                    cparts = b.string.strip().split(':')
                                    yield book_name
                                    yield cparts[0]
                                    yield cparts[1]
                                    yield t.string.strip()
                                    if isinstance(t, bs4.element.Tag) and t.name == 'a':
                                        href = t.get('href')
                                        yield hrefToRef(href)
                                    else:
                                        yield None
                            yield list(getCols())
            for j, row in enumerate(getRows(book_name)):
                if row:
                    yield list(row) + [j]
    df = pd.DataFrame(getAllRows())
    df.columns = ('book', 'chapter', 'verse', 'word', 'strongs_ref', 'order')
    df.to_csv('word_parts/{}.csv'.format(book_name), index=False)
