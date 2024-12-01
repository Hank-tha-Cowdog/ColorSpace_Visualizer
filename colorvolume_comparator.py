import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

def xy_to_XYZ(x, y):
    """Convert CIE xy chromaticity coordinates to XYZ."""
    X = x / y
    Y = 1.0
    Z = (1 - x - y) / y
    return np.array([X, Y, Z])

def get_color_space_primaries():
    """Define color space primaries in xy chromaticity coordinates."""
    
    # Alexa Wide Gamut primaries
    alexa_primaries = {
        'red': (0.7347, 0.2653),
        'green': (0.1152, 0.8264),
        'blue': (0.1001, 0.1062),
        'white': (0.3127, 0.3290)  # D65
    }
    
    # ACES primaries
    aces_primaries = {
        'red': (0.7347, 0.2653),
        'green': (0.0000, 1.0000),
        'blue': (0.0001, -0.0770),
        'white': (0.32168, 0.33767)  # D60
    }
    
    return alexa_primaries, aces_primaries

def create_color_space_matrix(primaries):
    """Create RGB to XYZ transformation matrix for a color space."""
    # Convert primaries to XYZ
    primaries_XYZ = {
        color: xy_to_XYZ(x, y)
        for color, (x, y) in primaries.items()
    }
    
    # Create primary matrix
    M = np.column_stack([
        primaries_XYZ['red'],
        primaries_XYZ['green'],
        primaries_XYZ['blue']
    ])
    
    # Calculate RGB to XYZ matrix
    S = np.linalg.solve(M, primaries_XYZ['white'])
    M = M * S[:, np.newaxis]
    
    return M

def generate_gamut_points(steps=20):
    """Generate points to represent the color space volume."""
    vertices = []
    
    # Add primary points and black/white points
    vertices.append([0, 0, 0])  # Black
    vertices.append([1, 0, 0])  # Red primary
    vertices.append([0, 1, 0])  # Green primary
    vertices.append([0, 0, 1])  # Blue primary
    vertices.append([1, 1, 1])  # White
    
    # Add points along primary connecting lines and interior
    for i in range(steps):
        t = i / (steps - 1)
        # Primary connecting lines
        vertices.append([t, 1-t, 0])  # R-G
        vertices.append([0, t, 1-t])  # G-B
        vertices.append([1-t, 0, t])  # B-R
        
        # Interior points
        for j in range(steps):
            s = j / (steps - 1)
            vertices.append([t*s, (1-t)*s, (1-s)])
            vertices.append([s, t*s, (1-t)*(1-s)])
            vertices.append([(1-t)*s, s, t*(1-s)])
    
    return np.array(vertices)

def visualize_color_spaces():
    """Create 3D visualization comparing color spaces."""
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Get color space primaries and create transformation matrices
    alexa_primaries, aces_primaries = get_color_space_primaries()
    alexa_matrix = create_color_space_matrix(alexa_primaries)
    aces_matrix = create_color_space_matrix(aces_primaries)
    
    # Generate base points
    vertices = generate_gamut_points()
    
    # Transform vertices to XYZ space for both color spaces
    alexa_vertices = np.dot(alexa_matrix, vertices.T).T
    aces_vertices = np.dot(aces_matrix, vertices.T).T
    
    # Create and plot convex hulls
    for vertices, color, alpha, name in [
        (alexa_vertices, 'red', 0.2, 'Alexa Wide Gamut'),
        (aces_vertices, 'blue', 0.2, 'ACES')
    ]:
        hull = ConvexHull(vertices)
        for simplex in hull.simplices:
            pts = vertices[simplex]
            ax.plot_trisurf(pts[:,0], pts[:,1], pts[:,2],
                          alpha=alpha, color=color)
    
    # Plot primary points for both color spaces
    for primaries, matrix, color, marker in [
        (alexa_primaries, alexa_matrix, 'red', 'o'),
        (aces_primaries, aces_matrix, 'blue', '^')
    ]:
        primary_points = np.array([
            xy_to_XYZ(primaries['red'][0], primaries['red'][1]),
            xy_to_XYZ(primaries['green'][0], primaries['green'][1]),
            xy_to_XYZ(primaries['blue'][0], primaries['blue'][1])
        ])
        primary_points = np.dot(matrix, primary_points.T).T
        ax.scatter(primary_points[:,0], primary_points[:,1], primary_points[:,2],
                  c=color, s=100, marker=marker)
    
    # Set up the visualization
    arrow_length = max(np.max(alexa_vertices), np.max(aces_vertices)) * 1.2
    
    # Plot coordinate axes
    ax.plot([0, arrow_length], [0, 0], [0, 0], 'r-', linewidth=2)
    ax.plot([0, 0], [0, arrow_length], [0, 0], 'g-', linewidth=2)
    ax.plot([0, 0], [0, 0], [arrow_length], 'b-', linewidth=2)
    
    # Add legend
    ax.plot([], [], 'red', alpha=0.5, label='Alexa Wide Gamut')
    ax.plot([], [], 'blue', alpha=0.5, label='ACES')
    ax.legend()
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Color Space Comparison: Alexa Wide Gamut vs ACES')
    
    # Set axis limits
    max_val = arrow_length
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.set_zlim(0, max_val)
    
    # Add grid
    ax.grid(True)
    
    # Set initial view angle
    ax.view_init(elev=20, azim=45)
    
    return fig, ax

# Create and display the visualization
fig, ax = visualize_color_spaces()
plt.show()