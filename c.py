from collections import defaultdict
from lib.flask import app
import v
import m

@app.route('/strongs/<strongs_id>')
def strongs(strongs_id):
    def get_verses():
        result = defaultdict(list)
        def getKey(row):
            return (
                row.book_order, row.book_id, row.name, row.chapter, row.verse)
        def getValue(row):
            return row
        for row in m.get_verse_words(
                m.get_verse_refs(strongs_id)):
            result[getKey(row)].append(getValue(row))
        return result
    return v.strongs(
        m.get_strong(strongs_id),
        m.get_word_stats(strongs_id),
        get_verses(),
        )

@app.route('/')
def books():
    return v.books(m.get_book_rows())

@app.route('/<book>')
def chaps(book):
    return v.book(m.get_book(book))

@app.route('/<book>/<chap>')
@app.route('/<book>/<chap>/<verse>')
def index(book, chap, verse=None):
    return v.chap(
        m.get_book(book),
        chap,
        m.get_words(book, chap),
        verse,
        )
