# Welcome to spatial-tda


[![image](https://img.shields.io/pypi/v/spatial-tda.svg)](https://pypi.python.org/pypi/spatial-tda)

[![image](https://raw.githubusercontent.com/hashansl/spatial-tda/main/docs/assets/logo.png)](https://raw.githubusercontent.com/hashansl/spatial-tda/main/docs/assets/logo.png)

**A Python package for geospatial analysis and interactive mapping in a Jupyter environment.**

-   GitHub repo: <https://github.com/hashansl/spatial-tda>
<!-- -   Documentation: <https://spatial-tda.org> -->
-   PyPI: <https://pypi.org/project/spatial-tda>
<!-- -   Conda-forge: <https://anaconda.org/conda-forge/spatial-tda> -->
-   Free software: [MIT license](https://opensource.org/licenses/MIT)



## Introduction

<!-- **Leafmap** is a Python package for interactive mapping and geospatial analysis with minimal coding in a Jupyter environment. It is a spin-off project of the [geemap](https://geemap.org) Python package, which was designed specifically to work with [Google Earth Engine](https://earthengine.google.com) (GEE). However, not everyone in the geospatial community has access to the GEE cloud computing platform. Leafmap is designed to fill this gap for non-GEE users. It is a free and open-source Python package that enables users to analyze and visualize geospatial data with minimal coding in a Jupyter environment, such as Google Colab, Jupyter Notebook, JupyterLab, and [marimo](https://github.com/marimo-team/marimo). Leafmap is built upon several open-source packages, such as [folium](https://github.com/python-visualization/folium) and [ipyleaflet](https://github.com/jupyter-widgets/ipyleaflet) (for creating interactive maps), [WhiteboxTools](https://github.com/jblindsay/whitebox-tools) and [whiteboxgui](https://github.com/opengeos/whiteboxgui) (for analyzing geospatial data), and [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) (for designing interactive graphical user interfaces [GUIs]). Leafmap has a toolset with various interactive tools that allow users to load vector and raster data onto the map without coding. In addition, users can use the powerful analytical backend (i.e., WhiteboxTools) to perform geospatial analysis directly within the leafmap user interface without writing a single line of code. The WhiteboxTools library currently contains **500+** tools for advanced geospatial analysis, such as [GIS Analysis](https://jblindsay.github.io/wbt_book/available_tools/gis_analysis.html), [Geomorphometric Analysis](https://jblindsay.github.io/wbt_book/available_tools/geomorphometric_analysis.html), [Hydrological Analysis](https://jblindsay.github.io/wbt_book/available_tools/hydrological_analysis.html), [LiDAR Data Analysis](https://jblindsay.github.io/wbt_book/available_tools/lidar_tools.html), [Mathematical and Statistical Analysis](https://jblindsay.github.io/wbt_book/available_tools/mathand_stats_tools.html), and [Stream Network Analysis](https://jblindsay.github.io/wbt_book/available_tools/stream_network_analysis.html). -->

## Acknowledgments

This project is supported by Amazon Web Services ([AWS](https://aws.amazon.com)).

## Statement of Need

<!-- There is a plethora of Python packages for geospatial analysis, such as [geopandas](https://geopandas.org) for vector data analysis and [xarray](https://docs.xarray.dev) for raster data analysis. As listed at [pyviz.org](https://pyviz.org), there are also many options for plotting data on a map in Python, ranging from libraries focused specifically on maps like [ipyleaflet](https://ipyleaflet.readthedocs.io) and [folium](https://python-visualization.github.io/folium) to general-purpose plotting tools that also support geospatial data types, such as [hvPlot](https://hvplot.pyviz.org), [bokeh](http://bokeh.org), and [plotly](https://plotly.com/python). While these tools provide powerful capabilities, displaying geospatial data from different file formats on an interactive map and performing basic analyses can be challenging, especially for users with limited coding skills. Furthermore, many tools lack bi-directional communication between the frontend (browser) and the backend (Python), limiting their interactivity and usability for exploring map data. -->

Leafmap addresses these challenges by leveraging the bidirectional communication provided by ipyleaflet, enabling users to load and visualize geospatial datasets with just one line of code. Leafmap also provides an interactive graphical user interface (GUI) for loading geospatial datasets without any coding. It is designed for anyone who wants to analyze and visualize geospatial data interactively in a Jupyter environment, making it particularly accessible for novice users with limited programming skills. Advanced programmers can also benefit from leafmap for geospatial data analysis and building interactive web applications.

## Usage

Launch the interactive notebook tutorial for the **leafmap** Python package with Amazon SageMaker Studio Lab, Microsoft Planetary Computer, Google Colab, or Binder:

<!-- [![image](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/opengeos/leafmap/blob/master/examples/notebooks/00_key_features.ipynb)
[![image](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opengeos/leafmap/blob/master)
[![image](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/opengeos/leafmap/HEAD) -->

<!-- Check out this excellent article on Medium - [Leafmap a new Python Package for Geospatial data science](https://link.medium.com/HRRKDcynYgb) -->

## Key Features  

The **AdjacencySimplex** class and the **compute_persistence** function provide a comprehensive framework for processing geospatial data, constructing simplicial complexes, and performing topological data analysis (TDA). These functionalities enable the study of spatial structures and relationships with a focus on **spatial adjacency, simplicial complexes, and persistent homology**. The key features include:  

### **Geospatial Data Processing and Filtering**
- **Filtering and sorting geospatial data:** The class enables filtering and sorting a GeoDataFrame based on a specified variable. Sorting methods include ascending and descending orders.  
- **Threshold-based filtering:** Users can define minimum and maximum thresholds to focus on specific data ranges.  
- **Geospatial integrity maintenance:** The framework ensures that processed data retains its **geometric properties and CRS** for further spatial analysis.  

### **Adjacency Computation and Simplicial Complex Construction**
- **Computing adjacency relationships:** The class uses spatial joins to identify neighboring geographic entities while removing self-intersections.  
- **Creating adjacency dictionaries:** The adjacency relationships are stored in a dictionary format, making them easy to use for further computations.  
- **Generating simplicial complexes:** The class constructs **Vietoris-Rips simplicial complexes** using adjacency relationships, enabling higher-order topological analysis.  

### **Persistent Homology and Topological Summaries**
- **Computing persistence diagrams:** The **compute_persistence** function constructs a **Simplex Tree** using **Gudhi**, assigning filtration values based on the input variable.  
- **Extracting H0 features (connected components):** The function calculates **zero-dimensional (H0) persistence intervals**, representing connected components in the dataset.  
- **Handling infinite persistence values:** Infinite intervals are replaced with the **maximum variable value** to ensure finite computations.  
- **Topological summaries (TDA metrics):** The function computes essential TDA summaries for dimension 0, including:  
  - **H0 data points:** The number of connected components.  
  - **Total Lifespan (TL):** The sum of persistence intervals.  
  - **Average Lifespan (AL):** The mean lifespan of connected components.  
  - **Total Mid-Lifespan (TML):** The sum of midpoints of persistence intervals.  
  - **Average Mid-Lifespan (AML):** The average of midpoints of persistence intervals.  

### **Efficient Computational Design**
- **Optimized spatial computations:** The class efficiently processes adjacency relationships, even for large datasets.  
- **Integration with Pandas, GeoPandas, and Gudhi:** The framework seamlessly works with popular Python libraries for geospatial and topological data analysis.  
- **Dynamic variable selection:** Users can select any **numerical attribute** to control filtering and sorting.  

These features make the **AdjacencySimplex** class and **compute_persistence** function **powerful tools for geospatial topological data analysis**, helping researchers explore **spatial connectivity, adjacency structures, and persistent homology in geospatial datasets**. Whether for **epidemiology, environmental studies, urban planning, or regional connectivity analysis**, this framework provides an intuitive and structured approach to **spatial TDA**.

## Citations

If you find **spatial-tda** useful in your research, please consider citing the following paper to support my work. Thank you for your support.

