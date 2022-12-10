import numpy as np
from data_util import Vertex, sort_faces
import pygame as pg

class Graphics():
    def __init__(self, vertex_matrix, faces):
        self.vertex_matrix = vertex_matrix
        # self.vertices = vertex_matrix.vertices
        self.faces = faces
        self.screen_size = np.array([800, 800])
        self.prev_mouse_pos = np.array([0, 0])
        self.curr_mouse_pos = np.array([0, 0])
        self.color_limit_low = "0x00005F"
        self.color_limit_high = "0x0000FF"
        vertices = vertex_matrix.get_vertices()
        max_x_coord = max([vertex.x for vertex in vertices])
        max_y_coord = max([vertex.y for vertex in vertices])
        max_coord = max([max_x_coord, max_y_coord])
        self.scale = 0.25 * min(self.screen_size) / max_coord
        self.origin = self.screen_size / 2
        self.to_pygame_coordinates(self.vertex_matrix.get_vertices())

    def to_pygame_coordinates(self, vertices):
        """
        Change the coordinates of the vertices to pygame coordinates
        """
        # scale the vertices to fit the screen
        for vertex in vertices:
            vertex.x = vertex.x * self.scale + self.origin[0]
            vertex.y = vertex.y * self.scale + self.origin[1]
            vertex.z = vertex.z * self.scale + self.origin[0]
        self.vertex_matrix.update_matrix(vertices)

    def plot(self, mode='part1'):
        """
        Plot 3D vertices and edges in 2D space with pygame
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
                    #for vertex in vertices:
                        #print(vertex.x, vertex.y, vertex.z)
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
        Update the vertices and faces according to mouse drag
        Need to incorporate rotation along x, y, and z axis using matrix operations
        """
        # Get the mouse movement
        mouse_movement = self.prev_mouse_pos - self.curr_mouse_pos

        if mouse_movement[0] == 0 and mouse_movement[1] == 0:
            return
        else:
            theta = mouse_movement[1] * 0.001
            self.vertex_matrix.rotate_along_axis(theta, 'x')

            theta = -mouse_movement[0] * 0.001
            self.vertex_matrix.rotate_along_axis(theta, 'y')
    
    def get_polygon_color(self, v1, v2, v3):
        """
        Given 3 vertices, find the color of the polygong according to the angle between this surface and the z-axis
        Color needs to be calculated in between the color limit low and high
        Color will be limit high if the angle is 0 and color will be limit low if the angle is 90
        """
        # Get the angle between the surface and the z-axis
        angle = self.get_angle(v1, v2, v3)
        angle = abs(angle)
        # Calculate the color
        # interpolate between the color limit low and high according to angle between 0 to 90
        color_range = int(self.color_limit_high, 16) - int(self.color_limit_low, 16)
        color = int(self.color_limit_low, 16) + int(angle / 90 * color_range)
        # color = abs(color)
        # print(color)
        color = hex(color)
        # convert from hex to rgb
        color = (0,0,int(color[2:], 16))
        return color
    
    def get_angle(self, v1, v2, v3):
        """
        Given 3 vertices, find the angle between the surface and the z-axis
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
        # angle = np.arccos(normal[2] / np.linalg.norm(normal)) * 180 / np.pi
        dot = np.dot(np.array([0,0,1]), normal)
        angle = (np.arccos(dot / np.linalg.norm(normal)) * 180 / np.pi) - 90.0
        return angle
