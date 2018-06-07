# stormlight-archive
play light control system


To setup to run w/o draguino:
grab http://www.vtk.org/files/release/7.0/vtkpython-7.0.0-Darwin-64bit.dmg
open disk image
drop 'vtkPython' from image to this directory. An 'ls' should show something like:
LICENSE        activate       src
README.md      capture        vtkpython

Then "source ./activate"
cd src
vtkpython main.py --display=sim

todo: update for other platforms!

# design-ish notes
Goals;
* be able to test off-real-thing

So that means the "main" needs a flag to say "be fake"
- pass in ArdiunoThingy (fake or real)
- IT should contain LEDs and such.
- plugins for algos?

Api for "strand":
  init(count, l0x, l0y, l0z)

  set(led#, r, g, b)
  clear(led#)
  getpos(led#) -> x, y, z


time-baed-things:
  firefly
    bouncing-in-strand
    wrapping-on-strand
    ??? len, dx, dy, edge-action ???

Firefly is (a set of) moving pixels. Fixed color/intensity.
Flames are unmoving pixels, but with "moving" colors/intensity.

route-1: api to add/delete moving pixels.
 + local-proc does the tics
 + can modify on the fly?
 - dynamic motion/color sources?
   ? some in-code (random #, etc)
   ? code "in-code" sensors?
   ? code "in-code" web-access
   ? could make it so one could alter the generators


route-2: 