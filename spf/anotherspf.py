
import sys
import os,copy,math

class PriorityQueue:
    def __init__(self):
        self.heapArray = [(0,0)]
        self.currentSize = 0

    def buildHeap(self,alist):
        self.currentSize = len(alist)
        self.heapArray = [(0,0)]
        for i in alist:
            self.heapArray.append(i)
        i = len(alist) // 2
        while (i > 0):
            self.percDown(i)
            i = i - 1

    def percDown(self,i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapArray[i][0] > self.heapArray[mc][0]:
                tmp = self.heapArray[i]
                self.heapArray[i] = self.heapArray[mc]
                self.heapArray[mc] = tmp
            i = mc

    def minChild(self,i):
        if i*2 > self.currentSize:
            return -1
        else:
            if i*2 + 1 > self.currentSize:
                return i*2
            else:
                if self.heapArray[i*2][0] < self.heapArray[i*2+1][0]:
                    return i*2
                else:
                    return i*2+1

    def percUp(self,i):
        while i // 2 > 0:
            if self.heapArray[i][0] < self.heapArray[i//2][0]:
               tmp = self.heapArray[i//2]
               self.heapArray[i//2] = self.heapArray[i]
               self.heapArray[i] = tmp
            i = i//2

    def add(self,k):
        self.heapArray.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def delMin(self):
        retval = self.heapArray[1][1]
        self.heapArray[1] = self.heapArray[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapArray.pop()
        self.percDown(1)
        return retval

    def isEmpty(self):
        if self.currentSize == 0:
            return True
        else:
            return False

    def decreaseKey(self,val,amt):
        # this is a little wierd, but we need to find the heap thing to decrease by
        # looking at its value
        done = False
        i = 1
        myKey = 0
        while not done and i <= self.currentSize:
            if self.heapArray[i][1] == val:
                done = True
                myKey = i
            else:
                i = i + 1
        if myKey > 0:
            self.heapArray[myKey] = (amt,self.heapArray[myKey][1])
            self.percUp(myKey)

    def __contains__(self,vtx):
        for pair in self.heapArray:
            if pair[1] == vtx:
                return True
        return False

class Graph:
    def __init__(self):
        self.vertices = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex

    def addVertexName(self,key,name):
        self.vertices[key].name = name

    def getVertexName(self,key):
        return (self.vertices[key].name)

    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices

    def addEdge(self,f,t,cost=0):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t],cost)

    def getVertices(self):
        return list(self.vertices.keys())

    def __iter__(self):
        return iter(self.vertices.values())

class Vertex:
    def __init__(self,num):
        self.id = num
        self.connectedTo = {}
        self.color = 'white'
        self.dist = sys.maxsize
        self.pred = None
        self.disc = 0
        self.fin = 0
        self.name = ''

    # def __lt__(self,o):
    #     return self.id < o.id

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def setColor(self,color):
        self.color = color

    def setDistance(self,d):
        self.dist = d

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime

    def setFinish(self,ftime):
        self.fin = ftime

    def getFinish(self):
        return self.fin

    def getDiscovery(self):
        return self.disc

    def getPred(self):
        return self.pred

    def getDistance(self):
        return self.dist

    def getColor(self):
        return self.color

    def getConnections(self):
        return self.connectedTo.keys()

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

    def __str__(self):
        return str(self.id) + ":color " + self.color + ":disc " + str(self.disc) + ":fin " + str(self.fin) + ":dist " + str(self.dist) + ":pred \n\t[" + str(self.pred)+ "]\n"

    def getId(self):
        return self.id

def heightTree(bt):
    '''
    Prints the Height of the Tree. gets the Current Size Variable which keeps track of the total element in the tree.
    we take a log of the current size and returns the ceiling (Rounded number) which is the height of the tree.
    '''
    print ("height of the tree is", math.ceil((math.log(bt.currentSize,2))))

def levelOrderTraversal(bt):
    #level order Traversal for Tree
    j = 1
    while j <= bt.currentSize:
        if (2 * j) < bt.currentSize:
            j = 2 * j
        else:
            break
    level = math.ceil(math.log(j,2))
    ilevel = 0
    i = 1
    j = 2 ** ilevel
    print (bt.heapArray[1][1].name,end=' ')
    while (i < bt.currentSize) and (ilevel <= level):
        n=0
        print ("At Level",j)
        while n < j:
            if (2*(j+n)) < bt.currentSize:
                print (bt.heapArray[2*(j+n)][1].name,end=' ')
            if (2*(j+n)+1) < bt.currentSize:
                print (bt.heapArray[2*(j+n)+1][1].name,end=' ')
            n = n+1
        ilevel=ilevel+1
        j = 2 ** ilevel

def dijkstra(aGraph,start,end):
    #Create the Priority Queue
    pq = PriorityQueue()
    # Set the Start Node Distance to 0
    start.setDistance(0)
    '''
    Builds the Priority Queue (Min-Heap) by passing the Node Distance Attribute and the Node.This will Create the initial
    Tree and Position the Nodes according to there Distance
    '''
    pq.buildHeap([(v.getDistance(),v) for v in aGraph])

    levelOrderTraversal(pq)

    # Run the Loop until the Tree is Empty
    while not pq.isEmpty():
        # Pop the Root Node out of the tree and return. DelMin also re-arranges the Tree by putting the last element to
        # top of the Root Node and Reshuffling
        currentVert = pq.delMin()

        # Exit the Loop if the Current Node as the Destination Node
        if currentVert.id == end.id:
            break

        # Repeat the Process for each of the edges of the Current Node
        for nextVert in currentVert.getConnections():
            # (Current Node Dist) + (Edge Weight of Current Neighbor) = New Distance
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)

            # If the New Distance is less than the Current Node Neighbors Known Distance then
            if newDist < nextVert.getDistance():
                # Set the New Distance as the Distance of the Current Node's Neighbor
                nextVert.setDistance( newDist )
                # Set the Predecessor of the Current Node's Neighbor to the Current Node
                nextVert.setPred(currentVert.id)
                '''
                Perform Decrease Key Operation which is essentially Updating the Current Node Neighbors position in the
                tree according to the New Distance value aka Priority
                '''
                pq.decreaseKey(nextVert,newDist)

    #Code for Calculating Path from Predecessor
    path = []
    pred = end.pred
    path.insert(0,end.name)
    while True:
        path.insert(0,aGraph.getVertexName(pred))
        if pred == start.id:
            return list(path)
            break
        pred = aGraph.getVertex(pred).pred

'''
# Dont Need these Functions anymore but too much love to delete them
def path(g,start,end):
    path = []
    pred = end.pred
    path.insert(0,end.name)
    while True:
        path.insert(0,g.getVertexName(pred))
        if pred == start.id:
            return list(path)
            break
        pred = g.getVertex(pred).pred

def pathid(g,start,end):
    path_id = []
    pred= end.pred
    path_id.insert(0,end.id)
    while True:
        path_id.insert(0,pred)
        if pred == start.id:
            return list(path_id)
            break
        pred = g.getVertex(pred).pred

'''

def main():

    #Create a Graph Instance
    g=Graph()

    #Create 16 empty Node Instance in the Graph Instance

    for i in range (16):
        g.addVertex(i)
    #Fill the Edges in the Graph Instance between the Nodes and there Weights according to the Topology
    g.addEdge(0,1,10)
    g.addEdge(1,0,10)
    g.addEdge(0,1,10)
    g.addEdge(1,0,10)
    g.addEdge(0,8,10)
    g.addEdge(8,0,10)
    g.addEdge(0,5,10)
    g.addEdge(5,0,10)
    g.addEdge(5,6,10)
    g.addEdge(6,5,10)
    g.addEdge(6,8,10)
    g.addEdge(8,6,10)
    g.addEdge(8,9,10)
    g.addEdge(9,8,10)
    g.addEdge(8,11,10)
    g.addEdge(11,8,10)
    g.addEdge(11,13,10)
    g.addEdge(13,11,10)
    g.addEdge(13,9,10)
    g.addEdge(9,13,10)
    g.addEdge(13,14,10)
    g.addEdge(14,13,10)
    g.addEdge(1,9,100)
    g.addEdge(9,1,100)
    g.addEdge(1,2,100)
    g.addEdge(2,1,100)
    g.addEdge(9,14,100)
    g.addEdge(14,9,100)
    g.addEdge(2,9,10)
    g.addEdge(9,2,10)
    g.addEdge(9,10,10)
    g.addEdge(10,9,10)
    g.addEdge(2,3,10)
    g.addEdge(3,2,10)
    g.addEdge(3,4,10)
    g.addEdge(4,3,10)
    g.addEdge(2,7,10)
    g.addEdge(7,2,10)
    g.addEdge(3,7,10)
    g.addEdge(7,3,10)
    g.addEdge(4,7,10)
    g.addEdge(7,4,10)
    g.addEdge(7,10,10)
    g.addEdge(10,7,10)
    g.addEdge(12,10,10)
    g.addEdge(10,12,10)
    g.addEdge(14,12,10)
    g.addEdge(12,14,10)
    g.addEdge(12,15,10)
    g.addEdge(15,12,10)
    g.addEdge(10,15,10)
    g.addEdge(15,10,10)
    g.addVertexName(0,'SEA')
    g.addVertexName(1,'MIN')
    g.addVertexName(2,'CHI')
    g.addVertexName(3,'ALB')
    g.addVertexName(4,'BOS')
    g.addVertexName(5,'POR')
    g.addVertexName(6,'SFC')
    g.addVertexName(7,'NYC')
    g.addVertexName(8,'SJC')
    g.addVertexName(9,'KCY')
    g.addVertexName(10,'WDC')
    g.addVertexName(11,'LAX')
    g.addVertexName(12,'ATL')
    g.addVertexName(13,'SAN')
    g.addVertexName(14,'HST')
    g.addVertexName(15,'MIA')

    # Print the Path by Calling the Dijkstra Function, Passing hte Graph Instance, Source and Target Node.
    print (dijkstra(g,g.vertices[0],g.vertices[15]))


if __name__=="__main__":
    main()