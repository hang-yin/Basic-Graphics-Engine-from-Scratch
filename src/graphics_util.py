import numpy as np
import pygame as pg
from data_util import sort_faces

class Graphics():
    """
    A class to handle the graphics of the 3D object.

    Attributes:
        vertex_matrix: a VertexMatrix object
        faces: a list of Face objects
        mouse_sensitivity: the sensitivity of the mouse
        screen_size: the size of the screen
        prev_mouse_pos: the previous mouse position
        curr_mouse_pos: the current mouse position
        color_limit_low: the lower limit of the color
        color_limit_high: the upper limit of the color
    
    Methods:
        to_pygame_coordinates: change the coordinates of the vertices to pygame coordinates
        plot: plot the 3D object
        update: update the 3D object
        get_polygon_color: get the color of the polygon based on its angle wrt. the z-axis
        get_angle: get the angle of a polygon wrt. the z-axis
    """
    def __init__(self,
                 vertex_matrix,
                 faces,
                 window_size=(800, 800),
                 mouse_sensitivity=0.003,
                 color_limit_low="0x00005F",
                 color_limit_high="0x0000FF"):
        """
        Constructor for the Graphics class.

        Input: 
            vertex_matrix: a VertexMatrix object
            faces: a list of Face objects
            mouse_sensitivity: the sensitivity of the mouse
            window_size: the size of the screen
            color_limit_low: the lower limit of the color
            color_limit_high: the upper limit of the color
        """
        
        self.vertex_matrix = vertex_matrix
        # self.vertices = vertex_matrix.vertices
        self.faces = faces
        self.mouse_sensitivity = mouse_sensitivity
        self.screen_size = np.array(window_size)
        self.prev_mouse_pos = np.array([0, 0])
        self.curr_mouse_pos = np.array([0, 0])
        self.color_limit_low = color_limit_low
        self.color_limit_high = color_limit_high
        vertices = vertex_matrix.get_vertices()
        max_x_coord = max([vertex.x for vertex in vertices])
        max_y_coord = max([vertex.y for vertex in vertices])
        max_coord = max([max_x_coord, max_y_coord])
        self.scale = 0.25 * min(self.screen_size) / max_coord
        self.origin = self.screen_size / 2
        self.to_pygame_coordinates(self.vertex_matrix.get_vertices())

    def to_pygame_coordinates(self, vertices):
        """
        Change the coordinates of the vertices to pygame coordinates.

        Input:
            vertices: a list of Vertex objects
        """
        # scale the vertices to fit the screen
        for vertex in vertices:
            vertex.x = vertex.x * self.scale + self.origin[0]
            vertex.y = vertex.y * self.scale + self.origin[1]
            vertex.z = vertex.z * self.scale + self.origin[0]
        self.vertex_matrix.update_matrix(vertices)

    def plot(self, mode='part1'):
        """
        Plot 3D vertices and edges in 2D space with pygame. 

        Input:
            mode: the mode of the program (can be 'part1' or 'part2')
        """
        # Initialize pygame
        pg.init()
        # Set up the drawing window
        screen = pg.display.set_mode(self.screen_size)
        # Run until the user asks to quit
        running = True
        while running:
            for event in pg.event.get():
                # Did the user click the window close button?
                if event.type == pg.QUIT:
                    running = False
                # Is there a mouse movement?
                if event.type == pg.MOUSEMOTION:
                    self.prev_mouse_pos = self.curr_mouse_pos
                    self.curr_mouse_pos = np.array(pg.mouse.get_pos())
                    if pg.mouse.get_pressed()[0]:
                        # If the user is dragging the mouse, update the vertices
                        self.update()
            # Fill the background with white
            screen.fill((255, 255, 255))
            # Draw a solid blue circle for each vertex
            for vertex in self.vertex_matrix.get_vertices():
                pg.draw.circle(screen, (0, 0, 255), (int(vertex.x), int(vertex.y)), 5)
            # we sort the faces by their z coordinate
            self.faces = sort_faces(self.faces)
            for face in self.faces:
                vertices = face.get_vertices()
                if mode == 'part1':
                    # draw edges between vertices
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[0].x), int(vertices[0].y)), (int(vertices[1].x), int(vertices[1].y)))
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[1].x), int(vertices[1].y)), (int(vertices[2].x), int(vertices[2].y)))
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[2].x), int(vertices[2].y)), (int(vertices[0].x), int(vertices[0].y)))
                elif mode == 'part2':
                    # draw polygon
                    color = self.get_polygon_color(vertices[0], vertices[1], vertices[2])
                    pg.draw.polygon(screen,
                                    color,
                                    [(int(vertices[0].x), int(vertices[0].y)),
                                     (int(vertices[1].x), int(vertices[1].y)),
                                     (int(vertices[2].x), int(vertices[2].y))])
            # Flip the display
            pg.display.flip()
        # Done! Time to quit.
        pg.quit()
    
    def update(self):
        """
        Update the vertices and faces according to mouse drag.
        """
        # Get the mouse movement
        mouse_movement = self.prev_mouse_pos - self.curr_mouse_pos

        if mouse_movement[0] == 0 and mouse_movement[1] == 0:
            return
        else:
            theta = mouse_movement[1] * self.mouse_sensitivity
            self.vertex_matrix.rotate_along_axis(theta, 'x')

            theta = -mouse_movement[0] * self.mouse_sensitivity
            self.vertex_matrix.rotate_along_axis(theta, 'y')
    
    def get_polygon_color(self, v1, v2, v3):
        """
        Find the color of a polygon given 3 vertices.

        Input:
            v1, v2, v3: Vertex objects
        """
        # Get the angle between the surface and the z-axis
        angle = self.get_angle(v1, v2, v3)
        angle = abs(angle)
        # Calculate the color
        # interpolate between the color limit low and high according to angle between 0 to 90
        color_range = int(self.color_limit_high, 16) - int(self.color_limit_low, 16)
        color = int(self.color_limit_low, 16) + int(angle / 90 * color_range)
        color = hex(color)
        # convert from hex to rgb
        color = (0,0,int(color[2:], 16))
        return color
    
    def get_angle(self, v1, v2, v3):
        """
        Find the angle between a surface formed by three vertices and the z-axis.

        Input:
            v1, v2, v3: Vertex objects
        """
        # Get the normal vector of the surface
        # Get the 2 vectors of the surface
        v1 = np.array([v1.x, v1.y, v1.z])
        v2 = np.array([v2.x, v2.y, v2.z])
        v3 = np.array([v3.x, v3.y, v3.z])
        v12 = v2 - v1
        v13 = v3 - v1
        # Get the cross product of the 2 vectors
        normal = np.cross(v12, v13)
        # Get the angle between the normal and the z-axis
        dot = np.dot(np.array([0,0,1]), normal)
        angle = (np.arccos(dot / np.linalg.norm(normal)) * 180 / np.pi)
        # if angle is not a number, return 0
        if np.isnan(angle):
            return 0
        else:
            angle = angle - 90.0
            return angle
