import geopandas as gpd
import pandas as pd
import spatial_tda.invr as invr

class AdjacencySimplex:
    """
    A class to process a GeoDataFrame, filter and sort it based on a variable, 
    compute adjacency relationships, and form a simplicial complex.
    """
    
    def __init__(self, gdf, variable, threshold=None, filter_method='up'):
        """
        Initialize with a GeoDataFrame.
        
        Parameters:
        - gdf: GeoDataFrame containing geographic and attribute data.
        - variable: Column name used for filtering and sorting.
        - threshold: Tuple (min, max) for filtering values within a range.
        - filter_method: Sorting method, either 'up' (descending) or 'down' (ascending).
        """
        self.gdf = gdf
        self.variable = variable
        self.filter_method = filter_method
        self.threshold = threshold

    def filter_sort_gdf(self):
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
        return filtered_df, gdf

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

    def form_simplicial_complex(self):
        """
        Construct a simplicial complex using adjacency relationships.
        """
        if not hasattr(self, 'adjacent_counties_dict'):
            raise ValueError("Run calculate_adjacent_countries() before calling this method.")
        
        max_dimension = 3  # Define maximum dimension for the simplicial complex
        simplicial_complex = invr.incremental_vr([], self.adjacent_counties_dict, max_dimension, list(self.adjacent_counties_dict.keys()))
        
        return simplicial_complex
