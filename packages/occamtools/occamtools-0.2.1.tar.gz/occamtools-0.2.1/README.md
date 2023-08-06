OccamTools 
&middot;
[![Build Status](https://travis-ci.com/mortele/OccamTools.svg?token=81VUNKkUYjZSicZzs1NR&branch=master)](https://travis-ci.com/mortele/OccamTools) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/b91377a289bc42868314310dd6be2b60)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mortele/OccamTools&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/mortele/OccamTools/branch/master/graph/badge.svg?token=IXlriBpSwo)](https://codecov.io/gh/mortele/OccamTools) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![PyPI version](https://badge.fury.io/py/occamtools.svg)](https://badge.fury.io/py/occamtools)
=========
Analysis and synthesis tools for [OCCAM](#OCCAM) molecular dynamics/hybrid particle-field simulations.

Input to [OCCAM](#OCCAM) consists mainly of three file types; `fort.1` (simulation metadata), `fort.3` (particle and bond parameters), and `fort.5` (positions and bond structure). The output from the run is a `fort.8` file, adhering to the [`.xyz`](https://en.wikipedia.org/wiki/XYZ_file_format) file format. The `occamtools` python package provides a reader for these file formats (both input and output) and generates a single object containing all the information about the simulation, making analysis of simulation runs and comparison between runs easier. 

Installation
---------
Install by (requires **python >= 3.7**)
```bash
> pip install occamtools
```

Usage
---------
**Loading data**
&middot;
Loading simulation data is done by
```python
import numpy as np
from occamtools import OccamData

data = OccamData('your/file/or/directory/here')
```
where the `data` object now holds all information about the simulation run, e.g. print what kinds of particles a simulation consists of 
```python 
print('Simulation consists of...')
for type_name in data.type_dict:
    num_type = sum(data.type == data.type_dict[type_name])
    print(f'  - {num_type} particles of type {type_name}')

# Simulation consists of...
#   - 400 particles of type H
#   - 100 particles of type C
#   - 250 particles of type Ar
#   ...
```
or make a simple plot of particles in a section of the simulation box diffusing (requires `pip install asciichartpy`)
```python
from asciichartpy import plot

indices = (data.x[0, :] > 20.0) & (data.x[0, :] < 25.0)
diffused = data.x[-1, indices]
bins, hist = np.histogram(diffused)
print(plot(bins.tolist(), hist.tolist()))

# 9.00  ┤  ╭─╮
# 8.00  ┤  │ ╰╮
# 7.00  ┤  │  │
# 6.00  ┤ ╭╯  ╰╮
# 5.00  ┤ │    ╰╮
# 4.00  ┤ │     │
# 3.00  ┤╭╯     │
# 2.00  ┤│      ╰╮
# 1.00  ┼╯       ╰
```
or plot the deviations of the total kinetic energy from the mean over the simulation run (again requires `pip install asciichartpy`)
```python
kinetic_energy_deviations = data.kinetic_energy - np.mean(data.kinetic_energy)
print(plot(kinetic_energy_deviations.tolist()))

#  60.53  ┤            ╭╮
#  50.62  ┤            ││  ╭╮╭╮
#  40.71  ┤            ││  ││││              ╭╮
#  30.81  ┤            ││  ││││              ││     ╭╮    ╭─
#  20.90  ┤ ╭╮         ││  ││││    ╭─╮       ││     ││    │
#  10.99  ┤ ││ ╭─╮ ╭╮ ╭╯│  ││││╭╮  │ │ ╭╮    ││     ││    │
#  10.09  ┤ ││ │ │ ││ │ │  │││││╰╮ │ ╰╮││    ││ ╭╮  ││╭╮╭╮│
#   0.18  ┼╮││ │ │ ││ │ ╰╮ │││╰╯ │ │  ╰╯│╭╮  │╰╮││╭╮│││││││
# -00.73  ┤│││ │ │ ││ │  ╰─╯││   │╭╯    ││╰──╯ ╰╯││││││││││
# -10.64  ┤│││╭╯ │ ││╭╯     ││   ││     ╰╯       ││││││││╰╯
# -20.54  ┤││╰╯  │ │╰╯      ╰╯   ╰╯              ││││││╰╯
# -30.45  ┤╰╯    ╰─╯                             ││││╰╯
# -40.36  ┤                                      ││││
# -50.26  ┤                                      ││╰╯
# -60.17  ┤                                      ╰╯
```

**File storage**
&middot;
Behind the scenes, `.npy` (for numpy arrays) and `.json` (for anything else) files are used to represent the simulation data. By default, loading a simulation run causes the saving of small (relative to the original `fort.5/7/8`) binary files containing the data. These are used to load from on subsequent calls. This means calls to `OccamData.load('your/file/here')` of `OccamData('your/file/here')` will be significantly faster *after* the first call. In this specific example, a 25x speedup is achieved (but your mileage may vary).
![load example](https://i.imgur.com/Wssbx9B.gif)

OCCAM
---------
OCCAM is a program for Molecular Dynamics Simulations able to perform Hybrid Particle-Field (PF) Theoretical Molecular Dynamics simulations. This recent PF technique combines molecular dynamics (MD) and self consistent field theory (SCF). [Read more.](http://www.occammd.org/about/)

[![occam-website](http://www.occammd.org/wp-content/uploads/2018/08/cropped-Untitled-2-01-2.png)](http://www.occammd.org/)