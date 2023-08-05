# ShpWay: A Shapefile Navigator

ShpWay is a simple Python library that converts shapefiles into a navigation system by the conversion of shapefiles to graph.


## Getting Started

### Requirements

* Python 2.7+
* Two shapefiles
    - a shapefile containing _**polyline**_ shapes to outline the pathways
    - a shapefile containing all potential visitation objects _**polygon shapes is currently only supported**_

### Installation

ShpWay can be installed with pip:

```
$ pip install shp-way-bbrownrichardson
```

or directly from the source code:

```
$ git clone https://github.com/bbrownrichardson/ShpWay.git
$ cd ShpWay
$ python setup.py install
```

### Basic Usage
The usage of the library's interface is simple.

```python
from shp_way.shapefile_navigator import ShapefileNavigator

pathways = "shapefiles/roads.shp"
visitation = "shapefiles/buildings.shp"

sn = ShapefileNavigator(pathways, visitation)
```

ShpWay allows users to have control of efficiency in terms of determining spatial grid size. Users can provide a fixed value for the number of rows and columns used in the conversion process. See documentation for more information.

```python
from shp_way.shapefile_navigator import ShapefileNavigator

pathways = "shapefiles/roads.shp"
visitation = "shapefiles/buildings.shp"

sn = ShapefileNavigator(pathways, visitation, rows=15, cols=30)
```

The `sn` object can then be used as described in the `ShpWay-ShapefileNavigator` docs [link here]
