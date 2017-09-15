from apq import APQ

class Vertex:
    """Class to implement Vertex ADT

       Attributes:
       self._elt : the element contain in the vertex

       Methods:
       __init__ : constructor method to initialise the class
       element : returns the vertex's element
       __str__ : method to print a string representation of the vertex
    """
    def __init__(self, element):
        self._element = element

    def element(self):
        return self._element

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = str(self._element)
        return output


class Edge:
    """Class to implement Edge ADT

       Attributes:
       self._label : name of the edge
       self._vertices : a set containing the vertices of the edge

       Methods:
       __init__ : constructor method to initialise the class
       vertices : returns the set of vertices
       opposite : if the edge is incident on parameter item, returns the other vertex
       element : returns the label of the edge
    """
    def __init__(self, a, b, label):
        self._label = label
        self._vertices = (a, b)

    def vertices(self):
        return self._vertices

    def opposite(self, item):
        if item == self._vertices[0]:
            return self._vertices[1]
        elif item == self._vertices[1]:
            return self._vertices[0]
        else:
            return None

    def element(self):
        return self._label

    def getFirstElement(self):
        return self._vertices[0]

    def getSecondElement(self):
        return self._vertices[1]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = ('(' + str(self._vertices[0]) + '--'
                  + str(self._vertices[1]) + ' : '
                  + str(self._label) + ')')
        return output


class Graph:
    """Class to represent undirected Graph ADT
    """
    def __init__(self):
        self._vertices = dict()

    #Query methods -----------------------------------------

    def vertices(self):
        #Return a list of all vertices
        output = []
        for v in self._vertices:
            output += [v]
        return output

    def edges(self):
        #Return a list of all edges
        output = []
        for v in self._vertices:
            for e in self._vertices[v]:
                if self._vertices[v][e] not in output:
                    output += [self._vertices[v][e]]
        return output

    def num_vertices(self):
        #Return the number of vertices
        return len(self._vertices)

    def num_edges(self):
        #Return the number of edges
          return len(self.e1dges())

    def get_vertex_by_label(self, x):
        #Return the vertex with elt x
        for v in self._vertices:
            if v.element() == x:
                return v
        return None

    def get_edge(x, y):
        #Return the edge from x to y
        if y in self._vertices[x]:
            return self._vertices[x][y]
        return None

    def degree(self, x):
        #Return the degree of vertex x
        if x in self._vertices:
            return len(self._vertices[x])
        return None

    def in_degree(self, x):
        #Return the in-degree of vertex x
        in_degree = 0
        if x in self._vertices:
            edges = self._vertices[x]
            for e in edges:
                if edges[e].getSecondElement() == x:
                    in_degree += 1
        return in_degree

    def out_degree(self, x):
        #Return the out-degree of vertex x
        out_degree = 0
        if x in self._vertices:
            edges = self._vertices[x]
            for e in edges:
                if edges[e].getFirstElement() == x:
                    out_degree += 1
        return out_degree

    def get_edges(self, x):
        #Return a list of all edges incident on x
        output = []
        if x in self._vertices:
            for opp in self._vertices[x]:
                output += [self._vertices[x][opp]]
        return output

    def get_in_edges(self, x):
        #Return a list of all in edges of x
        output = []
        if x in self._vertices:
            edges = self._vertices[x]
            for e in edges:
                if edges[e].getSecondElement() == x:
                    output += [edges[e]]
        return output

    def get_out_edges(self, x):
        #Return a list of all out edges of x
        output = []
        if x in self._vertices:
            edges = self._vertices[x]
            for e in edges:
                if edges[e].getFirstElement() == x:
                    output += [edges[e]]
        return output

    def highest_degree(self):
        highest = (None, 0)
        for v in self._vertices:
            if self.degree(v) > highest[1]:
                highest = (v, self.degree(v))
        return print(highest[0])

    #Methods to add to graph -------------------------------

    def add_vertex(self, elt):
        #Add a new vertex with element elt
        v = Vertex(elt)
        if v not in self._vertices:
            self._vertices[v] = dict()

    def add_edge(self, x, y, elt):
        #Add a new edge between x and y, with element elt
        e = Edge(x, y, elt)
        if x in self._vertices and y in self._vertices:
            self._vertices[x][y] = e
            self._vertices[y][x] = e

    def remove_vertex(self, x):
        #Remove vertex and all incident edges
        if x in self._vertices:
            for opp in self._vertices[x]:
                del self._vertices[opp][x]
            del x

    def remove_edge(self, e):
        #Remove edge e
        a = e.getFirstElement()
        b = e.getSecondElement()
        if a in self._vertices:
            del self._vertices[a][b]
        if b in self._vertices:
            del self._vertices[b][a]

    #Search Methods ----------------------------------------

    def depthfirstsearch(self, v):
        #Move through the graph starting from vertex v, moving to a new vertex each
        #time, until no new vertices can be reached. Then back-track and try a different
        #route. Repeat until all vertices have been reached
        marked = {v:None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        #Helper method for depthfirstsearch
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)

    def breadthfirstsearch(self, v):
        marked = {v:None}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = e
                        nextlevel.append(x)
            level = nextlevel
        return marked

    #Directed graph methods --------------------------------

    def topological_sort(self):
        inedgecount = {}
        tsort = []
        available = []
        for v in self._vertices:
            v_incount = self.in_degree(v)
            inedgecount[v] = v_incount
            if v_incount == 0:
                available.append(v)
        while len(available) > 0:
            w = available.pop()
            tsort.append(w)
            for e in self.get_edges(w):
                u = e.opposite(w)
                inedgecount[u] -= 1
                if inedgecount[u] == 0:
                    available.append(u)
        return tsort

    def is_dag(self):
        t = self.topological_sort()
        if len(t) > 0:
            return True
        return False

    #Dijkstra's Algorithm ----------------------------------

    def dijkstra(self, vertex):
        """Computes the shortest paths from vertex to all other reachable
        vertices in the graph"""

        #Initialise our APQ and three dictionaries
        opened = APQ()
        locations = dict()
        closed = dict()
        preds = dict()
        #There is no predecessor to the first vertex
        preds[vertex] = None
        locations[vertex] = opened.add(0, vertex)
        
        while opened._length > 0:
            v = opened.remove_min()
            locations.pop(v._value)
            predecessor = preds.pop(v._value)
            closed[v._value] = (v._key, predecessor)
            for edge in self.get_edges(v._value):
                w = edge.opposite(v._value)
                if w not in closed:
                    newcost = v._key + int(edge.element())
                    if w not in locations:
                        preds[w] = v._value
                        locations[w] = opened.add(newcost, w)
                    elif newcost < locations[w]._key:
                        preds[w] = v._value
                        opened.update_key(locations[w], newcost)
        return closed

            
            

    #String Method -----------------------------------------

    def __str__(self):
        output = """Vertices: """
        for v in self.vertices():
            output += v.__str__()
            output += ", "
        output += "\n"
        output += "Edges: "
        for e in self.edges():
            output += e.__str__()
            output += ", "
        return output


#Test Methods---------------------------------------------

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def graphreader2(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        gps = file.readline().split()
        gps_lat, gps_long = float(gps[1]), float(gps[2])
        vertex = graph.add_vertex(nodeid, gps_lat, gps_long)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        file.readline()
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def runDijkstras(filename, vertex):
    #Runs dijkstra's algorithm on the graph created from information in file
    #filename, computing the shortest path to each vertex in the graph starting
    #from vertex
    graph = graphreader(filename)
    v = graph.get_vertex_by_label(vertex)
    result = graph.dijkstra(v)
    print('Vertex   Cost   Predecessor')
    for vert in result:
        print('%5s : %5s : %5s' % (vert, result[vert][0], result[vert][1]))


#--------------------------------------------------------------------------------
#- Part II of assignment --------------------------------------------------------
#- Routemap Class ---------------------------------------------------------------
#--------------------------------------------------------------------------------

class RouteMap:

    def __init__(self):
        self._vertices = dict()
        self._vertex_coords = dict()
        self._vertex_references = dict()
        self._num_edges = 0

    def __str__(self):
        output = """"""
        if self.num_vertices() < 100:
            output = """Vertices: """
            for v in self.vertices():
                output += v.__str__()
                output += ", "
            output += "\n"
        if self.num_edges() < 100:
            output += "Edges: "
            for e in self.edges():
                output += e.__str__()
                output += ", "
        return output

    #Query methods -----------------------------------------

    def vertices(self):
        #Return a list of all vertices
        output = []
        for v in self._vertices:
            output += [v]
        return output

    def edges(self):
        #Return a list of all edges
        output = []
        for v in self._vertices:
            for e in self._vertices[v]:
                if self._vertices[v][e] not in output:
                    output += [self._vertices[v][e]]
        return output

    def num_vertices(self):
        #Return the number of vertices
        return len(self._vertices)

    def num_edges(self):
        #Return the number of edges
          return self._num_edges

    def get_vertex_by_label(self, x):
        #Return the vertex with elt x
        if x in self._vertex_references:
            return self._vertex_references[x]
        return None

    def get_edge(x, y):
        #Return the edge from x to y
        if y in self._vertices[x]:
            return self._vertices[x][y]
        return None

    def get_edges(self, x):
        #Return a list of all edges incident on x
        output = []
        if x in self._vertices:
            for opp in self._vertices[x]:
                output += [self._vertices[x][opp]]
        return output

    def degree(self, x):
        #Return the degree of vertex x
        if x in self._vertices:
            return len(self._vertices[x])
        return None

    def get_coords(self, v):
        #Return the co-ordinates of vertex v
        if v in self._vertex_coords:
            return self._vertex_coords[v]
        return None

    #Methods to add to graph -------------------------------

    def add_vertex(self, elt, lat, long):
        #Add a new vertex with element elt
        if elt not in self._vertex_references:
            v = Vertex(elt)
            self._vertices[v] = dict()
            self._vertex_references[elt] = v
            self._vertex_coords[v] = (lat, long)

    def add_edge(self, x, y, elt):
        #Add a new edge between x and y, with element elt
        e = Edge(x, y, elt)
        if x in self._vertices and y in self._vertices:
            self._vertices[x][y] = e
            self._vertices[y][x] = e
            self._num_edges += 1

    def remove_vertex(self, x):
        #Remove vertex and all incident edges
        if x in self._vertices:
            for opp in self._vertices[x]:
                del self._vertices[opp][x]
            del x

    def remove_edge(self, e):
        #Remove edge e
        a = e.getFirstElement()
        b = e.getSecondElement()
        if a in self._vertices:
            del self._vertices[a][b]
        if b in self._vertices:
            del self._vertices[b][a]
        self._num_edges -= 1

    #Dijkstra's Algorithm ----------------------------------

    def dijkstra(self, vertex):
        """Computes the shortest paths from vertex to all other reachable
        vertices in the graph"""

        #Initialise our APQ and three dictionaries
        opened = APQ()
        locations = dict()
        closed = dict()
        preds = dict()
        #There is no predecessor to the first vertex
        preds[vertex] = None
        locations[vertex] = opened.add(0, vertex)
        
        while opened._length > 0:
            v = opened.remove_min()
            locations.pop(v._value)
            predecessor = preds.pop(v._value)
            closed[v._value] = (v._key, predecessor)
            for edge in self.get_edges(v._value):
                w = edge.opposite(v._value)
                if w not in closed:
                    newcost = v._key + int(edge.element())
                    if w not in locations:
                        preds[w] = v._value
                        locations[w] = opened.add(newcost, w)
                    elif newcost < locations[w]._key:
                        preds[w] = v._value
                        opened.update_key(locations[w], newcost)
        return closed

    def sp(self, v, w):
        #Will calculate the shortest path from v to w by calling the Dijkstra
        #method
        shortest_paths = self.dijkstra(v)
        route = []
        prev_cost = shortest_paths[w][0]
        vertex = w
        while vertex != v:
            data = shortest_paths[vertex]
            cost = data[0]
            route += [(vertex, (prev_cost-cost))]
            prev_cost = cost
            vertex = data[1]
        return route[::-1]

    def printvlist(self, lst):
        print("type,latitude,longitude,element,cost")
        for pair in lst:
            gps = self.get_coords(pair[0])
            print("w,%.6f,%.6f,%10i,%3i" % (gps[0], gps[1], pair[0].element(), pair[1]))
            

def routeTest():
    #Test routine for routemap class
    routemap = graphreader2('corkCityData.txt')
    ids = {}
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'wgb'
    deststr = 'neptune'
    source = routemap.get_vertex_by_label(ids[sourcestr])
    dest = routemap.get_vertex_by_label(ids[deststr])
    tree = routemap.sp(source, dest)
    routemap.printvlist(tree)
