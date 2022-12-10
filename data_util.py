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

class VertexMatrix():
    def __init__(self, vertices):
        self.vertices = vertices
        self.matrix = self.create_matrix()
    
    def create_matrix(self):
        """
        Create a matrix of vertices
        """
        matrix = np.zeros((3, len(self.vertices)))
        for i, vertex in enumerate(self.vertices):
            matrix[0][i] = vertex.x
            matrix[1][i] = vertex.y
            matrix[2][i] = vertex.z
        return matrix
    
    def get_matrix(self):
        return self.matrix
    
    def get_vertices(self):
        return self.vertices
    
    def rotate_along_axis(self, theta, axis):
        """
        Rotate the vertices along an axis
        """
        if axis == 'x':
            rotation_matrix = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
        elif axis == 'y':
            rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
        elif axis == 'z':
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
        else:
            raise ValueError("Axis must be 'x', 'y', or 'z'")
        self.matrix = np.dot(rotation_matrix, self.matrix)
        self.update_vertices()
    
    def update_vertices(self):
        """
        Update the vertices with the new matrix
        """
        for i, vertex in enumerate(self.vertices):
            vertex.x = self.matrix[0][i]
            vertex.y = self.matrix[1][i]
            vertex.z = self.matrix[2][i]

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
        vertex_matrix = VertexMatrix(vertices)
        return vertex_matrix, faces
