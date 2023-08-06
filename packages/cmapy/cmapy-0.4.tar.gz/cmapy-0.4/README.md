# cmapy

Use Matplotlib colormaps with OpenCV in Python.

Matplotlib provides a lot of [nice colormaps](https://matplotlib.org/tutorials/colors/colormaps.html). Cmapy exposes these colormaps as lists of colors that can be used with OpenCV to colorize images or for other drawing tasks in Python.

| Original image | ![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/examples/imgs/gradient.png) | ![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/examples/imgs/jupiter.png) | ![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/examples/imgs/woman.png) |
| -- | -- | -- | -- |
|viridis|![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/docs/imgs/gradient_viridis.png)|![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/docs/imgs/jupiter_viridis.png)|![](https://gitlab.com/cvejarano-oss/cmapy/raw/master/docs/imgs/woman_viridis.png)|

See all of the available colormaps as of Matplotlib 2.2.3 in this [all colormaps example](https://gitlab.com/cvejarano-oss/cmapy/blob/master/docs/colorize_all_examples.md).

## Requirements

* Python 2.7 or 3.
* Matplotlib.
* OpenCV >= 3.3.0 (to use cv2.applyColorMap()).

## Installation

Python 2.7, with pip:

```bash
pip install cmapy
```

Python 3.x, with pip:

```bash
pip3 install cmapy
```

Or, in a Conda environment:

```bash
conda install -c conda-forge cmapy 
```

## How to use

### Colorize images

Colorize means to apply a colormap to an image. This is done by getting the colormap
with cmapy.cmap() and then applying cv2.applyColorMap(), like this:

```python
img_colorized = cv2.applyColorMap(img, cmapy.cmap('viridis'))
```

Alternatively, you can use cmapy.colorize() directly:

```python
img_colorized = cmapy.colorize(img, 'viridis')
```

See the full [colorize example](https://gitlab.com/cvejarano-oss/cmapy/blob/master/examples/colorize.py).

### Draw with colors

Use the cmapy.color() function and an index between 0 and 255 to get a color 
from a colormap. Cmapy.color() returns a list of BGR (or RGB) values that can be
used with OpenCV drawing functions.

```python
# Get color in BGR order (default) by index.
bgr_color = cmapy.color('viridis', 127)

# Get color in RGB order with a float value.
rgb_color = cmapy.color('viridis', 0.5, rgb_order=True)
```

See a complete [drawing with colors example](https://gitlab.com/cvejarano-oss/cmapy/blob/master/examples/draw_with_colors.py).
