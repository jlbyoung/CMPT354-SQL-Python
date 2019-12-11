# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc
from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
import sys

SERVER_NAME = 'cypress.csil.sfu.ca'
DATABASE_NAME = 'jlyoung354'
USERNAME = 'jlyoung'
PASSWORD = 'Girlsday5%'
listings = pd.DataFrame()
userReviews = pd.DataFrame()
reviews = pd.DataFrame()
bookings = pd.DataFrame()


def createConnection():
    conn = pyodbc.connect('Driver={SQL Server};Server=cypress.csil.sfu.ca;Database=jlyoung354; Trusted_Connection=yes;')
    cursor = conn.cursor()
    print('connection successful')
    return conn
    
    '''
    global db 
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(conn)
    
    if db.open():
        print('Connected to SQL Server')
        return True
    else:
        print('Connection failed')
        return False
    '''
    
    '''
def displayData(sqlStatement):
    print('processing query')
    qry = QSqlQuery(db)
    qry.prepare(sqlStatement)
    qry.exec()
    
    model = QSqlQueryModel()
    model.setQuer(qry)
    
    view = QTableView()
    view.setModel(model)
    return view
    '''
def chooseFunction(conn):
    user = 0    
    while True:
        print('Press Number for Function: \n1. Search Listings\n2. Book Listing\n3. Write Review\n4. Exit')
        user = input('Enter Number: ')
        if user == '1':
            searchListings(conn)
        elif user == '2':
            bookListing(conn)
        elif user == '3':
            writeReview(conn)
        elif user == '4':
            break

### SEARCH LISTINGS #########################
def searchListings(conn):
    print('Search Listings')
    user = 0
    beds = 2
    start = '2016-01-01'
    end = '2017-06-21'
    minP = 0
    maxP = 1000000
    while True:
        print('Press Number for Filter: \n1. Min/Max Price\n2. Number of Bedrooms\n3. Start and End Date\n4. Submit')
        user = input('Enter Number: ')
        if user == '1':
            ##min/max price
            minP = input('Enter Min Price: ')
            maxP = input('Enter Max Price: ')
        elif user == '2':
            ##num of bedrooms
            beds = input('Enter Number of Bedrooms: ')
        elif user == '3':
            ##start and end date
            start = input('Enter start date in YYYY-MM-DD form: ')
            end = input('Enter end date in YYYY-MM-DD form: ')
            ##start = datetime.strptime(start, '%Y-%m-%d').date()
            ##end = datetime.strptime(end, '%Y-%m-%d').date()
            ##print(type(start))
        elif user == '4':
            break
    print(user)
    if user == '4':
        searchCommand(conn, minP, maxP, beds, start, end)

def searchCommand(conn, minP, maxP, beds, start, end):
    SQLCommand = ''
    SQLCommand = f'''
    SELECT L.id, L.name, L.description, L.number_of_bedrooms, C.price 
    FROM Listings L 
    INNER JOIN Calendar C ON L.id = C.listing_id 
    WHERE C.price >= {minP} AND C.price <= {maxP} AND L.number_of_bedrooms = {beds} AND C.available = 1 AND C.date >= \'{start}\' AND C.date <= \'{end}\'
    '''
    SQLCommand = SQLCommand
    executeSearch(conn, SQLCommand)
        
def executeSearch(conn, SQLCommand):
    print('Search Listings')
    print(SQLCommand)
    global listings
    listings = pd.read_sql(SQLCommand, conn)
    print(listings)
    
###########################################
### BOOK LISTINGS ######################
def bookListing(conn):
    global listings
    global bookings
    print('Book Listing')
    SQLCommand = f'INSERT INTO Bookings(name, stay_from, stay_to, number_of_guests)'
    executeBooking(conn, SQLCommand)
    
def executeBooking(conn, SQLCommand):
    cursor = conn.cursor()
    SQLBookings = 'SELECT * FROM Bookings'
    bookings = pd.read_sql(SQLBookings, conn)
    bid = bookings.iloc[-1]['id'] + 1
    name = input('Enter your name: ')   
    stay_from = input('Enter your check in date in format YYYY-MM-DD: ')
    stay_to = input('Enter your check out date in format YYYY-MM-DD: ')
    num_of_guests = input('Enter the number of guests: ')
    SQLCommand += 'VALUES(?, ?, ?, ?, ?)'
    Values = [bid, name, stay_from, stay_to, num_of_guests]
    cursor.execute(SQLCommand, Values)
    conn.commit()
########################################

### WRITE REVIEWS ######################
def writeReview(conn):
    print('Write Review')
    name = input('Enter your name: ')
    searchUserReviews(name)
    SQLCommand = f'INSERT INTO Reviews(id, listing_id, comments)'
    executeWrite(conn, SQLCommand)
    
def searchUserReviews(name):
    SQLCommand = ''
    SQLCommand += 'SELECT * FROM Bookings B'
    SQLCommand += f'WHERE B.guest_name = {name}'
    userReviews = pd.read_sql(SQLCommand, conn)
    print(userReviews)
    
def executeWrite(conn, SQLCommand):
    cursor = conn.cursor()
    SQLReviews = 'SELECT * FROM Reviews'
    reviews = pd.read_sql(SQLReviews, conn)
    rid = reviews.iloc[-1]['id'] + 1
    reviewListID = input('Enter listing ID you want to write review for: ')
    reviewText = input('Type your review: ')
    SQLCommand += 'VALUES(?, ?, ?)
    Values = [rid, reviewListID, comments]
    cursor.execute(SQLCommand, Values)
    conn.commit()
#######################################
    
    
if __name__=='__main__':
    app = QApplication(sys.argv)
    
    conn = createConnection()
    if conn:
        chooseFunction(conn)
        ##chooseFunction()
        ##SQL_STATEMENT = ''
        ##dataView = displayData(SQL_STATEMENT)
        ##dataView.show()
    conn.close()
    
    app.exit()