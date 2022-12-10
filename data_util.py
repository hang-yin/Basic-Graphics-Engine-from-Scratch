import numpy as np

class Vertex():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Edge():
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def get_vertices(self):
        return [self.v1, self.v2]
    
class Face():
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def get_vertices(self):
        return [self.v1, self.v2, self.v3]
    
    def get_edges(self):
        return [Edge(self.v1, self.v2), Edge(self.v2, self.v3), Edge(self.v3, self.v1)]

def read_file(file_name):
    """
    Read a file and return a list of vertices and a list of faces
    """
    with open(file_name, 'r') as f:
        lines = f.readlines()
        num_vertices = int(lines[0].split(',')[0])
        num_faces = int(lines[0].split(',')[1])
        vertices = []
        for i in range(num_vertices):
            v = lines[i+1].split(',')
            vertices.append(Vertex(float(v[1]), float(v[2]), float(v[3])))
        faces = []
        for i in range(num_faces):
            f = lines[i+1+num_vertices].split(',')
            faces.append(Face(vertices[int(f[0])-1], vertices[int(f[1])-1], vertices[int(f[2])-1]))
        return vertices, faces
