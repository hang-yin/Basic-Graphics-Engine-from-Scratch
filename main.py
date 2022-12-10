from graphics_util import Graphics
from data_util import read_file, VertexMatrix

def main():
    vertices, faces = read_file('object.txt')
    vertex_matrix = VertexMatrix(vertices)
    graphics = Graphics(vertex_matrix, faces)
    graphics.plot()

if __name__ == '__main__':
    main()