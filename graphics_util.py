import numpy as np
from data_util import Vertex
import pygame as pg

class Graphics():
    def __init__(self, vertex_matrix, faces):
        self.vertex_matrix = vertex_matrix
        # self.vertices = vertex_matrix.vertices
        self.faces = faces
        self.screen_size = np.array([800, 800])
        self.dragging = False
        self.prev_mouse_pos = np.array([0, 0])
        self.curr_mouse_pos = np.array([0, 0])
        self.color_limit_low = "0x00005F"
        self.color_limit_high = "0x0000FF"
    
    def to_pygame_coordinates(self, vertices):
        """
        Change the coordinates of the vertices to pygame coordinates
        """
        game_vertices = []
        # set origin to center of screen
        origin = self.screen_size / 2
        # scale the vertices to fit the screen
        scale = 0.2 * min(self.screen_size)
        for vertex in vertices:
            x = vertex.x * scale + origin[0]
            y = vertex.y * scale + origin[1]
            game_vertices.append(Vertex(x, y, vertex.z))
        return game_vertices

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
                # Did the user click the mouse button?
                if event.type == pg.MOUSEBUTTONDOWN:
                    # If the user clicked the mouse button, set drag state
                    self.dragging = True
                # Did the user release the mouse button?
                if event.type == pg.MOUSEBUTTONUP:
                    # If the user released the mouse button, set drag state
                    self.dragging = False
                if event.type == pg.MOUSEMOTION:
                    if self.dragging and pg.mouse.get_pressed()[0]:
                        # If the user is dragging the mouse, update the vertices
                        self.prev_mouse_pos = self.curr_mouse_pos
                        self.curr_mouse_pos = np.array(pg.mouse.get_pos())
                        self.update()
                    else:
                        self.prev_mouse_pos = self.curr_mouse_pos
                        self.curr_mouse_pos = np.array(pg.mouse.get_pos())
                    
            # set origin to center of screen
            # Fill the background with white
            screen.fill((255, 255, 255))
            # Draw a solid blue circle in the center
            # vertices = self.vertex_matrix.vertices
            vertices = self.to_pygame_coordinates(self.vertex_matrix.vertices)
            for vertex in vertices:
                # print(int(vertex.x), int(vertex.y))
                pg.draw.circle(screen, (0, 0, 255), (int(vertex.x), int(vertex.y)), 5)
            for face in self.faces:
                vertices = face.get_vertices()
                if mode == 'part1':
                    vertices = self.to_pygame_coordinates(vertices)
                    # draw edges between vertices
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[0].x), int(vertices[0].y)), (int(vertices[1].x), int(vertices[1].y)))
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[1].x), int(vertices[1].y)), (int(vertices[2].x), int(vertices[2].y)))
                    pg.draw.line(screen, (0, 0, 255), (int(vertices[2].x), int(vertices[2].y)), (int(vertices[0].x), int(vertices[0].y)))
                elif mode == 'part2':
                    # draw polygon
                    color = self.get_polygon_color(vertices[0], vertices[1], vertices[2])
                    # only display polygons in the front
                    vertices = self.to_pygame_coordinates(vertices)
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
            theta = -mouse_movement[1] * 0.01
            self.vertex_matrix.rotate_along_axis(theta, 'x')

            theta = mouse_movement[0] * 0.01
            self.vertex_matrix.rotate_along_axis(theta, 'y')
    
    def get_polygon_color(self, v1, v2, v3):
        """
        Given 3 vertices, find the color of the polygong according to the angle between this surface and the z-axis
        Color needs to be calculated in between the color limit low and high
        Color will be limit high if the angle is 0 and color will be limit low if the angle is 90
        """
        # Get the angle between the surface and the z-axis
        angle = self.get_angle(v1, v2, v3)
        # Calculate the color
        # interpolate between the color limit low and high according to angle between 0 to 90
        color_range = int(self.color_limit_high, 16) - int(self.color_limit_low, 16)
        color = int(self.color_limit_low, 16) + int(angle / 90 * color_range)
        color = abs(color)
        color = hex(color)
        # convert from hex to rgb
        color = (0,0,int(color[2:], 16))
        return color
    
    def get_angle(self, v1, v2, v3):
        """
        Given 3 vertices, find the angle between the surface and the z-axis
        """
        # Get the normal vector of the surface
        normal = self.get_normal(v1, v2, v3)
        # Get the angle between the normal and the z-axis
        # angle = np.arccos(normal[2] / np.linalg.norm(normal)) * 180 / np.pi
        dot = np.dot(np.array([0,0,1]), normal)
        angle = (np.arccos(dot / np.linalg.norm(normal)) * 180 / np.pi) - 90.0
        return angle
    
    def get_normal(self, v1, v2, v3):
        """
        Given 3 vertices, find the normal vector of the surface
        """
        # Get the 2 vectors of the surface
        v1 = np.array([v1.x, v1.y, v1.z])
        v2 = np.array([v2.x, v2.y, v2.z])
        v3 = np.array([v3.x, v3.y, v3.z])
        v12 = v2 - v1
        v13 = v3 - v1
        # Get the cross product of the 2 vectors
        normal = np.cross(v12, v13)
        return normal
