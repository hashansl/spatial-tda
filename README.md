# spatial-tda


[![image](https://img.shields.io/pypi/v/spatial-tda.svg)](https://pypi.python.org/pypi/spatial-tda)
[![image](https://img.shields.io/conda/vn/conda-forge/spatial-tda.svg)](https://anaconda.org/conda-forge/spatial-tda)

[![image](https://raw.githubusercontent.com/hashansl/spatial-tda/main/docs/assets/logo.png)](https://raw.githubusercontent.com/hashansl/spatial-tda/main/docs/assets/logo.png)

**A Python package for Topological Data Analysis(TDA) in spatial data.**

-   GitHub repo: <https://github.com/hashansl/spatial-tda>
-   Documentation: <https://hashansl.github.io/spatial-tda/>
-   PyPI: <https://pypi.org/project/spatial-tda>
-   Free software: [MIT license](https://opensource.org/licenses/MIT)


## Introduction

**Spatial-TDA** is a Python package designed for extracting topological information from spatial data with minimal coding. It provides an intuitive framework for applying **topological data analysis (TDA)** to geospatial datasets, enabling researchers and analysts to explore **spatial connectivity, adjacency relationships, and persistent homology** efficiently. Built on GeoPandas, Gudhi, and Matplotlib, the package integrates seamless workflows for adjacency detection, simplicial complex construction, and persistent homology computation while maintaining geospatial integrity. With automatic adjacency extraction, **Adjacency simplicial complex formation(Filtering up/ Filtering down)**, and topological visualization tools, **Spatial-TDA** simplifies geospatial TDA workflows, making it ideal for applications in epidemiology, environmental studies and spatial network analysis. Through a combination of computational efficiency and easy-to-use functions, **Spatial-TDA** bridges the gap between geospatial analytics and topological insights, enabling users to quantify and visualize higher-order spatial structures** with just a few lines of code.

## Usage

Launch the interactive notebook tutorial for the **spatial-tda** Python package with Google Colab:(upcoming)

## Key Features  

The **AdjacencySimplex** class and the **compute_persistence** function provide a comprehensive framework for processing geospatial data, constructing simplicial complexes, and performing topological data analysis (TDA). These functionalities enable the study of spatial structures and relationships with a focus on **spatial adjacency, simplicial complexes, and persistent homology**. The key features include:  

### **Geospatial Data Processing and Filtering**
- **Threshold-based filtering:** Users can define minimum and maximum thresholds to focus on specific data ranges.  
- **Geospatial integrity maintenance:** The framework ensures that processed data retains its geometric properties and CRS for further spatial analysis.  

### **Adjacency Computation and Simplicial Complex Construction**
- **Computing adjacency relationships:** The class currently uses  the Queen contiguity method to define adjacency, where regions are considered neighbors if they share at least one vertex. However, support for additional adjacency methods will be added soon, providing greater flexibility for geospatial topological analysis.
- **Generating simplicial complexes:** The class constructs **Adjacency simplicial complexes** using adjacency relationships for both **filtering up and filtering down methods**, enabling higher-order topological analysis with greater flexibility and precision.

### **Persistent Homology and Topological Summaries**
- **Computing persistence diagrams:** The **compute_persistence** function constructs a Simplex Tree using **Gudhi**, assigning filtration values based on the input variable.
- **Topological summaries (TDA metrics):** The function computes essential TDA summaries for dimension zero, including: 
  - **Total Lifespan (TL):** The sum of persistence intervals. 
  - **Average Lifespan (AL):** The mean lifespan of connected components.  
  - **Total Mid-Lifespan (TML):** The sum of midpoints of persistence intervals.  
  - **Average Mid-Lifespan (AML):** The average of midpoints of persistence intervals.  

### **Efficient Computational Design**
- **Optimized spatial computations:** The class efficiently processes adjacency relationships, even for large datasets.  
- **Integration with Pandas, GeoPandas, and Gudhi:** The framework seamlessly works with popular Python libraries for geospatial and topological data analysis.  
- **Dynamic variable selection:** Users can select any **numerical attribute** to control filtering and sorting.  

These features make the AdjacencySimplex class and **compute_persistence** function powerful tools for geospatial topological data analysis, helping researchers explore spatial connectivity, adjacency structures, and persistent homology in geospatial datasets. Whether for epidemiology, environmental studies, urban planning, or regional connectivity analysis, this framework provides an intuitive and structured approach to **spatial TDA**.

## Citations

If you find **spatial-tda** useful in your research, please consider citing the following paper to support my work. Thank you for your support.

