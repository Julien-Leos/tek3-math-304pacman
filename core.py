import operator
import copy

adjacentCoordsOffset = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def addTuples(tup1, tup2):
    return tuple(map(operator.add, tup1, tup2))

class Core:
    map = []
    mapLength = 0
    mapHeight = 0
    c1 = ''
    c2 = ''

    visited = []
    unvisited = []

    ghostPosition = ()
    pacmanPosition = ()

    vertex = {
        "position": (),
        "shortDist": 1000000,
        "prevVertex": None
    }

    pacmanFound = False
    dijkstra = []
    dijkstraMap = []

    def __init__(self, map, c1, c2):
        self.map = map
        self.mapLength = len(self.map[0])
        self.mapHeight = len(self.map)
        self.c1 = c1
        self.c2 = c2
        self.initDijkstra()
        self.initGhostVertex()

    def initDijkstra(self):
        self.dijkstraMap = [[0] * self.mapLength for i in range(self.mapHeight)]
        for (yIdx, y) in enumerate(self.map):
            for (xIdx, x) in enumerate(y):
                if x == '1':
                    self.dijkstraMap[yIdx][xIdx] = self.c1
                elif x == '0':
                    self.dijkstraMap[yIdx][xIdx] = self.c2
                elif x == 'F':
                    self.dijkstraMap[yIdx][xIdx] = 'F'
                    self.ghostPosition = (xIdx, yIdx)
                elif x == 'P':
                    self.dijkstraMap[yIdx][xIdx] = 'P'
                    self.pacmanPosition = (xIdx, yIdx)

    def createNewVertex(self, pos):
        self.dijkstra.append(copy.deepcopy(self.vertex))
        self.dijkstra[-1]["position"] = pos
        self.unvisited.append(self.dijkstra[-1])
        return self.dijkstra[-1]

    def initGhostVertex(self):
        ghostVertex = self.createNewVertex(self.ghostPosition)
        ghostVertex["shortDist"] = 0

    def removeVertexFromUnvisited(self, vertexToRemove):
        for vertex in self.unvisited:
            if vertex == vertexToRemove:
                self.unvisited.remove(vertex)

    def findVertexByPos(self, vertexPos):
        for vertex in self.dijkstra:
            if vertex["position"] == vertexPos:
                return vertex
        return None

    def findSmallestDistFromUnvisited(self):
        min = 1000000
        minVertex = None

        for vertex in self.unvisited:
            if vertex["shortDist"] < min:
                min = vertex["shortDist"]
                minVertex = vertex
        return minVertex

    def dijkstraLoop(self):
        while self.pacmanFound == False and self.browseAdjacentCoords() == True:
            pass

    def browseAdjacentCoords(self):
        actualVertex = self.findSmallestDistFromUnvisited()
        if actualVertex == None:
            return False
        for adjacentCoordOffset in adjacentCoordsOffset:
            newAdjacentCoord = addTuples(actualVertex["position"], adjacentCoordOffset)
            if newAdjacentCoord[0] < 0 or newAdjacentCoord[1] < 0 or \
            newAdjacentCoord[0] >= self.mapLength or newAdjacentCoord[1] >= self.mapHeight:
                continue
            if self.map[newAdjacentCoord[1]][newAdjacentCoord[0]] == '1':
                continue
            if newAdjacentCoord == self.pacmanPosition:
                self.pacmanFound = True
                return
            adjacentVertex = self.findVertexByPos(newAdjacentCoord)
            if adjacentVertex == None:
                adjacentVertex = self.createNewVertex(newAdjacentCoord)
            if actualVertex["shortDist"] + 1 < adjacentVertex["shortDist"]:
                adjacentVertex["shortDist"] = actualVertex["shortDist"] + 1
                adjacentVertex["prevVertex"] = actualVertex
                self.dijkstraMap[adjacentVertex["position"][1]][adjacentVertex["position"][0]] = adjacentVertex["shortDist"] % 10
        self.removeVertexFromUnvisited(actualVertex)
        self.visited.append(actualVertex)
        return True

    def displayMap(self):
        for y in self.dijkstraMap:
            for x in y:
                print(x, end='')
            print('')