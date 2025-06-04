Terminal Scripting Animations
=============================

This directory contains the tools to generate animated gifs to demonstrate how
to use the andebox tool.

Quickstart
----------

To generate images, do:
```
./setup
make clean all
```

Actual process
--------------

The scripts are the files with the `.pexp` extension, they are parsed by the
`pexp` script (python script based on `pexpect`) to generate `.cast` files,
which are in turn read by `asciinema` and its docker-based companion tool `agg`
to generate the `.gif` files.

This process is not meant to be executed in the CI, mainly because `pexp` will
generate random delays while printing the "typed" characters trying to mimic a
human. That means that every run the cast and the `.gif` files will be
different, even if the scripts remained the same, which is not suitable for the
build process, nor for `git` itself.

Known Issues
------------

This project has been using devcontainers and, in such a context, this image
generation is bumping into two issues:

* Every time `andebox` run it spills a message saying that `vagrant` has not
  been found. Possible solutions: disable that message coming from vagrant, or
  uninstall `python-vagrant` from the poetry venv (that of course will not help
  with tests), actually installing vagrant within the devcontainer (not a good
  choice for obvious reasons, I think.)
* When runing the command `andebox test -- ... --docker default ...` to
  generate the ascii animation, a warning message pops up:
  ```
  WARNING: Unable to detect the network for the current container. Use the `--docker-network` option if containers are unreachable.
  ```
  Not sure yet how get rid of it, but not too worried since it is a minor
  hassle: the execution works fine regardless of that.
