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

basic install
pw to Iheart
copied in ssh key

echo "blacklist snd_bcm2835" > /etc/modprobe.d/snd-blacklist.conf
sudo apt-get install scons -y
sudo apt-get install python-dev swig -y
  scons in rpi_ws281x
  into "python" dir
     python ./setup.py build
     sudo python ./setup.py install


git clone stormlight-archive
git clone https://github.com/jgarff/rpi_ws281x.git
git

## needed improvements
- joining strands
## cool ideas?

### tool to create an Arrangement using two pi (or other) cams

Twould be cool to set up two cams to get binocular vision and then cycle through lights
one at a time in order to place them "in space".

- would probably need to tell tool geometry of cameras:
  - to each other
  - to a nominal "center" of the arrangement space
- thinking of a christmas tree, it might take multiple scans to get full
  view of the arrangement.

### post-balena new-device notes
#### steps
copyied in authorized_keys to root

first ssh to root saw:
  cp: cannot create regular file '~stuarts/ssh_plus_balena_env_vars': No such file or directory... wahaha????
  root@deep-surf:~# touch ~${DEV_USER}/x
  touch: cannot touch '~stuarts/x': No such file or directory
  root@deep-surf:~# touch ~stuarts/x
  root@deep-surf:~#

Ok, so that's a thing. The ~ expands to 'root'
-- fixed by using /home/${DEV_USER}

first su - stuarts
 -- went into zsh set. ah: /usr/local/stormlight_archive/stormlight_archive/ci/templates/dev_user/setup_dev_user_container_start.sh: No such file or direc
   -- It was named setupdev_user... Fixed.
did deploy.

Next boot, saw:
 stormlight-archive  + ZSH_CUSTOM=/home/nfgsw/.oh-my-zsh/custom
 stormlight-archive  + git clone https://github.com/janjoswig/Ducula.git /home/nfgsw/.oh-my-zsh/custom/themes/Ducula
 stormlight-archive  fatal: could not create leading directories of '/home/nfgsw/.oh-my-zsh/custom/themes/Ducula': Permission denied
 stormlight-archive  cp: cannot stat '/usr/local/stormlight_archive/stormlight_archive/ci/templates/stuarts_user/dot_emacs.template': No such file or directory

fixed nfgsw and trying to pull from DEV_USER in templates
removed everything in /home/stuart
did deploy.

Still not complete zsh...
- looks like something was plopping down a .zshrc? Maybe hacked it to copy ours when installing ohmyzsh.
- custome type for Ducula


Setting up ssh in worker space:
https://github.com/settings/keys
on-target or common:
'ssh-keygen -t ed25519`
