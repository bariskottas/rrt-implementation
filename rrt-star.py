import tkinter as tk
from random import randint
from math import sqrt
from math import atan2

class Node:
    x:int
    y:int
    cost:int

    id:int
    parent:int

    def __init__(self, x, y, id = 0, parent = -1):    
        self.x = x
        self.y = y
        self.cost = 0

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

    def intersects(self, edge):
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
        
        return False
    
def drawCircle(canvas, x, y, color):
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline = color, fill = color, width = 0)
    canvas.pack()

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

def findClosestNode(nodes, node):
    closestDist = float('inf')
    closestNode = node

    for possibleNode in nodes:
        dist = sqrt((node.x - possibleNode.x) ** 2 + (node.y - possibleNode.y) ** 2)
        if dist <= closestDist:
            closestDist = dist
            closestNode = possibleNode

    if closestNode == node:
        return None

    return closestNode

def replaceWithCloserNode(node, closestNode):
    dist = sqrt((node.x - closestNode.x) ** 2 + (node.y - closestNode.y) ** 2)

    if dist <= 20:
        return node
    
    ratio = 20 / dist

    return Node((1 - ratio) * closestNode.x + ratio * node.x, (1 - ratio) * closestNode.y + ratio * node.y, node.id)

def replaceWithProximalNode(node, closestNode, nodes):
    proximalNode = closestNode
    for possibleProximalNode in nodes:
        if possibleProximalNode.cost < proximalNode.cost and sqrt((node.x - possibleProximalNode.x) ** 2 + (node.y - possibleProximalNode.y) ** 2) <= 60:
            proximalNode = possibleProximalNode
    
    return proximalNode

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

        if closestNode.parent != -1:
            closestNodeParent:Node = nodes[closestNode.parent]
            if closestNode.x - closestNodeParent.x == 0:
                m1 = float('inf')
            else:
                m1 = (closestNode.y - closestNodeParent.y) / (closestNode.x - closestNodeParent.x)
            
            if node.x - closestNode.x == 0:
                m2 = float('inf')
            else:
                m2 = (node.y - closestNode.y) / (node.x - closestNode.x)

            angle = abs(atan2(m1 - m2, 1 + m1 * m2))
            if angle >= 0.6:
                continue
        
        edge = Edge(node, closestNode)
        
        intersectionExists = False
        for obstacle in obstacles:
            if type(obstacle) == Shape and obstacle.intersects(edge):
                intersectionExists = True
                break

        if intersectionExists:
            continue
                
        node.cost = closestNode.cost + sqrt((node.x - closestNode.x) ** 2 + (node.y - closestNode.y) ** 2)
        node.parent = closestNode.id

        nodes.append(node)
        drawCircle(canvas, node.x, node.y, "red")

        canvas.create_line(edge.node1.x, edge.node1.y, edge.node2.x, edge.node2.y, fill = "black", width = 1)

        if inGoal(node):
            pathNotFound = False

            currentNode = node.id
            while currentNode != 0:
                if type(nodes[currentNode]) == Node and type(nodes[nodes[currentNode].parent]) == Node:
                    canvas.create_line(nodes[currentNode].x, nodes[currentNode].y, nodes[nodes[currentNode].parent].x, nodes[nodes[currentNode].parent].y, fill = "darkgoldenrod1", width = 3)
                
                currentNode = nodes[currentNode].parent
