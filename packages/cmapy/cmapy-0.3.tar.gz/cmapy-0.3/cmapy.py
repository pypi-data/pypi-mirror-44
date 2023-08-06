#!/usr/bin/env python
"""Exposes Matplotlib's colormaps so they can be used with OpenCV."""

import matplotlib.cm
import numpy as np
import cv2
import functools
import sys

# This colormap list code has been adapted from:
# https://matplotlib.org/tutorials/colors/colormaps.html
# It is useful to have colormaps grouped by categories.
cmap_groups = [
    {'name': 'Perceptually Uniform Sequential',
    'short_name': 'pu_sequential',
    'colormaps': [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis']},

    {'name':  'Sequential',
    'short_name': 'sequential',
    'colormaps': [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']},

    {'name': 'Sequential (2)',
    'short_name': 'sequential_2',
    'colormaps': [
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']},

    {'name': 'Diverging',
    'short_name': 'diverging',
    'colormaps': [
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
        'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']},

    {'name': 'Qualitative',
    'short_name': 'qualitative',
    'colormaps': ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                  'Dark2', 'Set1', 'Set2', 'Set3',
                  'tab10', 'tab20', 'tab20b', 'tab20c']},

    {'name':  'Miscellaneous',
    'short_name': 'miscellaneous',
    'colormaps': [
        'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
        'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
        'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']}]

# Add the _r versions (reverse colormaps).
for group_data in cmap_groups:
    group_data['colormaps'] += [s + '_r' for s in group_data['colormaps']]


def cmap(cmap_name, rgb_order=False):
    """Extract colormap color information as a LUT
    compatible with cv2.applyColormap(). Default channel order is BGR."""

    c_map = matplotlib.cm.get_cmap(cmap_name, 256)
    rgba_data = matplotlib.cm.ScalarMappable(cmap=c_map).to_rgba(np.arange(0, 1.0, 1.0 / 256.0), bytes=True)
    rgba_data = rgba_data[:, 0:-1].reshape((256, 1, 3))

    # Convert to BGR (or RGB), uint8, for OpenCV.
    cmap = np.zeros((256, 1, 3), np.uint8)

    if not rgb_order :
        cmap[:, :, :] = rgba_data[:, :, ::-1]
    else:
        cmap[:, :, :] = rgba_data[:, :, :]

    return cmap


# If python 3, redefine cmap() to use lru_cache.
if sys.version_info > (3, 0):
    cmap = functools.lru_cache(maxsize=200)(cmap)


def color(cmap_name, val, rgb_order=False):
    """Returns the i-th color of a given colormap as a list of 3 BGR or RGB values.
    Integer values are supposed to be between 0 and 255, float values between 0.0 and 1.0.
    """

    # Float values: scale from 0-1 to 0-255.
    if isinstance(val, float):
        val = round(min(max(val, 0.0), 1.0) * 255)
    else:
        val = min(max(val, 0), 255)

    # Get colormap and extract color.
    colormap = cmap(cmap_name, rgb_order)
    return colormap[val, 0, :].tolist()


def colorize(image, cmap_name):
    """Colorize an image with a colormap."""

    return cv2.applyColorMap(image, cmap(cmap_name))