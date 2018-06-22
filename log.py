#!/usr/bin/env python2
import psycopg2

GET_ARTICLES = """
    SELECT articles.title, count(log.path) as views
    FROM articles, log
    WHERE log.path like ('%' || articles.slug)
    GROUP BY articles.title
    ORDER BY views DESC
    LIMIT 3;"""

GET_AUTHORS = """
    SELECT authors.name, count(log.path) as num
    FROM log, articles, authors
    WHERE log.path LIKE ('%' || articles.slug)
      AND authors.id = articles.author
    GROUP BY authors.name
    ORDER BY num DESC;"""

GET_ERRORS = """
    SELECT totalrequests.day,
      round(100*totalerrors.errors::decimal/totalrequests.requests, 2) AS fail
    FROM totalerrors, totalrequests
    WHERE totalrequests.day = totalerrors.day
    AND (totalerrors.errors::decimal/totalrequests.requests > 0.01);"""

POP_ARTICLES = "The most popular three articles of all time:"
POP_AUTHOR = "The most popular authors of all time:"
ERROR_DAY = "Day(s) having more than 1%" + " errors"

db = psycopg2.connect(database="news")
c = db.cursor()

"""
q: is the sql querry
text: is the title text of each querry print
bad_day: is a boolean, if true then print out days with errors
"""
def querry(q, text, bad_day):
    print text + "\n"
    c.execute(q)
    rows = c.fetchall()
    for row in rows:
        if bad_day:
            print " "+ row[0].strftime("%Y-%m-%d"),
            print " - " + str(row[1]) + "%" + " errors"
        else:
            print " " + row[0] + " - " + str(row[1]) + " views"
    print "\n"

querry(GET_ARTICLES, POP_ARTICLES, False)
querry(GET_AUTHORS, POP_AUTHOR, False)
querry(GET_ERRORS, ERROR_DAY, True)
db.close()
