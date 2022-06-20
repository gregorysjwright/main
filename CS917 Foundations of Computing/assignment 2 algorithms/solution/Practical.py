import itertools
import csv


# Binary Search Tree to store the letters in the alphabet. Each node is a letter. A left traverse is equivalent to a '-'.
# A right traverse is equivalent to a '.'
# The tree class has only the most basic functionality for which is needed for the problem
class BinaryTree:
    def __init__(self):
        self.left = None  #'child' node
        self.right = None #'child' node
        self.value = None # letter stored

    def insert(self, morse, value): # add a letter to the tree based on the given morse code
        if len(morse) == 0:
            self.value = value
        elif morse[0] == '-': # left traversal
            if self.left == None:
                self.left = BinaryTree()
            self.left.insert(morse[1:], value)
        elif morse[0] == '.': # right traversal
            if self.right == None:
                self.right = BinaryTree()
            self.right.insert(morse[1:], value)
        else:
            print("error, invalid morse code entered!")
        
    def search(self, sequence): # traverses the tree to find a corresponding letter to the morse code given
        if len(sequence) == 0:
            return self.value
        elif sequence[0] == 'x': # handles x case by returning a list of 2 letters instead of one.
            return (self.left.search(sequence[1:]), self.right.search(sequence[1:]))
        elif sequence[0] == '-':
            if self.left == None: # case no letter exists
                return None
            else:
                return self.left.search(sequence[1:])
        elif sequence[0] == '.':
            if self.right == None: # case no letter exists
                return None 
            else:
                return self.right.search(sequence[1:])
        else:
            print("error, invalid morse code entered!")



### finds the corresponding letter (or letters) to the morse code sequence 
def decode(morseLetter, tree):
    return tree.search(morseLetter)
        


def morseDecode(inputStringList):
    """
    This method should take a list of strings as input. Each string is equivalent to one letter
    (i.e. one morse code string). The entire list of strings represents a word.

    This method should convert the strings from morse code into english, and return the word as a string.
    
    """
    ### creates a binary tree and stores the letters of the alphabet in it.
    ### Note this is run everytime morseDecode is called. Instead this would be defined in a more global scope but is left here to not cause issues with your testing  
    tree = BinaryTree()
    alphabetMorseTable = [ ["A", ".-"],["B", "-..."],["C", "-.-."],["D", "-.."],["E", "."],["F", "..-."],["G", "--."]
                           ,["H", "...."],["I", ".."],["J", ".---"],["K", "-.-"],["L", ".-.."],["M", "--"],["N", "-."],["O", "---"]
                           ,["P", ".--."],["Q", "--.-"],["R", ".-."],["S", "..."],["T", "-"],["U", "..-"],["V", "...-"],["W", ".--"],
                           ["X", "-..-"],["Y", "-.--"],["Z", "--.."]]
    for map1 in alphabetMorseTable:
        tree.insert(map1[1], map1[0]);

    ###
    
    ### decodes each morse code 'letter' into the corresponding letter. Then appends it to the word
    word=""
    for string in inputStringList:
        letter = decode(string, tree)
        word = word + letter
    ###
        
    return word


# searchs the given file data and checks to see if each word is contained within it. Linear Search used.
def searchWordList(wordCheckList, data):
    words =[]
    for i in range(0, len(wordCheckList)):
        for line in data:
            if wordCheckList[i].upper() == line.upper().strip():
                words.append(wordCheckList[i].upper())
    return words


# The letters found from the tree search() function results in an array of the form [ [A,B],[A,B],[A,B], ... ] where A & B are the two possible letters due to the 'x' in the morse code.
# This functions converts this into a list of all possible combinations of letters (potential words) and stores it in 'words'. Recursion implemented.
def findWords(letterCombs, i, partialWord, words):
    # Each call creates 2 new calls with the partial word updated with both possible combinations until the end of the list is reached.
    if letterCombs[i][0] != None: # case x=- exists
        newPartialWord = partialWord + letterCombs[i][0]
        if i == len(letterCombs)-1:
            words.append(newPartialWord)
        else:
            findWords(letterCombs, i+1, newPartialWord, words)    
    if letterCombs[i][1] != None: # case x=. exists
        newPartialWord2 = partialWord + letterCombs[i][1]
        if i == len(letterCombs)-1:
            words.append(newPartialWord2)
        else:
            findWords(letterCombs, i+1, newPartialWord2, words)

def morsePartialDecode(inputStringList):
    ### creates a binary tree and stores the letters of the alphabet in it.
    ### Note this is run everytime morseDecode is called. Instead this would be defined in a more global scope but is left here to not cause issues with your testing  
    tree = BinaryTree()
    alphabetMorseTable = [ ["A", ".-"],["B", "-..."],["C", "-.-."],["D", "-.."],["E", "."],["F", "..-."],["G", "--."]
                           ,["H", "...."],["I", ".."],["J", ".---"],["K", "-.-"],["L", ".-.."],["M", "--"],["N", "-."],["O", "---"]
                           ,["P", ".--."],["Q", "--.-"],["R", ".-."],["S", "..."],["T", "-"],["U", "..-"],["V", "...-"],["W", ".--"],
                           ["X", "-..-"],["Y", "-.--"],["Z", "--.."]]
    for map1 in alphabetMorseTable:
        tree.insert(map1[1], map1[0]);

    ### Reads the file where the list of all possible words are stored
    dictionaryFileLoc = './dictionary.txt'
    data = []
    with open(dictionaryFileLoc) as fp:
        Lines = fp.readlines()

    ### decodes each morse code 'letter' into the corresponding 2 letter combination. Then appends it to the word
    words=[]
    word = []
    for string in inputStringList:
        letter = decode(string, tree)
        word.append(letter)
    ### converts this to a list of possible words
    findWords(word, 0, "", words)

    return searchWordList(words, Lines)  # returns the subset that are within the dictionary file 
    
# Class for a 'vertex' within the graph/maze. The coordinate is the name of the vertex. A list of neighbours for each vertex. Whether the vertex has been traversed. Finally the previous vertex that has been traversed.
class Vertex:
    def __init__(self,x,y):
        self.coord = (x,y)
        self.neighbours = list()
        self.discovered = False
        self.previous = self.coord
    def add_neighbour(self, v): # adds a 
        if v not in self.neighbours:
            self.neighbours.append(v)   

# effectively a class for a graph
class Maze:
    def __init__(self):
        #stores list of vertices, i.e. the graph
        self.vertices = dict()
        ## stores the grid size for the maze
        self.M = 0
        self.N = 0
        ##
        
    def update_neighbours(self,x, y): # add a 'neighbour'/defines an edge for a graph node/vertex
        for coord in self.vertices.keys(): # explicitly checks to see if adjacent grid points are within the current list of vertices, if so creates an edge between them.
            if coord == (x-1,y) or coord == (x+1,y) or coord == (x,y-1) or coord == (x,y+1):
                self.vertices[coord].add_neighbour(self.vertices[(x,y)])
                self.vertices[(x,y)].add_neighbour(self.vertices[coord])
                
    def addCoordinate(self,x,y,blockType):
        ## updates grid size on a rolling basis each time a coordinate is added
        if x >= self.M:
            self.M = x+1
        if y >= self.N:
            self.N = y+1
        ##
        if blockType == 0: # can ignore the vertex if it's a wall. By default, it is considered a wall. The grid size is already updated.
            ## adds new vertex/node to graph and updates the edges to be all the adjacent nodes(coordinates) that are already within the graph
            vertex = Vertex(x,y)
            self.vertices[vertex.coord] = vertex
            self.update_neighbours(x,y)
            ##

    
    def dfsOrBfs(self, start, end): # determines whether to use dfs or bfs based on start and endpoints provided. #start end are the grid coordinates form (i,j)
        X = self.M*self.M + self.N*self.N # X = |(M,N)|^2
        x1,y1 = start
        x2,y2 = end
        Y = (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) # Y = |start - end|^2
        if X>=4*Y: # i.e grid/maze size more than double start to end point length. Double chosen arbitrarily.
            return False # use bfs
        else:
            return True # use dfs
            
    def resetDiscoveredVertices(self): # performed after a depth first search to reset the 'discovered node' record when dfs has completed.
        for coord in self.vertices.keys():
            self.vertices[coord].discovered = False

    def getFavouriteNeighbour(self, neighbours, end): # dfs performed heuristically to find a 'good enough' path through the maze. May not overall be the one with minimal steps.
        # returns the preferential Neighbour of the list of neighbours based on the resulting 'distance' to the maze endpoint (i.e. neighbour closest to the endpoint)
        if len(neighbours)==1:
            return neighbours[0]
        else:
            magSquared = 0
            for neighbour in neighbours:
                x,y = neighbour.coord
                X,Y = end
                temp = (x-X)*(x-X) + (y-Y)*(y-Y) # calculates square of the distance of the neighbour and endpoint
                if temp < magSquared or magSquared == 0:
                    magSquared = temp
                    favourite = neighbour
            return favourite
        
            
    def dfs(self, v, start, end, path=[]): # depth first search recursive procedure on graph. Each call of dfs traverses one 'open space' on the grid. Breaks when 'a' NOT 'the/the optimal' route is found
        if v.coord == end: # if we have reached the endpoint, simply add the endpoint to the path
            path.append(end)
        else:
            v.discovered = True # indicates the node has been checked for future recursive calls
            neighbours = []
            for neighbour in v.neighbours: # creates temporary neighbour list of neighbours that havnt been traversed yet
                if (neighbour.discovered == False):
                    neighbours.append(neighbour)
            
            for i in range(0, len(neighbours)):
                neighbour = self.getFavouriteNeighbour(neighbours,end) # gets 'favourite' neighbour/closest to endpoint to try next.
                if (neighbour.discovered == False): #checks neighbour hasnt been traversed again
                    neighbours.remove(neighbour) # remove neighbour from temporary list so it isnt checked again in getFavouriteNeighbour call.
                    self.dfs(neighbour, start, end, path) 
                    if path != []: # indicates the recursion has found a solution ahead so add this point to the path. breaks to prevent unnecessary traversal (implications i.e. finds a not the best route)
                        path.append(v.coord)
                        break

    def bfs(self, queue, end): # bread first search recursive procedure on graph. Breaks when the optimal path is found (shortest number of steps). i.e similar to djikstras algorithm with equal weightings
        
        l = len(queue)
        for i in range(0, l): # for each vertex in queue, add it's neighbours to queue that havnt been 'discovered yet', remove the element from the queue and record it as discovered,  
            
            v = queue.pop(0)
            if v.coord == end:
                queue=[]
                break
            else:
                for neigh in v.neighbours:
                   if neigh.discovered == False:
                       queue.append(neigh)
                       neigh.previous = v.coord # set previous vertex record to the ones added to the queue
                       neigh.discovered = True
        if len(queue)>0:
            self.bfs(queue, end) # repeat

        
    def resetPrevious(self): # reset the stored previous nodes
        for coord in self.vertices.keys():
            self.vertices[coord].previous = self.vertices[coord].coord


    def getBfsPath(self, start, vertex, path): # backtracks each vertex from endpoint to get list of previous nodes
        if vertex.previous != start:
            path.append(vertex.previous)
            self.getBfsPath(start, self.vertices[vertex.previous], path)
        else:
            path.append(start)

            
    def printMaze(self):
        # creates an ascii grid with all '*'s (walls)
        grid = []
        for i in range(0, self.N):
            row = []
            for j in range(0,self.M):
                row.append("*")
            grid.append(row)
        # manually replaces 'walls' with 'open space / " " ' at the vertices
        for coord in self.vertices.keys():
            grid[coord[1]][coord[0]] = " "

        # prints resulting grid/maze
        for row in grid:
            print("".join(row))

    def findRoute(self,x1,y1,x2,y2): # finds the route through the maze by calling the recursive dfs procedure. Stores the resulting path list in 'path' and returns it
        path = [] # stores path through maze as coordinates

        try:    
            if self.dfsOrBfs((x1,y1), (x2,y2)): # depth first search if maze is 'large' compared to distance from start to end points
                self.dfs(self.vertices[(x1,y1)],(x1,y1),(x2,y2), path) # initially the first vertex is the start coordinate
            else: # breadth first search if maze is 'small' compared to distance from start to end points
                path = [(x2,y2)] # initially endpoint
                self.bfs([self.vertices[(x1,y1)]], (x2,y2))
                self.getBfsPath((x1,y1),self.vertices[(x2,y2)], path) # works out path from recorded previous nodes
                self.resetPrevious()
            self.resetDiscoveredVertices()
            if path[0] == path[1]: # case start = end
                return [path[0]]
            else:
                return list(reversed(path)) # due to recursive nature, the path coordinates obtained are in reverse
        except:
            return []
def morseCodeTest():
    """
    This test program passes the morse code as a list of strings for the word
    HELLO to the decode method. It should receive a string "HELLO" in return.
    This is provided as a simple test example, but by no means covers all possibilities, and you should
    fulfill the methods as described in their comments.
    """

   
    hello = ['....','.','.-..','.-..','---']
    print(morseDecode(hello))

def partialMorseCodeTest():

    """
    This test program passes the partial morse code as a list of strings 
    to the morsePartialDecode method. This is provided as a simple test example, but by
    no means covers all possibilities, and you should fulfill the methods as described in their comments.
    """

    # This is a partial representation of the word TEST, amongst other possible combinations
    test = ['x','x','x..','x']
    print(morsePartialDecode(test))

    # This is a partial representation of the word DANCE, amongst other possible combinations
    dance = ['x..','x-','x.','x.-.','x']
    print(morsePartialDecode(dance))

    quest = ['x-.-','x.-','x','x..','x']
    print(morsePartialDecode(quest))
def mazeTest():
    """
    This sets the open space coordinates for the example
    maze in the assignment.
    The remainder of coordinates within the max bounds of these specified coordinates
    are assumed to be walls
    """
    myMaze = Maze()
    myMaze.addCoordinate(1,0,0) # Start index
    myMaze.addCoordinate(1,1,0)
    #myMaze.addCoordinate(1,2,0)
    myMaze.addCoordinate(1,3,0)
    myMaze.addCoordinate(1,4,0)
    myMaze.addCoordinate(1,5,0)
    myMaze.addCoordinate(1,6,0)
    myMaze.addCoordinate(1,7,0)

    myMaze.addCoordinate(2,1,0)
    myMaze.addCoordinate(2,2,0)
    myMaze.addCoordinate(2,3,0)
    myMaze.addCoordinate(2,6,0)

    myMaze.addCoordinate(3,1,0)
    myMaze.addCoordinate(3,3,0)
    myMaze.addCoordinate(3,4,0)
    myMaze.addCoordinate(3,5,0)
    myMaze.addCoordinate(3,7,0)
    myMaze.addCoordinate(3,8,0) # End index

    myMaze.addCoordinate(4,1,0)
    myMaze.addCoordinate(4,5,0)
    myMaze.addCoordinate(4,7,0)

    myMaze.addCoordinate(5,1,0)
    myMaze.addCoordinate(5,2,0)
    myMaze.addCoordinate(5,3,0)
    myMaze.addCoordinate(5,5,0)
    myMaze.addCoordinate(5,6,0)
    myMaze.addCoordinate(5,7,0)

    myMaze.addCoordinate(6,3,0)
    myMaze.addCoordinate(6,5,0)
    myMaze.addCoordinate(6,7,0)

    myMaze.addCoordinate(7,1,0)
    myMaze.addCoordinate(7,2,0)
    myMaze.addCoordinate(7,3,0)
    myMaze.addCoordinate(7,5,0)
    myMaze.addCoordinate(7,7,0)
    myMaze.addCoordinate(10,10,0)
    myMaze.printMaze()
    # TODO: Test your findRoute method
    print(myMaze.findRoute(1,0,3,8))
def main():
    #morseCodeTest()
    #partialMorseCodeTest()
    mazeTest()

    

if __name__ == "__main__":
    main()
