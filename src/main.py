from graphics_util import Graphics
from data_util import read_file

def main():
    vertex_matrix, faces = read_file('examples/object2.txt')
    graphics = Graphics(vertex_matrix=vertex_matrix,
                        faces=faces,
                        window_size=(800,800),
                        mouse_sensitivity=0.003,
                        color_limit_low="0x00005F",
                        color_limit_high="0x0000FF")
    # ask for user input to know which part to run
    part = input("Which part do you want to run? (1 or 2) ")
    if part == '1':
        graphics.plot('part1')
    elif part == '2':
        graphics.plot('part2')
    else:
        raise ValueError("Part must be 1 or 2")

if __name__ == '__main__':
    main()