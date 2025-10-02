# Name: Evan Miocevich
# Student Number: 24147733


def trains_planes(trains, planes):
    """Find what flights can be replaced with a rail journey.

    Initially, there are no rail connections between cities. As rail connections
    become available, we are interested in knowing what flights can be replaced
    by a rail journey, no matter how indirect the route. All rail connections
    are bidirectional.

    Target Complexity: O(N lg N) in the size of the input (trains + planes).

    Args:
        trains: A list of `(date, lcity, rcity)` tuples specifying that a rail
            connection between `lcity` and `rcity` became available on `date`.
        planes: A list of `(code, date, depart, arrive)` tuples specifying that
            there is a flight scheduled from `depart` to `arrive` on `date` with
            flight number `code`.

    Returns:
        A list of flights that could be replaced by a train journey.
    """   
    class sets:
        class child:
            def __init__(self, v):
                self.data = v
                self.parent = v   
        def __init__(self):
            self.objs = {}
        def makeSet(self, v):
            if self.objs.get(v, True) == True:
                self.objs[v] = self.child(v)     
        def find(self, v):
            try:
                if self.objs[v].parent != v:
                    return self.find(self.objs[v].parent)
                else:
                    return v 
            except KeyError:
                return None   
        def union(self, a, b):
            self.objs[self.find(b)].parent = self.find(a)
           
    def merge(arr1, arr2, arr, ind):
        n = len(arr)
        i, j = 0, 0
        while i + j < n:
            if i == len(arr1):
                arr[i+j] = arr2[j]
                j += 1
            elif j == len(arr2)or arr1[i][ind] < arr2[j][ind]:
                arr[i+j] = arr1[i]
                i += 1
            else:
                arr[i+j] = arr2[j]
                j += 1
     
    def mergeSort(arr, ind):
        n = len(arr)
        if n < 2:
            return arr        
        arr1 = arr[0:n//2]
        arr2 = arr[n//2:]
        mergeSort(arr1, ind)
        mergeSort(arr2, ind)
        merge(arr1, arr2, arr, ind)
        return arr
    
    flights = []    
    mergeSort(trains, 0)
    mergeSort(planes, 1)
    i, j = 0,0
    trainSets = sets()
    while i < len(planes):
        if j == len(trains):
            if trainSets.find(planes[i][2]) == trainSets.find(planes[i][3]) and trainSets.find(planes[i][2]) != None:
                flights.append(planes[i])
            i += 1
        elif trains[j][0] <= planes[i][1]:
            trainSets.makeSet(trains[j][1])
            trainSets.makeSet(trains[j][2])
            trainSets.union(trains[j][1], trains[j][2])
            j+= 1
        else:
            if trainSets.find(planes[i][2]) == trainSets.find(planes[i][3]) and trainSets.find(planes[i][2]) != None:
                flights.append(planes[i])
            i += 1
    return flights
               
    
