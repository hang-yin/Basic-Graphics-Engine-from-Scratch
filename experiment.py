import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

# Define the vertices of the 3D object as a list of (x, y, z) coordinates
vertices = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

# Create a figure and a 3D Axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the vertices of the 3D object using matplotlib
ax.scatter(vertices[0], vertices[1], vertices[2])

# Connect the vertices with lines to create the edges of the 3D object
for i in range(len(vertices)):
    for j in range(len(vertices)):
        if i != j:
            ax.plot([vertices[i][0], vertices[j][0]], [vertices[i][1], vertices[j][1]], [vertices[i][2], vertices[j][2]])

# Enable mouse interaction with the 3D object
ax.mouse_init()

# Add labels and title to the plot
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D Object in 2D Space')

# Show the plot
plt.show()
