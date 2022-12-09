import numpy as np
import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def get_vertices(self):
        return [self.v1, self.v2]
    
class Face:
    def __init__(self, v1, v2, v3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
    
    def get_vertices(self):
        return [self.v1, self.v2, self.v3]
    
    def get_edges(self):
        return [Edge(self.v1, self.v2), Edge(self.v2, self.v3), Edge(self.v3, self.v1)]

class Graphics:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        self.ax.set_zlim(-1, 1)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('figure_enter_event', self.on_enter)
        self.fig.canvas.mpl_connect('figure_leave_event', self.on_leave)
        self.fig.canvas.mpl_connect('draw_event', self.on_draw)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('draw_event', self.on_draw)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.fig.canvas.mpl_connect('figure_enter_event', self.on_enter)
    
    def on_click(self, event):
        print('click')
    
    def read_file(self, filename):
        with open(filename, 'r') as f:
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
                faces.append(Face(vertices[int(f[0])], vertices[int(f[1])], vertices[int(f[2])]))
            return vertices, faces