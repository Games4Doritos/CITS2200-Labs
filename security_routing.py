# Name: Evan Miocevich
# Student Number: 24147733

from enum import IntEnum


class Clearance(IntEnum):
    NONE = 0
    RED = 1
    BLUE = 2
    GREEN = 3


def security_route(stations, segments, source, target):
    """Finds the fastest route from source station to target station.

    You start with no security clearance.
    When at a security station, you may choose to set your clearance to the same
    as that of the station.
    Each segment gives how long it takes to get from one station to another, and
    what clearance is required to be able to take that segment.

    Target Complexity: O(N lg N) in the size of the input (stations + segments).

    Args:
        stations: A list of what clearance is available at each station, or
            `NONE` if that station can not grant any clearance.
        segments: A list of `(u, v, t, c)` tuples, each representing a segment
            from `stations[u]` to `stations[v]` taking time `t` and requiring
            clearance `c` (`c` may be `NONE` if no clearance is required).
        source: The index of the station from which we start.
        target: The index of the station we are trying to reach.

    Returns:
        The minimum length of time required to get from `source` to `target`, or
        `None` if no route exists.
    """
    vertices = {}
    edges = {}
    class edge:
        def __init__(self, v1,v2,time, c):
            self.time = time
            self.c = c
            self.left = v1
            self.right = v2
            vertices[v1].adjacent[v2] = (time, c)
        
    class vertex:
        def __init__(self, v):
            self.num = v
            self.adjacent = {}
            vertices[v] = self

    class clearanceTree:
        class node:
            def __init__(self, c, parent, v):
                self.c = parent.c
                self.v = v
                self.parent = parent
                if stations[v] > self.c:
                    self.c = stations[v]
                self.children = []
        def __init__(self, root):
            self.root = root
        def add(self, c,parent,v):
            self
        def clearance(self):
            pass
    class heap:
        class node:
            def __init__(self, v, key):
                self.key = key
                self.v = v
                
        def __init__(self):
            self.nodes = []
            self.locator = {}
        def upheap(self, v):
            ind = v.ind
            if (v.ind-1)//2 >=0:
                if v.key < self.nodes[(v.ind-1)//2].key:
                    temp = self.nodes[(v.ind-1)//2]
                    self.locator[temp.v] = v.ind
                    temp.ind = v.ind
                    self.nodes[v.ind] = temp
                    v.ind = (v.ind-1)//2
                    self.nodes[v.ind] = v
                    ind = v.ind
                    self.locator[v.v] = v.ind
                    ind = self.upheap(self.nodes[v.ind])
            return ind
        def add(self, v, key):
            node = self.node(v, key)
            node.ind = len(self.nodes)
            self.nodes.append(node)
            self.locator[v] = len(self.nodes)-1
            return self.upheap(node)
        def downheap(self,v):
            if 2*v.ind + 2 <= len(self.nodes) -1:
                minKey = min(self.nodes[2*v.ind+1].key,self.nodes[2*v.ind+2].key)
                if minKey == self.nodes[2*v.ind+1].key:
                    minInd = 2*v.ind+1
                else: 
                    minInd = 2*v.ind + 2
                if v.key >= minKey:
                    temp = v
                    self.nodes[v.ind] = self.nodes[minInd]
                    self.locator[self.nodes[minInd].v] = v.ind
                    temp.ind = minInd
                    self.nodes[temp.ind] = temp
                    self.downheap(v)      
                    self.locator[v.v] = temp.ind
            elif len(self.nodes) == 2:
                if self.nodes[0].key >= self.nodes[1].key:
                    temp = self.nodes[1]
                    self.nodes[1] = self.nodes[0]
                    self.nodes[0] = temp
                    self.nodes[0].ind = 0
                    self.nodes[1].ind = 1
                    self.locator[self.nodes[0].v] = 0
                    self.locator[self.nodes[1].v] = 1
                else:
                    self.nodes[0].ind = 0
                    self.nodes[1].ind = 1
                    self.locator[self.nodes[0].v] = 0
                    self.locator[self.nodes[1].v] = 1
            
        def removeMin(self):
            temp = self.nodes[0]
            self.nodes[0] = self.nodes[-1]
            self.nodes[0].ind = 0
            self.nodes.pop(-1)
            if len(self.nodes) > 1:
                self.downheap(self.nodes[0])
            return temp
        def updateD(self, v, d):
            if len(self.nodes) == 2:
                if self.nodes[0].v == v:
                    self.nodes[0].key = d
                else:
                    self.nodes[1].key = d
                if self.nodes[0].key >= self.nodes[1].key:
                    temp = self.nodes[1]
                    self.nodes[1] = self.nodes[0]
                    self.nodes[0] = temp
                    self.nodes[0].ind = 0
                    self.nodes[1].ind = 1
                    self.locator[self.nodes[0].v] = 0
                    self.locator[self.nodes[1].v] = 1
            else:
                self.nodes[self.locator[v]].key = d
                self.downheap(self.nodes[self.locator[v]])
                self.upheap(self.nodes[self.locator[v]])
    
    for i in range(len(stations)):
        vertex(i)
    for i in segments:
        edge(i[0], i[1], i[2], i[3])
    
    def dijkstra():
        d = {}
        cloud = {}
        pq = heap()
        maxClearance = []
        for i in stations:
            maxClearance.append(Clearance.NONE)
        
        for v in vertices:
            if v == source:
                d[vertices[v]] = 0
            else:
                d[vertices[v]] = float('inf')
            pq.add(vertices[v], d[vertices[v]])
        
        while len(pq.nodes) != 0: 
            min = pq.removeMin()
            cloud[min.v.num] = min.key
            pq.locator.pop(min.v)
            u = min.v
            if stations[u.num] >= maxClearance[u.num]:
                maxClearance[u.num] = stations[u.num]
            max = Clearance.NONE
            for v in cloud:
                if stations[v] > max:
                    max = stations[v]
            maxClearance[u.num] = max
            for v in u.adjacent:
                e = u.adjacent[v]
                if v not in cloud:
                    if maxClearance[u.num] >= e[1] or e[1] == Clearance.NONE:
                        wgt = e[0]
                        if d[u] + wgt < d[vertices[v]]:
                            d[vertices[v]] = d[u] + wgt
                            pq.updateD(vertices[v], d[vertices[v]])
                        
        if cloud[target] == float('inf'):
            return None
        else:
            return cloud[target]
    
    return dijkstra() 
