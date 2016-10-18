import mido
from mido import MidiFile, MetaMessage
import time
import random




class SonascaPlayer(object):

    _output_port = None
    _note_on_queue = {}
    _note_adj_factor = 0
    _note_adj_counter = 0
    _mangle_enabled = True

    def __init__(self, note_adj_factor=0, note_adj_frequency=10,
                 mangle_enabled=True):
        self._output_port = [
            port for port in mido.get_output_names()
            if 'Synth' in port and 'input' in port][0]
        self._note_on_queue = {}
        self._note_adj_factor = note_adj_factor
        self._note_adj_frequency = note_adj_frequency
        self.note_adj_counter = 0

    def _send_notes(self, notes, output):
        for note in notes:
            if not isinstance(note, MetaMessage):
                output.send(note)

    def _note_muck(self, notes):
        for note in notes:
            if self._mangle_enabled:
                if note.channel != 9:

                    if note.type == 'note_on':
                        self._note_on_queue[
                            '%s,%s' % (note.channel, note.note)] = note
                        if self._should_muck():
                            note.note += random.randint(
                                0, self._note_adj_factor)

                    if note.type == 'note_off':
                        orig_note_on = self._note_on_queue.get(
                            '%s,%s' % (note.channel, note.note))
                        note.note = orig_note_on.note

    def _should_muck(self):
        self._note_adj_counter += 1
        if self._note_adj_counter >= self._note_adj_frequency:
            self._note_adj_counter = 0
            return True
        return False

    def play(self, filename):

        midifile = MidiFile(filename)
        with mido.open_output(self._output_port) as output_to_synth:
            note_cache = []
            for message in midifile:
                if not isinstance(message, MetaMessage):
                    # if message.channel ==4:
                    note_cache.append(message)
                if message.time > 0:
                    self._note_muck(note_cache)
                    self._send_notes(note_cache, output_to_synth)
                    note_cache = []
                    time.sleep(message.time)

    def increase_frequency(self):
        self._note_adj_frequency -= 1
        if self._note_adj_frequency < 0:
            self._note_adj_frequency = 0

    def decrease_frequency(self):
        self._note_adj_frequency += 1
        if self._note_adj_frequency > 10:
            self._note_adj_frequency = 10

    def mangler_enabled(self, mangle_on=True):
        self._mangle_enabled = mangle_on


if __name__ == '__main__':
    sonasca_player = SonascaPlayer(note_adj_factor=4, note_adj_frequency=4)
    sonasca_player.play('resources/tubthumping.mid')
