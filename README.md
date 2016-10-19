# Sonasca Midi Player

The aim of this class is to mess up a midi file's playback in a controlled
manner so that the song remains recognisable.

This means that the user may ratchet up and down the wrongness to reflect
external factors.

### Installation

    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt

    sudo apt-get install libportmidi-dev fluidsynth fluid-soundfont-gm

### Running

In one terminal set up the midi playback environment:

    fluidsynth -a alsa -l --server -i /usr/share/sounds/sf2/FluidR3_GM.sf2

In another:

    . .venv/bin/activate
    python midi/player.py

### Notes on usage

SonascaPlayer accepts a mangle factor between 0 and 10.  0 means no mangling is
done, 10 meaning every note is mangled excepting (on the example midi file) the
rhythm track notes.

It's necessary to set the SonsacaPlayer instance up executing play() on a
thread if it is required that the mangle factor be manipulated during playback.
The player.py module has an example usage implemented if executed as __main__.


