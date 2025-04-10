# Function Plotter with Area Calculation

## Overview

This application provides an interactive GUI for plotting mathematical functions and calculating the area under the curve between specified bounds. Designed for both educational and professional use, it combines powerful mathematical computation with an intuitive interface.

## Key Features

### Mathematical Capabilities
- Supports plotting of mathematical expressions using Python syntax
- Includes common functions: `sin`, `cos`, `tan`, `log`, `exp`, `sqrt`, `abs`
- Recognizes mathematical constants: `pi` (π) and `e` (Euler's number)
- Displays formatted mathematical expressions using LaTeX rendering

### Interactive Visualization
- **Dynamic zooming** with mouse wheel (focuses on x-axis expansion)
- **Pan functionality** (click-and-drag to move the graph)
- Clean, modern matplotlib styling with grid lines
- Automatic legend generation with LaTeX-formatted function display

### Area Calculation
- Precise numerical integration between user-defined bounds
- Input validation for boundary conditions (0 ≤ x ≤ 1)
- Clear display of computed area with 4 decimal precision

## Installation

1. Ensure Python 3.7+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python plot_app.py
   ```

## Usage Guide

### Basic Plotting
1. Enter your function in the "Function f(x)" field (e.g., `(4*e)**(-4*x)`)
2. Click "Plot Graph" to visualize your function

### Advanced Controls
- **Mouse wheel**: Adjust x-axis range (zooms rightward)
- **Left-click + drag**: Pan the graph horizontally
- Right-click context menu (planned for future release)

### Area Calculation
1. Set your integration bounds in the "x1" and "x2" fields
2. Click "Calculate Area" to compute and display the result
3. The shaded area will appear on the graph (implementation in progress)

## Technical Details

### Core Technologies
- **Frontend**: Tkinter with ttk widgets for modern styling
- **Math Engine**: SymPy for symbolic computation and LaTeX conversion
- **Plotting**: Matplotlib with interactive backend
- **Rendering**: Pillow for LaTeX formula display

### Architecture
The application follows an MVC-like pattern:
- **Model**: NumPy/SymPy computation backend
- **View**: Tkinter interface with embedded matplotlib canvas
- **Controller**: Event handlers for user interactions

## Roadmap

### Near-term Features (v1.1)
- [ ] Export graphs as PNG/SVG
- [ ] Multiple function plotting
- [ ] Customizable line styles/colors
- [ ] Area visualization (shading under curve)

### Future Development
- [ ] 3D function plotting
- [ ] Derivative/integral visualization
- [ ] CSV data export/import
- [ ] Dark mode support
- [ ] Plugin system for custom functions

## Why This Tool?

Unlike simple graphing calculators, this application offers:
- **Educational value**: See the direct relationship between functions and their integrals
- **Professional utility**: Quick visual verification of mathematical models
- **Research applications**: Prototype mathematical concepts before full implementation

## Contribution

We welcome contributions! Please fork the repository and submit pull requests for:
- Bug fixes
- New features
- Documentation improvements
- Localization support

## Support

For issues or feature requests, please open an issue on GitHub. For educational institutions interested in custom versions, contact the maintainers.

---

*"Mathematics is the language with which God has written the universe." — Galileo Galilei*