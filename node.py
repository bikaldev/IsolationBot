class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.children = []
        self.parent = None
  
    def set_id(self,id):
        self.id = id
    
    def set_data(self,data):
        self.data = data
    
    def set_child(self, child):
        child.parent = self
        self.children.append(child)
        return child