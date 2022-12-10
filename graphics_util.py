import numpy as np
import matplotlib.pyplot as plt
from data_util import Vertex, Edge, Face, read_file, VertexMatrix
from matrix_util import matrix_multiplication, rotation_along_axis
import pygame as pg

"""
Using 2D graphics only, create a window which will display a 3D object defined by vertices and 
the edges of the faces of the object. 
Represent the vertices using small, filled blue circles, and the edges using straight blue lines. 
The edges will be lines which go between the vertices, and the faces should be transparent, 
such that a wireframe of the 3D object is displayed. 
Make the object fill approximately half of the window both vertically and horizontally. 

Set up the coordinate frame of the window such that:
the positive X-axis is pointing horizontally to the right,
the positive Y-axis is pointing vertically upward,
the positive Z-axis is pointing out of the plane of the window toward the observer, and
the origin is at the center of the window.
Assume that the observer is an infinite distance from the canvas.

Now write code to read and display any 3D object from a comma-separated text file specified by the user. 
A sample object text file is attached in “object.txt.” The format of the file is:
The first line contains two integers. 
The first integer is the number of vertices that define the 3D object, 
and the second number is the number of faces that define the 3D object.
Starting at the second line each line will define one vertex of the 3D object 
and will consist of an integer followed by three real numbers. 
The integer is the ID of the vertex and the three real numbers define the (x,y,z) coordinates of the vertex. 
The number of lines in this section will be equal to the first integer in the file.
Following the vertex section will be a section defining the faces of the 3D object. 
The number of lines in this section will be equal to the second integer on the first line of the file. 
Each line in this section will consist of three integers that define a triangle that is a face of the object. 
The three integers each refer to the ID of a vertex from the second section of the file.

Add click and drag mouse functionality such that while the mouse button is pressed, 
movement of the mouse rotates the object thusly:
Horizontal movement of the mouse rotates the 3D object about the window's Y-axis.
Vertical movement of the mouse rotates the 3D object about the window's X-axis.
Diagonal movement of the mouse is decomposed into vertical and horizontal components and 
rotates the 3D object accordingly as above.
The point of the object nearest to the observer follows the mouse's direction
"""

class Graphics():
    def __init__(self, vertex_matrix, faces):
        self.vertex_matrix = vertex_matrix
        # self.vertices = vertex_matrix.vertices
        self.faces = faces
        self.screen_size = np.array([800, 800])
        self.dragging = False
        self.prev_mouse_pos = np.array([0, 0])
        self.curr_mouse_pos = np.array([0, 0])
    
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

    def plot(self):
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
                vertices = self.to_pygame_coordinates(vertices)
                pg.draw.line(screen, (0, 0, 255), (int(vertices[0].x), int(vertices[0].y)), (int(vertices[1].x), int(vertices[1].y)))
                pg.draw.line(screen, (0, 0, 255), (int(vertices[1].x), int(vertices[1].y)), (int(vertices[2].x), int(vertices[2].y)))
                pg.draw.line(screen, (0, 0, 255), (int(vertices[2].x), int(vertices[2].y)), (int(vertices[0].x), int(vertices[0].y)))
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
