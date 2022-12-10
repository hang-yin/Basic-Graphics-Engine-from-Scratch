from graphics_util import Graphics
from data_util import read_file

def main():
    vertices, faces = read_file('object.txt')
    for vertex in vertices:
        print(vertex.x, vertex.y, vertex.z)
    graphics = Graphics(vertices, faces)
    graphics.to_pygame_coordinates()
    graphics.plot()

if __name__ == '__main__':
    main()