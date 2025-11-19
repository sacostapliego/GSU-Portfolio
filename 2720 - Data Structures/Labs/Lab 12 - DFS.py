class Graph:
    def __init__(self, V):
        #Number of vertices
        self.V = V 
        #Adjacent lists
        self.adj = {}
        
        #Initialize ajaceny lists for all vertices
        for i in range(V):
            self.adj[i] = []

    def add_edge(self, v, w):
        #Ensure V is in the dictionary
        if v not in self.adj:
            self.adj[v] = []
        #Add w to the adjacency list of v
        self.adj[v].append(w)

#Recursive
def recursive(graph, current, visit):
    #current node is visited, add it to visit set
    visit.add(current)
    #Print the value of the current 
    print(current, end=" ")

    #Recursively go through all vertices adjacent to current vertex
    for i in graph.adj[current]:
        if i not in visit:
            recursive(graph, i, visit)

#Time Copmlexity: O(V + E)
#Each verticies (V) and edge (E) will be visited once in the worst case sceneario. 
    
#Space Complexity: O(V)
#Recursive means that the depth can be the number of verticies in the graph, which will therefore mean the space
#will be the number of verticies(V)

#Code from Lab
g = Graph(6)
g.add_edge(0,1)
g.add_edge(0,2)
g.add_edge(2,3)
g.add_edge(2,4)
g.add_edge(4,5)
g.add_edge(1,3)
g.add_edge(3,5)

#Example from lab executed
print("DFS: ",end=" ")
example = set()
recursive(g, 0, example)

"""The way that I would test the user is whenever they
    input a graph with a certain number of vertices, the program will check if they
    are entering numbers and not strings using exception"""

try:
    #The user would need to input the proper numbers in order for the program to execute
    print("\n\nExample 1")
    g = Graph(3)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(1,2)

    print("DFS: ",end=" ")
    example = set()
    recursive(g, 0, example)

    print("\n\nEample 2")
    g = Graph(3)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(1,100)

    print("DFS: ",end=" ")
    example = set()
    recursive(g, 0, example)


except:
    print("Error")