#the aim of this project is the calculate the average time a simulated commute would take.
#Madeline Hansen
#UIN: 667606386
#email: mhanse21@uic.edu
#Project 1

#I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s
#Academic Integrity standards. Signed: Madeline Hansen


import random

def one_step(x,y):
    """takes in 2 arguments 'x' and 'y' representing the computers current placement on the map. The function will generate random wait times for 'up' and 'down'  
    and will choose to take the path with the least wait time (it will choose up in the case where the wait times are equal. The function will then return a tuple containing
    the new values for x and y, as well as the resulting wait time."""
    Up=random.uniform(0,75)
    Right=random.uniform(0,75)
    #to make sure the code wouldn't continue to go further up or right after hitting an edge, I made if and elif statements to 
    #check to see if the position is at an edge of the grid or not (and if so, which edge)
    if(1<=x<5)and(1<=y<5):
        #starting position is not at either the top or right side of the grid
        if Right>Up:
            x+=1
            waittime=Right
        else:
            y+=1
            waittime=Up
        #this makes it so that 'right' is only selected if it is strictly larger than 'up', so if they tie it goes to 'up'
    elif(0<=x<5)and(y==5):
        #starting postion is at the top of the grid but not the right side of the grid
        #no need to check which direction is bigger here or in the elif below, as it only has one directional option
        x+=1
        waittime=Right
    elif(x==5)and(0<=y<5):
        #starting position is on the right side of the grid, but not yet at the top
        y+=1
        waittime=Up
    return (x,y,waittime)


def one_commute():
    """Simulates a single commute from the lower left to the upper right. This function takes no inputs, and returns the total travel time simulated."""
    x=1
    y=1
    #starting position on the grid set to (1,1)
    totalwaittime=0
    while x<5 or y<5:
        onesteptuple=one_step(x,y)
        totalwaittime+=onesteptuple[2]
        x=onesteptuple[0]
        y=onesteptuple[1]
    #x and y will both equal to 5 at this point, thus being at the upper right corner of the grid
    return totalwaittime
        
#one_commute()

def month_max(): 
    """This function simulates all the commutes for a month (using one_commute) and calculates the maximum travel time out of all commutes for that month. 
    This function takes no inputs, and returns the maximum travel time for that month."""
    #In a month, you drive this commute a random number of times, assume its a random integer from 15 to 25
    numberofdrives=random.randint(15,25)
    drivetimes=[]
    #creates a list of all the commute times in the month, which the below for loop add in
    for i in range(numberofdrives):
        drivetimes.append(one_commute())
    maxtime=max(drivetimes)
    #searches the list of drives times and find the maximum number, setting that equal to the maxtime variable
    return maxtime
    
#print(month_max())
        

def ave_max(n):
    """This function runs month max multiple times, and then takes the average of all the maximum travel times generated. This function takes in the input n, which is
    the number of maximum travel times that should be generated before computing the average. It returns the average maximum
    travel time."""
    maximums=[]
    for i in range(n):
        maximums.append(month_max())
        #this will run the code n times and append the result to the maximums list
    average=(sum(maximums)/n)
    #finds the average value of all the elements in maximums
    minutes=int(average//60)
    #intger divison so that we get the number of minutes without any remainder
    seconds=int(average%60)
    #modular division so that we get seconds remaining
    print('The average maximum travel time was',minutes,'minutes and',seconds,'seconds.')
    return average
    
#ave_max(10000)

#as seen above, I tested the code using an n=10,000 and usually that resulted in an average of 7 minutes and 49 seconds (althought rarely
#I would get 7 min and 50 seconds). that results in an average wait at a stop to be about 58 seconds, just a bit less than a minute per stop. when 
#compared to a maximum of 75 seconds per stop, it is obviously lower.
    