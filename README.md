# Sonasca Midi Player

The aim of this class is to mess up a midi file's playback in a controlled
manner so that the song remains recognisable.

This means that the user may ratchet up and down the wrongness to reflect
external factors.

### Installation

    virtualenv .venv
    . .venv/bin/activate
    pip install mido

    sudo apt-get install libportmidi-dev fluidsynth fluid-soundfont-gm

### Running

In one terminal set up the midi playback environment:

    fluidsynth -a alsa -l --server -i /usr/share/sounds/sf2/FluidR3_GM.sf2

In another:

    . .venv/bin/activate
    python midi/player.py

### Notes on usage

note_adj_frequency represents the interval between notes that are changed,
increasing it will result in fewer mangled notes

note_adj_factor represents the maximum number of semitones that a note can be
adjusted though the actual number is pseudo random up to this limit


