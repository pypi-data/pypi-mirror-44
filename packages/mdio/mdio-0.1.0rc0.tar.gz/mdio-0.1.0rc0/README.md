# mdio

A library of simple I/O routines for MD trajectory formats.

*mdio* is designed to provide basic MD file I/O capabilities. It's not supposed
to replace great packages like *mdtraj* and *mdanalysis*, but may be useful
when all you need is basic MD trajectory file I/O and nothing much more.

Currently mdio supports reading and writing dcd, xtc, and Amber netcdf (.nc) format files.

## Installation:

Easiest via pip:

```
% pip install mdio
```

## Usage:

*mdio* provides three basic functions: *xtc_open()*, *dcd_open()*, and *nc_open()*. Reading and writing is done via *Frame* objects that
wrap the key data (coordinates, box info, timepoint). 

**Be aware:** *mdio* makes no assumptions about units - it's up to the user to
provide data in angstroms or nanometers, etc., as required.


### Example 1: reading a dcd format file:
```
from mdio.dcdio import dcd_open

f = dcd_open('mydcdfile.dcd') # default is to open in "read" mode
frame = f.read_frame() # returns a frame object
coordinates = frame.crds # an [N, 3] numpy array
box = frame.box # a [3,3] numpy array
time = frame.time # time point (float) - in whatever units the dcd file used.

while frame is not None:
    frame = f.read_frame() # returns None at the end of the file
f.close()

```

### Example 2: writing a .nc format file:

```
from mdio.ncio import nc_open
from mdio.base import Frame
import numpy as np

natoms = 100
crds = np.random.rand(natoms, 3)
box = np.identity(3) * 40.0
time = 1.0

myframe = Frame(crds, box=box, time=time) # crds is the only mandatory argument; box can be None and time defaults to 1.0
with nc_open('myncfile.nc', 'w') as f: # context managers supported
    f.write_frame(frame)
	
```

### Example 3: reading an xtc format file:

Xtc format files are handled analogously to dcd and nc format ones, but in addition it is possible to restrict reading 
to an initial subset of all the atoms (e.g. maybe the trajectory is of a solvated system of a total of 10,000 atoms, but
the solute is just the first 200 atoms). This can increase reading performance considerably. This option is not available
for dcd and nc files as it provides no performance boost.

```
from mdio.xtcio import xtc_open
import numpy as np

first_atoms = 56 # Imagine we are only interested in the first 56 atoms in each snapshot
nframes = 10 # Imagine we only want the first 10 frames in the trajectory
trajectory = np.zeros((nframes, first_atoms, 3))

with xtc_open('myxtcfile.xtc') as f:
     for i in range(nframes):
	     frame = f.read_frame(natoms=first_atoms)
		 trajectory[i] = frame.crds
```

## Author:

Charlie Laughton charles.laughton@nottingham.ac.uk

## License:

BSD 3-clause
