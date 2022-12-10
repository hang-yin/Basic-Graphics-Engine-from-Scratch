from graphics_util import Graphics
from data_util import VertexMatrix, read_file

def main():
    vertex_matrix, faces = read_file('object.txt')
    graphics = Graphics(vertex_matrix, faces)
    # graphics.plot()
    graphics.plot('part2')

if __name__ == '__main__':
    main()