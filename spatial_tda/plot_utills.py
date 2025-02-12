
# import libraries
import io
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def fig2img(fig):
     #convert matplot fig to image and return it

     buf = io.BytesIO()
     fig.savefig(buf)
     buf.seek(0)
     img = Image.open(buf)
     return img

def plot_simplicial_complex_gif(dataframe, simplices, variable, list_gif=[]):
    """
    Plot the simplicial complex, including edges and triangles.
    
    Parameters:
    - dataframe: GeoDataFrame containing the geographic data.
    - simplices: List of edges and triangles forming the simplicial complex.
    - variable: Column name for labeling data points.
    - list_gif: List to store generated frames for animations.
    """
    
    # Extract centroids for positioning labels
    city_coordinates = {row['sortedID']: np.array((row['geometry'].centroid.x, row['geometry'].centroid.y)) for _, row in dataframe.iterrows()}
    
    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_axis_off()
    dataframe.plot(ax=ax, edgecolor='black', linewidth=0.3, color="white")
    
    # Plot centroids with variable labels
    for _, row in dataframe.iterrows():
        centroid = row['geometry'].centroid
        plt.text(centroid.x, centroid.y, f"{row[variable]:.3f}", fontsize=10, ha='center', color="black")
    
    # Plot simplicial complex edges and triangles
    for simplex in simplices:
        if len(simplex) == 2:
            ax.plot(*zip(*[city_coordinates[vertex] for vertex in simplex]), color='red', linewidth=2)
        elif len(simplex) == 3:
            ax.add_patch(plt.Polygon([city_coordinates[vertex] for vertex in simplex], color='green', alpha=0.2))
        
        # Capture frame for animation
        img = fig2img(fig)
        list_gif.append(img)
    
        plt.close(fig)
    
    return list_gif