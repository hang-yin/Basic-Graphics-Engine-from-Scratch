import numpy as np

class Vertex():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
class Face():
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def get_vertices(self):
        return [self.v1, self.v2, self.v3]

class VertexMatrix():
    def __init__(self, vertices):
        self.vertices = vertices
        self.matrix = None
        self.update_matrix(self.vertices)
    
    def update_matrix(self, vertices):
        """Create a matrix of vertices"""
        matrix = np.zeros((3, len(vertices)))
        for i, vertex in enumerate(vertices):
            matrix[0][i] = vertex.x
            matrix[1][i] = vertex.y
            matrix[2][i] = vertex.z
        self.matrix = matrix
    
    def get_matrix(self):
        """Get the matrix"""
        return self.matrix
    
    def get_vertices(self):
        """Get the vertices"""
        return self.vertices
    
    def rotate_along_axis(self, theta, axis):
        """
        Rotate the vertices along an axis for a given angle.

        Input: 
            theta: the angle to rotate
            axis: the axis to rotate along ('x', 'y', or 'z')
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
        # Update the vertices with the new matrix
        for i, vertex in enumerate(self.vertices):
            vertex.x = self.matrix[0][i]
            vertex.y = self.matrix[1][i]
            vertex.z = self.matrix[2][i]

def sort_faces(faces):
    """
    Sort the faces by z-value from low to high.

    Input:
        faces: a list of Face objects
    Output:
        sorted_faces: a list of Face objects sorted by z-value
    """
    sorted_faces = sorted(faces, key=lambda face: (face.v1.z + face.v2.z + face.v3.z) / 3)
    sorted_faces.reverse()
    return sorted_faces

def read_file(file_name):
    """
    Read a file and return a list of vertices and a list of faces.

    Input: 
        file_name: the name of the file to read
    Output:
        vertex_matrix: a VertexMatrix object
        faces: a list of Face objects
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
