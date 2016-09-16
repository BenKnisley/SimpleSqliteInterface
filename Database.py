#!/usr/bin/env python
"""
Project: Simple Sqlite Interface
Author: Ben Knisley [benknisley@gmail.com]
Date: 15, Sept 2016
This simple Python Sqlite interface is made to make dealing with database calls
    super easy. It provides the most basic of operations, add, get, update, and
    delete. It provides no error detection, all thrown errors are from sqlite
    itself. It does its best to sterlize input, but sqlite doesn't let table or
    keys be inputed in as ?. So don't push it.

    There will be more complex future iterations, but they will likey be based
    off of this simple codebase.

Depends:
    Python sqlite3

Future:
    - Add Documention, to make easy to use.
    - Add a runSQL() function to run a raw statment.
    - Add a getTables() function
"""
import sqlite3

class Database:
    """
    """
    def __init__(self, dbPath):
        """
        """
        ## Set database path from one given
        self.dbPath = dbPath

    def getLayout(self, table):
        """
        """
        ## Connect to Database
        conn = sqlite3.connect(self.dbPath)
        sql = conn.cursor()

        ## Setup query
        query = "PRAGMA table_info('%s');" % table

        ## Execute query
        sql.execute(query)

        ## Get data from response
        data = sql.fetchall()

        ## Create return list
        retn = list()

        ## Loop through data and append name to retn
        for datum in data:
            retn.append(datum[1])

        ## Return
        return retn

    def getAll(self, table):
        ## Connect to Database
        conn = sqlite3.connect(self.dbPath)
        sql = conn.cursor()

        ## Setup query
        query = "SELECT * FROM '%s';" % (table)

        ## Execute query
        sql.execute(query)

        ## Get data from response
        data = sql.fetchall()

        ## Return
        return data

    def get(self, table, parm, value):
        ## Connect to Database
        conn = sqlite3.connect(self.dbPath)
        sql = conn.cursor()

        ## Setup query
        query = "SELECT * FROM '%s' WHERE %s = ?;" % (table, parm)

        ## Execute query
        sql.execute(query, (value,))

        ## Get data from response
        data = sql.fetchone()

        ## Return
        return data

    def add(self, table, *args):
        ## Connect to Database
        conn = sqlite3.connect(self.dbPath)
        sql = conn.cursor()

        ## Setup Query

        ## Generate a sirces of ? to fill in
        qbrack = '(' + ('?,' * (len(args)-1))  + '?)'

        ## Generate Query
        query = "INSERT INTO '%s' VALUES %s;" % (table, qbrack)

        ## Send query to database
        sql.execute(query, args)

        ## Add changes to database
        conn.commit()

    def delete(self, table, parm, value):
        ## Connect to Database
        conn = sqlite3.connect(self.dbPath)
        sql = conn.cursor()

        ## Setup query
        query = "DELETE FROM '%s' WHERE %s = ?;" % (table, parm)

        ## Execute query
        sql.execute(query, (value,))

        ## Commit changes to database
        conn.commit()

    def update(self, table, parm, value, **args):
        ## Get list of current values
        curValues = list(getOne(table, parm, value))

        ## Get table layout
        layout = getLayout(table)

        ## Loop through given updates
        for key in args:
            ## If given update is real, switch out vals in curValues and args
            if (key in layout):
                inx = layout.index(key)
                curValues[inx] = args[key]

        ## Delete entry
        delOne(table, parm, value)

        ## Add new entry with new values
        addOne(table, *tuple(curValues))
