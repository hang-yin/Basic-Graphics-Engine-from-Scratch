import numpy as np

def matrix_multiplication(m1, m2):
    """
    Multiply two matrices
    """
    return np.dot(m1, m2)

def rotation_along_axis(theta, axis):
    """
    Create a rotation matrix along an axis
    """
    if axis == 'x':
        return np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    elif axis == 'y':
        return np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    elif axis == 'z':
        return np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")
