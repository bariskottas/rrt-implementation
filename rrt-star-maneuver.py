import tkinter as tk

from math import atan2
from math import cos
from math import sqrt
from math import sin

from random import randint

def dot(v,w):
    x,y,z = v
    X,Y,Z = w
    return x*X + y*Y + z*Z

def length(v):
    x,y,z = v
    return sqrt(x*x + y*y + z*z)

def vector(b,e):
    x,y,z = b
    X,Y,Z = e
    return (X-x, Y-y, Z-z)

def unit(v):
    x,y,z = v
    mag = length(v)
    return (x/mag, y/mag, z/mag)

def distance2(p0,p1):
    return length(vector(p0,p1))

def scale(v,sc):
    x,y,z = v
    return (x * sc, y * sc, z * sc)

def add(v,w):
    x,y,z = v
    X,Y,Z = w
    return (x+X, y+Y, z+Z)

def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)    
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    nearest = scale(line_vec, t)
    dist = distance2(nearest, pnt_vec)
    nearest = add(nearest, start)
    return (dist, nearest)

class Node:
    x:int
    y:int
    cost:int
    heading:float

    id:int
    parent:int

    def __init__(self, x, y, id = 0, parent = -1):    
        self.x = x
        self.y = y
        self.cost = 0
        self.heading = 0

        self.id = id
        self.parent = parent

class Edge:
    node1:Node
    node2:Node

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

class Shape:
    edges:list

    def __init__(self, edges):
        self.edges = edges
    
    def distanceTo(self, node):
        result = float('inf')

        for shapeEdge in self.edges:
            distanceToShapeEdge = pnt2line((node.x, node.y, 0), (shapeEdge.node1.x, shapeEdge.node1.y, 0), (shapeEdge.node2.x, shapeEdge.node2.y, 0))[0]
            if distanceToShapeEdge < result:
                result = distanceToShapeEdge

        return result
    
def drawCircle(canvas, x, y, color):
    a = canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline = color, fill = color, width = 0)
    canvas.pack()
    return a

def createMap(canvas, nodes, obstacles):
    #create starting node
    nodes.append(Node(50, 50, len(nodes)))
    drawCircle(canvas, 50, 50, "black")

    #create obstacles
    snode1 = Node(500, 400)
    snode2 = Node(325, 550)
    snode3 = Node(675, 550)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode3)]))
    canvas.create_polygon([snode1.x, snode1.y, snode2.x, snode2.y, snode3.x, snode3.y], outline = "blue", fill = "blue", width = 0)

    snode1 = Node(150, 150)
    snode2 = Node(400, 150)
    snode3 = Node(150, 400)
    snode4 = Node(400, 400)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(150, 150, 150 + 250, 150 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(600, 150)
    snode2 = Node(850, 150)
    snode3 = Node(600, 400)
    snode4 = Node(850, 400)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(600, 150, 600 + 250, 150 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(150, 600)
    snode2 = Node(400, 600)
    snode3 = Node(150, 850)
    snode4 = Node(400, 850)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(150, 600, 150 + 250, 600 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(600, 600)
    snode2 = Node(850, 600)
    snode3 = Node(600, 850)
    snode4 = Node(850, 850)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(600, 600, 600 + 250, 600 + 250, outline = "blue", fill = "blue", width = 0)

    #create goal
    canvas.create_rectangle(900, 900, 900 + 50, 900 + 50, outline = "green", fill = "green", width = 0)

    canvas.pack()

def inObs(node):
    if 150 <= node.x and node.x <= 400 and 150 <= node.y and node.y <= 400:
        return True
    
    if 600 <= node.x and node.x <= 850 and 150 <= node.y and node.y <= 400:
        return True

    if 150 <= node.x and node.x <= 400 and 600 <= node.y and node.y <= 850:
        return True

    if 600 <= node.x and node.x <= 850 and 600 <= node.y and node.y <= 850:
        return True

    return False

def inGoal(node):
    if 900 <= node.x and node.x <= 950 and 900 <= node.y and node.y <= 950:
        return True

    return False

def distance(node1, node2):
    return sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)

def findClosestNode(nodes, node):
    closestDist = float('inf')
    closestNode = node

    for possibleNode in nodes:
        dist = distance(possibleNode, node)
        if dist <= closestDist:
            closestDist = dist
            closestNode = possibleNode

    if closestNode == node:
        return None

    return closestNode

def replaceWithCloserNode(node, closestNode):
    dist = distance(closestNode, node)

    if dist <= 20:
        return node
    
    ratio = 20 / dist

    return Node((1 - ratio) * closestNode.x + ratio * node.x, (1 - ratio) * closestNode.y + ratio * node.y, node.id)

def replaceWithProximalNode(node, closestNode, nodes):
    proximalNode = closestNode
    for possibleProximalNode in nodes:
        if possibleProximalNode.cost < proximalNode.cost and distance(possibleProximalNode, node) <= 60:
            proximalNode = possibleProximalNode
    
    return proximalNode

def thetaL(node1, node2):
    return atan2(node2.y - node1.y, node2.x - node1.x) - node1.heading

def rxy(node1, node2):
    tmp = 2 * sin(abs(thetaL(node1, node2)))
    if tmp == 0:
        return float('inf') 
    
    return distance(node1, node2) / tmp

def L(node1, node2):
    tL = thetaL(node1, node2)

    tmp =  sin(tL)
    if tmp == 0:
        return float('inf') 

    return distance(node1, node2) * tL / tmp

def steer(node1, node2):
    if rxy(node1, node2) < 45:
        return False
    
    return True

def drawArc(canvas, node1, node2, fill = "black", width = 1):
    t = node2.heading
    d = rxy(node1, node2) - sqrt(rxy(node1, node2) ** 2 - (distance(node1, node2) / 2) ** 2)

    if node2.heading >= node1.heading:
        midX = (node1.x + node2.x)/2 + d * sin(t)
        midY = (node1.y + node2.y)/2 - d * cos(t)
    else:
        midX = (node1.x + node2.x)/2 - d * sin(t)
        midY = (node1.y + node2.y)/2 + d * cos(t)

    canvas.create_line((node1.x, node1.y), (midX, midY), (node2.x, node2.y), smooth = True, fill = fill, width = width)
    canvas.pack()

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

obstacles = []
nodes = []
createMap(canvas, nodes, obstacles)

pathNotFound = True
while True:
    root.winfo_exists()
    root.update()

    if pathNotFound:
        node = Node(randint(0, windowSize), randint(0, windowSize), len(nodes))
        closestNode = findClosestNode(nodes, node)
        node = replaceWithCloserNode(node, closestNode)

        if inObs(node):
            continue

        closestNode = replaceWithProximalNode(node, closestNode, nodes)

        node.cost = closestNode.cost + L(closestNode, node)
        node.heading = atan2(node.y - closestNode.y, node.x - closestNode.x)
        node.parent = closestNode.id
        
        minDistanceToAnyObstacle = float('inf')
        for obstacle in obstacles:
            if type(obstacle) == Shape:
                distanceToObstacle = obstacle.distanceTo(node)
                if distanceToObstacle < minDistanceToAnyObstacle:
                    minDistanceToAnyObstacle = distanceToObstacle

        if minDistanceToAnyObstacle < 30:
            continue

        if not steer(closestNode, node):
            continue

        nodes.append(node)
        drawCircle(canvas, node.x, node.y, "red")

        drawArc(canvas, closestNode, node)

        if inGoal(node):
            pathNotFound = False

            currentNode = node.id
            while currentNode != 0:        
                drawArc(canvas, nodes[nodes[currentNode].parent], nodes[currentNode], "darkgoldenrod1", 3)
                currentNode = nodes[currentNode].parent
