#!/usr/bin/env python3
#
# This analysis tool shows
#                           -The most popular three articles of all time
#                           -The most popular article authors of all time
#                           -Which days did more than 1% of requests lead
#                            to errors

__version__ = '0.1'
__author__ = "Zizo Naser"

import psycopg2

# Database's name
DBNAME = 'news'


def get_aricles():
    """Return a list of the most popular three articles paired with
    the number of views"""
    # Connect to the DB
    db = psycopg2.connect(database=DBNAME)
    # Get a cursor
    cursor = db.cursor()
    # Prepare the sql query
    cursor.execute("SELECT * FROM articleViews LIMIT 3")
    # Get the results and pair it with the views' count
    results = [(title, views) for title, views in cursor.fetchall()]
    # Close the connectionn
    db.close()
    return results


def get_authors():
    """Return a list of the most popular article authors of all time
    paired with the views"""
    # Connect to the DB
    db = psycopg2.connect(database=DBNAME)
    # Get a cursor
    cursor = db.cursor()
    # Prepare the sql query
    cursor.execute("SELECT * FROM authorsView")
    # Get the results and pair it with the views' count
    results = [(name, views) for name, views in cursor.fetchall()]
    # Close the connectionn
    db.close()
    return results


def get_errors():
    """Return a list of which days did more than 1% of requests lead to
    errors paired with the error percentage"""
    # Connect to the DB
    db = psycopg2.connect(database=DBNAME)
    # Get a cursor
    cursor = db.cursor()
    # Prepare the sql query
    cursor.execute("SELECT * FROM errorView WHERE percent > 1")
    # Get the results and pairs it with the error percentage
    results = [(name, percent) for name, percent in cursor.fetchall()]
    # Close the connectionn
    db.close()
    return results


def display(message, list, type):
    """Prints out the message followed by the list"""
    print(message, end='\n\n')
    for result in list:
        print(
            '\t* '+str(result[0])
            + ' ---- '+str(result[1])
            + type
        )
    print()


# Print out the report
display(
    "The most popular three articles of all time:",
    get_aricles(), ' Views'
)
display(
    "The most popular article authors of all time:",
    get_authors(), ' Views'
)
display(
    "The days did more than 1% of requests lead to errors:",
    get_errors(), '%'
)
