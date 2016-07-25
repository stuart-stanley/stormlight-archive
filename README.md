# stormlight-archive
play light control system

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