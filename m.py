from lib.db import sql_select
import pandas as pd

def get_book_rows():
    sql = '''
        select *
        from book
        order by "order"
        '''
    return sql_select(sql)

def get_book(book):
    sql = '''
        select *
        from book
        where book_id = %s
        '''
    params = [book]
    return sql_select(sql, params)[0]

def get_strong(strongs_id):
    sql = '''
        select *
        from strongs
        where strongs_id = %s
        '''
    params = [strongs_id]
    return sql_select(sql, params)[0]

def get_word_stats(strongs_id):
    sql = '''
        select w.text, count(*) as use_count
        from word w
        where w.strongs_id = %s
        group by w.text
        '''
    params = [strongs_id]
    return sql_select(sql, params)

def get_words(book, chap):
    sql = '''
        select distinct *
        from word
        where book_id = %s
        and chapter = %s
        order by word.order
        '''
    params = [book, chap]
    return sql_select(sql, params)

def get_verse_refs(strongs_id):
    sql = '''
        select distinct book_id, name, chapter, verse from (
            select
                b.order,
                b.book_id,
                b.name,
                w.chapter,
                w.verse
            from book b
            join word w
            on w.book_id = b.book_id
            where w.strongs_id = %s
            order by b.order, w.chapter, w.verse
            ) t
        '''
    params = [strongs_id]
    return sql_select(sql, params)

def get_verse_words(verse_refs):
    def getSql():
        def getParts():
            for ref in verse_refs:
                yield '''
                    select
                        w.book_id,
                        w.chapter,
                        w.verse,
                        w.text,
                        w.strongs_id,
                        w.order,
                        b.name,
                        b.order as book_order
                    from word w
                    join book b
                    on b.book_id = w.book_id
                    where b.book_id = %s
                    and w.chapter = %s
                    and w.verse = %s
                    '''
        return ' union all '.join(getParts())
    def getParams():
        for book_id, name, chapter, verse in verse_refs:
            yield book_id
            yield chapter
            yield verse
    return sql_select(getSql(), list(getParams()))

