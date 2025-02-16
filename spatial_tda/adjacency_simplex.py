import geopandas as gpd
import pandas as pd
import gudhi
import numpy as np
import spatial_tda.invr as invr
import io
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class AdjacencySimplex:
    """
    A class to process a GeoDataFrame, filter and sort it based on a variable, 
    compute adjacency relationships, and form a simplicial complex.
    """
    
    def __init__(self, geo_dataframe, variable, threshold=None, filter_method='up'):
        """
        Initialize with a GeoDataFrame.
        
        Parameters:
        - gdf: GeoDataFrame containing geographic and attribute data.
        - variable: Column name used for filtering and sorting.
        - threshold: Tuple (min, max) for filtering values within a range.
        - filter_method: Sorting method, either 'up' (descending) or 'down' (ascending).
        """
        self.gdf = geo_dataframe
        self.variable = variable
        self.filter_method = filter_method
        self.threshold = threshold
        self.filtered_df = None
        self.adjacent_counties_dict = None
        self.merged_df = None
        self.simplicial_complex = None

    def filter_sort_gdf(self,return_original=False,return_filtered=False):
        """
        Filter and sort the GeoDataFrame based on the specified variable and method.
        """
        gdf = self.gdf.copy()

        # Sort the DataFrame based on the specified method
        if self.filter_method == 'up':
            gdf = gdf.sort_values(by=self.variable, ascending=True)
        elif self.filter_method == 'down':
            # get the max value
            max_value = gdf[self.variable].max()
            # invert the values - Assuming negative values are not present
            gdf[self.variable] = max_value - gdf[self.variable]
            gdf = gdf.sort_values(by=self.variable, ascending=True)
        else:
            raise ValueError("Invalid filter method. Use 'up' or 'down'.")
        
        # this need to be done before filtering
        gdf['sortedID'] = range(len(gdf))

        # this for the below filter
        filtered_df = gdf.copy()

        # Apply threshold filtering if specified
        if self.threshold:
            filtered_df = filtered_df[(filtered_df[self.variable] >= self.threshold[0]) &
                                      (filtered_df[self.variable] <= self.threshold[1])]

        # Convert DataFrame to GeoDataFrame
        filtered_df = gpd.GeoDataFrame(filtered_df, geometry='geometry')

        # Set Coordinate Reference System (CRS)
        filtered_df.crs = "EPSG:4326"

        self.filtered_df = filtered_df

        # this returns a filtered dataframe and the original dataframe with the sortedID
        if return_original and return_filtered:
            return gdf, filtered_df
        elif return_filtered:
            return filtered_df
        elif return_original:
            return gdf
        

    def calculate_adjacent_countries(self):
        """
        Compute adjacency relationships between geographic entities.
        """
        # Ensure filter_sort_gdf() has been executed
        if not hasattr(self, 'filtered_df') or not isinstance(self.filtered_df, gpd.GeoDataFrame):
            raise ValueError("Run filter_sort_gdf() before calling this method.")

        # Perform spatial join to find adjacent entities
        adjacent_entities = gpd.sjoin(self.filtered_df, self.filtered_df, predicate='intersects', how='left')

        # Remove self-intersections
        adjacent_entities = adjacent_entities.query('sortedID_left != sortedID_right')

        # Group by entity and store adjacent entities in a list
        adjacent_entities = adjacent_entities.groupby('sortedID_left')['sortedID_right'].apply(list).reset_index()
        adjacent_entities.rename(columns={'sortedID_left': 'county', 'sortedID_right': 'adjacent'}, inplace=True)

        # Create adjacency dictionary
        adjacent_dict = dict(zip(adjacent_entities['county'], adjacent_entities['adjacent']))

        # Merge adjacency information with the original dataset
        merged_df = pd.merge(adjacent_entities, self.filtered_df, left_on='county', right_on='sortedID', how='left')
        
        # Convert to GeoDataFrame
        merged_df = gpd.GeoDataFrame(merged_df, geometry='geometry')
        merged_df.crs = "EPSG:4326"

        # Store results
        self.adjacent_counties_dict = adjacent_dict
        self.merged_df = merged_df

    def form_simplicial_complex(self,return_simplicial_complex=False):
        """
        Construct a simplicial complex using adjacency relationships.
        """
        if not hasattr(self, 'adjacent_counties_dict'):
            raise ValueError("Run calculate_adjacent_countries() before calling this method.")
        
        max_dimension = 3  # Define maximum dimension for the simplicial complex
        simplicial_complex = invr.incremental_vr([], self.adjacent_counties_dict, max_dimension, list(self.adjacent_counties_dict.keys()))
        
        self.simplicial_complex = simplicial_complex

        if return_simplicial_complex:
            return simplicial_complex
    

    def compute_persistence(self, summaries=None):
        """
        Compute persistence diagrams for the simplicial complex and return selected topological summaries.

        :param summaries: List of summary names to return (e.g., ["H0", "TL", "AL"]). If None, return all.
        :return: Dictionary with requested summaries.
        """

        st = gudhi.SimplexTree()
        st.set_dimension(2)

        for simplex in self.simplicial_complex:
            if len(simplex) == 1:
                st.insert([simplex[0]], filtration=0.0)

        for simplex in self.simplicial_complex:
            if len(simplex) == 2:
                last_simplex = simplex[-1]
                filtration_value = self.filtered_df.loc[
                    self.filtered_df['sortedID'] == last_simplex, self.variable
                ].values[0]
                st.insert(simplex, filtration=filtration_value)

        for simplex in self.simplicial_complex:
            if len(simplex) == 3:
                last_simplex = simplex[-1]
                filtration_value = self.filtered_df.loc[
                    self.filtered_df['sortedID'] == last_simplex, self.variable
                ].values[0]
                st.insert(simplex, filtration=filtration_value)

        st.compute_persistence()
        persistence = st.persistence()

        intervals_dim0 = st.persistence_intervals_in_dimension(0)

        # Replace infinity with the max variable value
        max_value = self.filtered_df[self.variable].max()
        intervals_dim0[:, 1][np.isinf(intervals_dim0[:, 1])] = max_value

        # Compute topological summaries
        H0_data_points = len(intervals_dim0)
        TL = sum(interval[1] - interval[0] for interval in intervals_dim0)
        TML = sum((interval[1] + interval[0]) / 2 for interval in intervals_dim0)

        AL = TL / len(intervals_dim0) if len(intervals_dim0) > 0 else 0
        AML = TML / len(intervals_dim0) if len(intervals_dim0) > 0 else 0

        # Store results in a dictionary
        results = {
            "H0": H0_data_points,
            "TL": TL,
            "AL": AL,
            "TML": TML,
            "AML": AML,
        }

        # Return only requested summaries
        if summaries:
            return {key: results[key] for key in summaries if key in results}
        return results  # Default: return all summaries
    
    @staticmethod
    def fig2img(fig):
        """
        Convert a Matplotlib figure to a PIL Image.

        Parameters:
        - fig: A Matplotlib figure.

        Returns:
        - A PIL Image.
        """
        buf = io.BytesIO()
        fig.savefig(buf, bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        img = Image.open(buf)
        return img
    
    def plot_simplicial_complex(self, save_dir=None):
        """
        Plot the simplicial complex and create a GIF animation showing its incremental construction.

        For each frame, the base map (self.gdf) is plotted along with labels, then
        all simplices up to that frame are drawn.

        Parameters:
        - save_dir: Directory path to save the GIF. If None, saves in the current directory.
        """
        if self.simplicial_complex is None:
            raise ValueError("Run form_simplicial_complex() before calling this method.")

        # Precompute centroids from filtered_df for plotting edges/triangles.
        city_coordinates = {
            row['sortedID']: np.array((row['geometry'].centroid.x, row['geometry'].centroid.y))
            for _, row in self.filtered_df.iterrows()
        }

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_axis_off() 

        # Plot the original GeoDataFrame without any filtration
        self.gdf.plot(ax=ax, edgecolor='black', linewidth=0.3, color="white")

        # Plot the centroid of the large square with values
        for _, row in self.gdf.iterrows():
            centroid = row['geometry'].centroid
            text_to_display = f"{row[self.variable]:.2f}"
            plt.text(centroid.x, centroid.y, text_to_display, fontsize=7, ha='center', color="black")
        

        frames = []
        for edge_or_triangle in self.simplicial_complex:

            # color sub regions based on how it enter the simplcial complex in adjacency method
            if len(edge_or_triangle) == 1:

                vertex = edge_or_triangle[0]
                # geometry = self.filtered_df.iterrows().loc[self.filtered_df.iterrows()['sortedID'] == vertex, 'geometry'].values[0]
                geometry = self.filtered_df[self.filtered_df['sortedID'] == vertex]['geometry'].values[0]
                ax.add_patch(Polygon(np.array(geometry.exterior.coords), closed=True, color='orange', alpha=0.3))
                img = self.fig2img(fig)
                frames.append(img)

            elif len(edge_or_triangle) == 2:
                # Plot an edge
                ax.plot(*zip(*[city_coordinates[vertex] for vertex in edge_or_triangle]), color='red', linewidth=2)
                img = self.fig2img(fig)
                frames.append(img)
            elif len(edge_or_triangle) == 3:
                # Plot a triangle
                ax.add_patch(plt.Polygon([city_coordinates[vertex] for vertex in edge_or_triangle], color='green', alpha=0.2))
                img = self.fig2img(fig)
                frames.append(img)

            #can change above code block
            plt.close(fig)

        
        # Define the GIF filename.
        gif_filename = f'adj_simplex_{self.variable}_{self.filter_method}.gif'
        
        if save_dir:
            gif_filename = f'{save_dir}/{gif_filename}'
        # Save the frames as a GIF.
        frames[0].save(gif_filename, save_all=True, append_images=frames[1:],
                       optimize=False, duration=600, loop=0)
        print(f"GIF created and saved as {gif_filename}.")