#the aim of this project was to create a puzzle solver that creates a virtual puzzle and then cycles through all of the pieces (which are objects)
# to find its matches, until the puzzle is solved.

#Madeline Hansen
#UIN: 667606386
#email: mhanse21@uic.edu
#Project 1

#I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s
#Academic Integrity standards. Signed: Madeline Hansen

import random
import matplotlib.pyplot as plt

class PuzzlePiece:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.connected_to=[]
        self.secret_id=(self.x,self.y)
    def __str__(self):
        return str(self.secret_id)
#the above code creates a single 'puzzle piece' object which is really just a set of coordinates on a grid spanning [0,9] on both
#the x and y axis there are 100 possible unique coordinates. the x and y values of the coordinates are stored as attributes

class Puzzle:
    def __init__(self):
        self.u_pieces=[]
        self.s_pieces=[]
        for y in range(10):
            for x in range(10):
                piece=PuzzlePiece(x,y)
                self.u_pieces.append(piece)
        #the above code creates 100 PuzzlePiece objects (all 100 possible unique coordinates) and adds them to the previously
        #empty 'u_pieces' representing the pieces not yet solved (all of them at this point)
    def get_rand_piece(self):
        piece=random.randint(0,len(self.u_pieces)-1)
        return self.u_pieces[piece]
        #this grabs a random piece from the unsolved list
    def solve_one_piece(self):
        newpiece=self.get_rand_piece()
        if len(self.s_pieces)==0:
            self.s_pieces.append(newpiece)
            self.u_pieces.remove(newpiece)
            #this checks to see if there are any objects in the 'solved' list, and if it's empty, it grabs a random piece
            #using the previosly defined get_random_piece and throws it in the solved list, making it the base piece
        else:
            for piece1 in self.s_pieces:
                if (newpiece.secret_id[0]==piece1.secret_id[0]) and ((newpiece.secret_id[1]-piece1.secret_id[1])==1):
                #ie the x coordinates are the same and the y coordinate
                # of newpiece is 1 greater than the y coordinate of piece
                #(ie ie the randomly choosen piece is connceted to the top of the piece)
                    newpiece.connected_to.append(piece1)
                    piece1.connected_to.append(newpiece)
                elif (newpiece.secret_id[0]==piece1.secret_id[0]) and ((newpiece.secret_id[1]-piece1.secret_id[1])==-1):
                #ie the x coordinates are the same and the y coordinate
                # of newpiece is 1 less than the y coordinate of piece
                #(ie ie the randomly choosen piece is connceted to the bottom of the piece)
                    newpiece.connected_to.append(piece1)
                    piece1.connected_to.append(newpiece)
                elif (newpiece.secret_id[1]==piece1.secret_id[1]) and ((newpiece.secret_id[0]-piece1.secret_id[0])==1):
                #ie the y coordinates are the same and the x coordinate
                # of newpiece is 1 greater than the y coordinate of piece
                #(ie ie the randomly choosen piece is connceted to the right of the piece)
                    newpiece.connected_to.append(piece1)
                    piece1.connected_to.append(newpiece)
                elif (newpiece.secret_id[1]==piece1.secret_id[1]) and ((newpiece.secret_id[0]-piece1.secret_id[0])==-1):
                #ie the y coordinates are the same and the x coordinate
                # of newpiece is 1 greater than the y coordinate of piece
                #(ie ie the randomly choosen piece is connceted to the left of the piece)
                    newpiece.connected_to.append(piece1)
                    piece1.connected_to.append(newpiece)
            #the above code checks a randomly grabbed piece against all the pieces in the solved list
            #to see if it connects to any of the pieces 'already on the board'. if it does, it adds the connecting pieces
            #to each other's 'connected to' lists
            if len(newpiece.connected_to)>0:
                self.s_pieces.append(newpiece)
                self.u_pieces.remove(newpiece)
                #this checks to see if the piece connected with any of the pieces in the solved list
                #if so, the piece is added to the solved list and removed from the unsolved list
                #if not, it does nothing ('throwing it back into the unsolved pile')
                
    def solve_all_pieces(self):
        if len(self.u_pieces)>0:
            self.solve_one_piece()
            self.solve_all_pieces()
            #this calls the solve_one_piece function, and then recursively calls itself until the unsolved list is empty, thus 'solving'
            #the puzzle
            
    def solution_graph(self):
        X=[coordinate.x for coordinate in self.s_pieces]
        Y=[coordinate.y for coordinate in self.s_pieces]
        #uses list comprehensions to create 2 lists of X and Y coordinates, where X[i] and Y[i] would be a coordinate pair
        #the values are added to the lists in the order they appear in the s_solved list, so they are in order of when they
        #were solved
        for i in range(100):
            plt.plot(X[i],Y[i],marker='X',color=(i/100, 1-i/100, 1-i/100))
        #this plots each point in order that they appear in their respective lists with the color changing the 
        #later the point appears in the lists. the sooner they appear in the list (and thus the sooner they were solved)
        #the more teal they are, the later they appear (and thus the later they were solved) the more red they are
        plt.show()
        
        
                    
                
            
            

#below is some of the code I used to test the above code
            
X=Puzzle()
#print('u.pieces before=',len(X.u_pieces))
#print('s.pieces before=',len(X.s_pieces))
X.solve_all_pieces()
#print('u.pieces after=',len(X.u_pieces))
#print('s.pieces after=',len(X.s_pieces))
#print('root piece=',X.s_pieces[4])
#for i in X.s_pieces[4].connected_to:
 #   print(i)
for i in X.s_pieces:
    print(i)

X.solution_graph()

