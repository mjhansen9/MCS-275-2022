#The aim of this project was to create a SQLite database but a csv file containing data about Chicago's bus network. 
#I then used SQLite to  extract information about, and perform a variety of transformations on the data.

#Madeline Hansen
#UIN: 667606386
#email: mhanse21@uic.edu
#Project 3

#I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s
#Academic Integrity standards. Signed: Madeline Hansen

import sqlite3
import pandas
import matplotlib.pyplot as plt 

def convert():
    """extracts all
the data from the csv file bus data.csv and puts it all into a SQLite database called bus data.db"""
    data = pandas.read_csv("bus_data.csv")
    con = sqlite3.connect('bus_data.db')
    curs = con.cursor()
    curs.execute("CREATE TABLE busdata (route text, date text,daytype text,rides int)")
    for i in range(len(data)):
        rt=data['route'][i]
        rt="'"+rt+"'"
        dt=data['date'][i]
        dt="'"+dt+"'"
        dyt=data['daytype'][i]
        dyt="'"+dyt+"'"
        rd=data['rides'][i]
        curs.execute("INSERT INTO busdata VALUES (%s,%s,%s,%d)"%(rt,dt,dyt,rd))
    #result=curs.execute("SELECT * FROM busdata")
    #for i in result:
        #print(i)
    #above code used to test to make sure the data was entered correctly 
    con.commit()
    con.close()
    
#convert()
#the bus_data.csv file takes up 19,854 KB of memory
#the bus_data.db file takes up 24,664 KB of memory

def route_data(rte):
    """takes as input a specified route (as a string) and
prints two things: the average daily ridership for that route, and the percentage of days for which
that route is in heavy use"""
    con = sqlite3.connect('bus_data.db')
    curs = con.cursor()
    out1 = curs.execute("SELECT AVG(rides) FROM busdata WHERE route={}".format(rte)).fetchall()[0][0]
    #the [][] makes it so out1 is just the number, rather than the number being contained within a list
    out2 = curs.execute("SELECT COUNT(rides) FROM busdata WHERE rides>1199 AND route={}".format(rte)).fetchall()[0][0]
    #I noticed that this defininition of 'heavy use' is fairly low for a lot of the routes, with some nearing 100% heavy use
    out3 = curs.execute("SELECT COUNT(rides) rides FROM busdata WHERE route={}".format(rte)).fetchall()[0][0]
    percent=str(round(100*(out2/out3),2))+'%'
    #the above is used to format the percetange value into it's usual format
    print('average daily riders=',out1,'\npercentage of days route is in heavy use=',percent)
    
#route_data('43')


def yr_sum(*args):
    """ computes and prints the sum total of all rides for the
specified year"""
    con = sqlite3.connect('bus_data.db')
    curs = con.cursor()
    L=[]
    for i in args:
        out = curs.execute("SELECT SUM(rides) FROM busdata WHERE date LIKE '%{}'".format(i)).fetchall()[0][0]
        L.append(out)
    for l in range(len(L)):
        print('total rides for',args[l],'=',L[l])
    #the use of for loops is to account for the unknown number of args entered, the order should be the same in each list so args[l] should match to L[l]

#yr_sum(2001,2015)

def my_func():
    """creates a matplotlib graph to view trends in ridership over time (looking specifically at monthly sums)"""
    con = sqlite3.connect('bus_data.db')
    curs = con.cursor()
    yrsmon=[]
    for year in range(2001,2023):
        for month in range(1,13):
            #this creates a list of month year pairs that contains all the month year pairs contained in the data
            if month<10:
                month='0'+str(month)
                #this makes it so the string will match the string in the data with single digit months
            else:
                month=str(month)
            yrsmon.append([month,str(year)])
    yrsmon=yrsmon[:-5]
    #to account for data not collected near the end of 2022
    y=[]
    for i in yrsmon:
        ridespermon = curs.execute("SELECT SUM(rides) FROM busdata WHERE date LIKE '{}%{}'".format(i[0],i[1])).fetchall()[0][0]
        #the above uses string formatting to have it look at each monthyear pair in the list yrsmon and SUM all the rides 
        y.append(ridespermon)
    x=[]
    for i in yrsmon:
        x1=i[1]+'.'+i[0]
        x.append(x1)
    plt.plot(x, y)
    plt.show()
    #each year seems to peak in the autumn and early winter, before dropping off 
    #at the beginning of year. huge pbvious drop during 2020 and has yet to recover
    #to pre covid numbers
    
#my_func()

def update():
    """decreases the value of each "A" day by 10 percent, rounded down"""
    con = sqlite3.connect('bus_data.db')
    curs = con.cursor()
    data = curs.execute("SELECT * FROM busdata").fetchall()
 
    conduplicate = sqlite3.connect('bus_data_backup.db')
    cursduplicate = conduplicate.cursor()
    cursduplicate.execute("CREATE TABLE busdatadup (route text, date text,daytype text,rides int)")
    for i in range(len(data)):
        rt=data[i][0]
        rt="'"+rt+"'"
        dt=data[i][1]
        dt="'"+dt+"'"
        dyt=data[i][2]
        dyt="'"+dyt+"'"
        rd=data[i][3]
        cursduplicate.execute("INSERT INTO busdatadup VALUES (%s,%s,%s,%d)"%(rt,dt,dyt,rd))
    conduplicate.commit()
    conduplicate.close() 

    
    
    curs.execute("UPDATE busdata SET rides=FLOOR(rides*.9) WHERE daytype LIKE 'A'")
    con.commit() 
    con.close()    
    result=curs.execute("SELECT rides FROM busdata WHERE daytype LIKE 'A'")
 
    
#update()