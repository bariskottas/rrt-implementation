import tkinter as tk

from math import atan2
from math import cos
from math import degrees
from math import dist
from math import pi
from math import sin
from math import sqrt

from random import randint

class Node:
    x:int
    y:int
    cost:int
    heading:float

    id:int
    parent:int
    children:list

    canvasNode: int
    canvasItem: list

    def __init__(self, x, y, id = 0, parent = -1):    
        self.x = x
        self.y = y
        self.cost = 0
        self.heading = 0

        self.id = id
        self.parent = parent
        self.children = []

        self.canvasNode = -1
        self.canvasItem = []
    
class Edge:
    node1:Node
    node2:Node

    start:float
    extent:float

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

class Shape:
    edges:list

    def __init__(self, edges):
        self.edges = edges

    def intersects(self, edge):
        t = 2 * thetaL(edge.node1, edge.node2)
        if abs(t) < 1e-4:
            for shapeEdge in self.edges:
                denom = (shapeEdge.node2.y - shapeEdge.node1.y) * (edge.node2.x - edge.node1.x) - (shapeEdge.node2.x - shapeEdge.node1.x) * (edge.node2.y - edge.node1.y)
                if denom == 0:
                    continue

                ua = ((shapeEdge.node2.x - shapeEdge.node1.x) * (edge.node1.y - shapeEdge.node1.y) - (shapeEdge.node2.y - shapeEdge.node1.y) * (edge.node1.x - shapeEdge.node1.x)) / denom
                if ua < 0 or ua > 1:
                    continue

                ub = ((edge.node2.x - edge.node1.x) * (edge.node1.y - shapeEdge.node1.y) - (edge.node2.y - edge.node1.y) * (edge.node1.x - shapeEdge.node1.x)) / denom
                if ub < 0 or ub > 1:
                    continue

                return True
        else:
            center = findCenter(edge.node1, edge.node2)
            r = rxy(edge.node1, edge.node2)

            sa = atan2(edge.node1.y - center.y, edge.node1.x - center.x)
            if sa < 0:
                sa += 2 * pi

            extent = 2 * thetaL(edge.node1, edge.node2)
            ea = sa + extent

            for shapeEdge in self.edges:
                dx = shapeEdge.node2.x - shapeEdge.node1.x
                dy = shapeEdge.node2.y - shapeEdge.node1.y

                aDet = dx * dx + dy * dy
                bDet = 2 * (dx * (shapeEdge.node1.x - center.x) + dy * (shapeEdge.node1.y - center.y))
                cDet = (shapeEdge.node1.x - center.x) * (shapeEdge.node1.x - center.x) + (shapeEdge.node1.y - center.y) * (shapeEdge.node1.y - center.y) - r * r

                if shapeEdge.node1.x > shapeEdge.node2.x:
                    gx = shapeEdge.node1.x
                    sx = shapeEdge.node2.x
                else:
                    gx = shapeEdge.node2.x
                    sx = shapeEdge.node1.x

                if shapeEdge.node1.y > shapeEdge.node2.y:
                    gy = shapeEdge.node1.y
                    sy = shapeEdge.node2.y
                else:
                    gy = shapeEdge.node2.y
                    sy = shapeEdge.node1.y

                det = bDet ** 2 - 4 * aDet * cDet
                
                if aDet <= 0.0000001 or det < 0:
                    continue

                elif det == 0:
                    t = -bDet / (2 * aDet)
                    if 0 <= t <= 1:
                        intersection1 = Node(shapeEdge.node1.x + t * dx, shapeEdge.node1.y + t * dy)
                        if sx <= intersection1.x <= gx and sy <= intersection1.y <= gy:          
                            i1Extent = 2 * thetaL(edge.node1, intersection1)
                            ai1 = sa + i1Extent

                            if extent > 0:
                                if sa <= ai1 <= ea:
                                    return True
                            else:
                                if ea <= ai1 <= sa:
                                    return True
       
                else:
                    t = (-bDet + sqrt(det)) / (2 * aDet)
                    if 0 <= t <= 1:
                        intersection1 = Node(shapeEdge.node1.x + t * dx, shapeEdge.node1.y + t * dy)
                        if sx <= intersection1.x <= gx and sy <= intersection1.y <= gy:
                            i1Extent = 2 * thetaL(edge.node1, intersection1)
                            ai1 = sa + i1Extent
                                                        
                            if extent > 0:
                                if sa <= ai1 <= ea:
                                    return True
                            else:
                                if ea <= ai1 <= sa:
                                    return True

                    t = (-bDet - sqrt(det)) / (2 * aDet)
                    if 0 <= t <= 1:
                        intersection2 = Node(shapeEdge.node1.x + t * dx, shapeEdge.node1.y + t * dy)
                        if sx <= intersection2.x <= gx and sy <= intersection2.y <= gy:
                            i2Extent = 2 * thetaL(edge.node1, intersection2)
                            ai2 = sa + i2Extent
                                                        
                            if extent > 0:
                                if sa <= ai2 <= ea:
                                    return True
                            else:
                                if ea <= ai2 <= sa:
                                    return True
   
        return False
    
def drawCircle(canvas, x, y, color):
    a = canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline = color, fill = color, width = 0)
    canvas.pack()
    return a

def createMap(canvas, nodes):
    #create starting node
    nodes.append(Node(50, 50, len(nodes)))
    nodes[0].canvasNode = drawCircle(canvas, 50, 50, "black")

    #create goal
    canvas.create_rectangle(900, 900, 900 + 50, 900 + 50, outline = "green", fill = "green", width = 0)

    canvas.pack()

def createObstacle(obstacles, newObstacles):
    x = randint(0, 950)
    y = randint(0, 950)
    snode1 = Node(x, y)
    snode2 = Node(x + 50, y)
    snode3 = Node(x, y + 50)
    snode4 = Node(x + 50, y + 50)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    newObstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(x, y, x + 50, y + 50, outline = "blue", fill = "blue", width = 0)

def handleCollisions(nodes, newObstacles):
    for i in range(len(nodes)):
        if nodes[i] == None:
            continue 
        
        if len(nodes[i].children) == 0:
            continue
        
        for j in range(len(nodes[i].children)):
            edge = Edge(nodes[i], nodes[nodes[i].children[j]])

            intersectionExists = False
            for obstacle in newObstacles:
                if obstacle.intersects(edge):
                    intersectionExists = True
                    break

            if intersectionExists:
                traverseAndReconstruct(nodes, nodes[nodes[i].children[j]])

                del nodes[i].children[j]
                del nodes[i].canvasItem[j]

    newObstacles = []

def traverseAndReconstruct(nodes, node):
    for child in node.children:
        traverseAndReconstruct(nodes, nodes[child])
    
    canvas.delete(nodes[node.id].canvasNode)

    for x in nodes[node.id].canvasItem:
        canvas.delete(x)

    nodes[node.id] = None

def inGoal(node):
    if 900 <= node.x and node.x <= 950 and 900 <= node.y and node.y <= 950:
        return True

    return False

def distance(node1, node2):
    return dist((node1.x, node1.y), (node2.x, node2.y))

def findClosestNode(nodes, node):
    closestDist = float('inf')
    closestNode = node

    for possibleNode in nodes:
        if possibleNode == None:
            continue

        dist = distance(possibleNode, node)
        if dist <= closestDist:
            closestDist = dist
            closestNode = possibleNode

    if closestNode == node:
        return None

    return closestNode

def replaceWithCloserNode(node, closestNode):
    dist = distance(closestNode, node)

    if dist <= 50:
        return node
    
    ratio = 50 / dist

    return Node((1 - ratio) * closestNode.x + ratio * node.x, (1 - ratio) * closestNode.y + ratio * node.y, node.id)

def replaceWithProximalNode(node, closestNode, nodes):
    proximalNode = closestNode
    for possibleProximalNode in nodes:
        if possibleProximalNode == None:
            continue

        if possibleProximalNode.cost < proximalNode.cost and distance(possibleProximalNode, node) <= 125:
            proximalNode = possibleProximalNode
    
    return proximalNode

def thetaL(node1, node2):
    return atan2(node2.y - node1.y, node2.x - node1.x) - node1.heading

def rxy(node1, node2):
    tmp = 2 * sin(thetaL(node1, node2))
    if tmp == 0:
        return float('inf') 
    
    return abs(distance(node1, node2) / tmp)

def L(node1, node2):
    tL = thetaL(node1, node2)

    tmp =  sin(tL)
    if tmp == 0:
        return float('inf') 

    return abs(distance(node1, node2) * tL / tmp)

def steer(node1, node2):
    if rxy(node1, node2) < 40:
        return False

    if L(node1, node2) > pi * rxy(node1, node2):
        return False

    return True

def findCenter(node1, node2):
    r = rxy(node1, node2)
    d = distance(node1, node2)
    
    center = Node(0, 0)

    if thetaL(node1, node2) >= 0:
        center.x = (node1.x + node2.x) / 2 + sqrt(r ** 2 - (d / 2) ** 2) * ((node1.y - node2.y) / d) 
        center.y = (node1.y + node2.y) / 2 + sqrt(r ** 2 - (d / 2) ** 2) * ((node2.x - node1.x) / d)
    else:        
        center.x = (node1.x + node2.x) / 2 - sqrt(r ** 2 - (d / 2) ** 2) * ((node1.y - node2.y) / d) 
        center.y = (node1.y + node2.y) / 2 - sqrt(r ** 2 - (d / 2) ** 2) * ((node2.x - node1.x) / d)

    return center

def drawArc(canvas, node1, node2, outline = "black", width = 1):
    t = 2 * thetaL(node1, node2)
    if abs(t) < 1e-4:
        canvasItem = canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill = outline, width = width)
        canvas.pack()
        return canvasItem

    center = findCenter(node1, node2)
    r = rxy(node1, node2)
    start = -degrees(atan2(node2.y - center.y, node2.x - center.x))
    extent = degrees(t)

    canvasItem = canvas.create_arc(center.x - r, center.y - r, center.x + r, center.y + r, start = start, extent = extent, outline = outline, width = width, style = tk.ARC)
    canvas.pack()
    return canvasItem

root = tk.Tk()

root.title("RRT* Implementation")

windowSize = 1000

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

centerX = int(screenWidth / 2 - windowSize / 2)
centerY = int(screenHeight / 2 - windowSize / 2)

root.geometry(f'{windowSize}x{windowSize}+{centerX}+{centerY}')
root.resizable(False, False)

canvas = tk.Canvas(root, width = windowSize, height = windowSize)

nodes = []
obstacles = []
newObstacles = []

createMap(canvas, nodes)

pathNotFound = True
while True:
    root.winfo_exists()
    root.update()

    if pathNotFound:
        node = Node(randint(0, windowSize), randint(0, windowSize), len(nodes))
        closestNode = findClosestNode(nodes, node)
        node = replaceWithCloserNode(node, closestNode)

        closestNode = replaceWithProximalNode(node, closestNode, nodes)
        edge = Edge(node1=closestNode, node2=node)

        node.cost = closestNode.cost + L(closestNode, node)

        node.heading = closestNode.heading + 2 * thetaL(closestNode, node)
        if node.heading > pi:
            node.heading -= pi

        if node.heading < -pi:
            node.heading += pi

        node.parent = closestNode.id

        intersectionExists = False
        for obstacle in obstacles:
            if type(obstacle) == Shape and obstacle.intersects(edge):
                intersectionExists = True
                break

        if intersectionExists:
            continue

        steerResult = steer(closestNode, node)
        if not steerResult:   
            continue
        
        nodes[node.parent].children.append(node.id)

        nodes.append(node)

        node.canvasNode = drawCircle(canvas, node.x, node.y, "red")
        nodes[node.parent].canvasItem.append(drawArc(canvas, closestNode, node))

        if len(nodes) % 15 == 0 and len(obstacles) < 25:
            createObstacle(obstacles, newObstacles)
            handleCollisions(nodes, newObstacles)

        if inGoal(node):
            pathNotFound = False

            currentNode = node.id
            while currentNode != 0:        
                drawArc(canvas, nodes[nodes[currentNode].parent], nodes[currentNode], "darkgoldenrod1", 3)
                currentNode = nodes[currentNode].parent
