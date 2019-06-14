import sys
import inspect
import heapq, random

class Node:
    def __init__(self, successor, parent=None):
      self.state = successor[0]
      self.parent = parent
      self.action = successor[1]
      if parent == None or parent.pathCost == None:
          self.pathCost = successor[2]
      else:
          self.pathCost = parent.pathCost + successor[2]

    def getPath(self):
      path = list()
      currentNode = self
      while currentNode.action != None:
          path.insert(0, currentNode.action)
          currentNode = currentNode.parent
      return path

class GraphQueue:
  def __init__(self):
    self.list = []
    self.stateList = []

  def push(self,node):
    self.list.insert(0,node)
    self.stateList.insert(0,node.state)
  def pop(self):

    self.stateList.pop()
    return self.list.pop()

  def isEmpty(self):
    return len(self.list) == 0



class GraphStack:
  def __init__(self):
    self.list = []
    self.stateList = []
  def push(self,node):
    self.list.append(node)
    self.stateList.append(node.state)
  def pop(self):
    self.stateList.pop()
    return self.list.pop()

  def isEmpty(self):
    return len(self.list) == 0



class Stack:
  def __init__(self):
    self.list = []

  def push(self,item):
    self.list.append(item)

  def pop(self):
    return self.list.pop()

  def isEmpty(self):
    return len(self.list) == 0


class Queue:
  def __init__(self):
    self.list = []

  def push(self,item):
    self.list.insert(0,item)

  def pop(self):
    return self.list.pop()

  def isEmpty(self):
    return len(self.list) == 0

class PriorityQueue:
  def  __init__(self):
    self.heap = []
    self.stateList = []

  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)
      self.stateList.append(item.state)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      self.stateList.remove(item.state)
      return item

  def isEmpty(self):
    return len(self.heap) == 0