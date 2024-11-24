# Python Scientific Data Tools

A collection of Python modules for handling scientific data formats and visualization, including:
- Starbase tables
- FITS files
- DS9 interface

## Installation

### Requirements
- Python 2.7 or later
- NumPy (optional but recommended)
- Cython (optional, for improved performance)
- DS9 and XPA tools (required for DS9 functionality)

### Building
```bash
make
```
This will build the optional Cython-optimized data reader (`starbase_data.so`).

## Modules

### 1. Starbase

The Starbase module provides a Python interface for reading and writing tabular data in the Starbase format.

#### Basic Usage
```python
from starbase import Starbase

# Read a table from file
tab = Starbase("input.tab", deftype=float)

# Read from a command pipeline
tab = Starbase('| row < input.tab "X > 3"', deftype=int)

# Access data
value = tab[0][0]           # Get value at row 0, col 0
value = tab[1]["Y"]         # Get value at row 1, col "Y"
value = tab[4].Y            # Get value using dot notation

# Iterate over rows
for row in tab:
    print(row)

# Slice rows
for row in tab[0:2]:
    print(row)

# Access column vectors
x_values = tab[:].X         # Get all X values
subset = tab[0:2].X         # Get first two X values

# Create from arrays
new_tab = Starbase.arrays("X", [1, 2, 3], "Y", [3, 4, 5])

# Write to file
tab > "output.tab"
```

### 2. FITS

The FITS module provides tools for reading and writing FITS (Flexible Image Transport System) files.

#### Basic Usage
```python
from fitsy import hdu, fits

# Read a FITS file
headers = fits("image.fits")

# Create a new HDU
import numpy as np
data = np.zeros((100, 100))
new_hdu = hdu(data)

# Write to file
new_hdu.writeto("output.fits")

# Access header information
print(hdu.bitpix)
print(hdu.shape)
```

### 3. DS9

The DS9 module provides a Python interface for interacting with the DS9 astronomical imaging and data visualization application.

#### Basic Usage
```python
from ds9 import ds9

# Create DS9 interface
display = ds9("ds9")

# Load an image
display.file("image.fits")

# Control display
display.frame(2)            # Switch to frame 2
display.zoom(2)             # Set zoom factor
display.panto(1024, 1024)   # Pan to coordinates

# Work with regions
# Draw circles
display.regions([[10, 10], [15, 15], [20, 20]])

# Draw boxes
display.regions([[10, 10, 4], [15, 15, 5], [20, 20, 6]], 
                {'shape': 'box'})

# Draw points
display.regions([[10, 10], [15, 15]], 
                {'shape': 'point', 'point': 'box'})

# Clear regions
display.regions(delete=True)
```

## Features

### Starbase
- Read/write Starbase format tables
- Column-based data access
- Row slicing and iteration
- Command pipeline support
- Optional Cython-optimized data reader
- NumPy array integration
- Custom data type handling

### FITS
- Read/write FITS files
- Header manipulation
- Data scaling support
- Multi-extension FITS support
- Byte-swapping handling
- NumPy array integration

### DS9
- Remote control of DS9 display
- Image loading and frame control
- Pan and zoom operations
- Region manipulation:
  - Circles
  - Boxes
  - Points
  - Lines
  - Ellipses
  - Polygons
  - Text annotations
- Coordinate system support:
  - Image
  - Physical
  - WCS (FK5, etc.)

## Advanced Features

### Starbase Column Types
```python
# Specify column types
tab = Starbase("data.tab", types={
    "x": float,
    "y": int,
    "name": str
})
```

### DS9 Region Styling
```python
# Colored regions with custom attributes
colors = ["red", "green", "blue"]
display.regions(
    [[10, 10, 4, 14, 0], 
     [15, 15, 5, 14, 1], 
     [20, 20, 6, 14, 2]],
    {
        'columns': "x y width height color",
        'shape': 'box',
        'color': lambda c: colors[c]
    }
)
```

## Contributing

Please feel free to submit issues and pull requests on GitHub.

## License

[License information not provided in source files]