from graphics_util import Graphics
from data_util import read_file

def main():
    vertex_matrix, faces = read_file('examples/object.txt')
    graphics = Graphics(vertex_matrix=vertex_matrix,
                        faces=faces,
                        window_size=(800,800),
                        mouse_sensitivity=0.003,
                        color_limit_low="0x00005F",
                        color_limit_high="0x0000FF")
    graphics.plot('part2')

if __name__ == '__main__':
    main()