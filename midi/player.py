import mido
from mido import MidiFile, MetaMessage
import time
import random
import threading


class SonascaPlayer(object):

    _output_port = None
    _note_on_queue = {}
    _note_adj_factor = 0
    _note_adj_counter = 0
    _mangle_enabled = False

    def __init__(self, note_adj_factor=0, note_adj_frequency=10):
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

    def _process_notes(self, notes):
        for note in notes:
                if note.channel != 9:
                    self._mangle_note(note)

    def _mangle_note(self, note):
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
        if self._mangle_enabled:
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
                    self._process_notes(note_cache)
                    self._send_notes(note_cache, output_to_synth)
                    note_cache = []
                    time.sleep(message.time)

    def set_mangle_factor(self, mangle_factor=0):
        print "Mangle factor to be set to %s" % mangle_factor
        if mangle_factor not in range(0, 11):
            raise Exception('Mangle factor required between 0 and 10')
        if mangle_factor == 0:
            self._mangle_enabled = False
        else:
            self._mangle_enabled = True
            self._note_adj_frequency = 11 - mangle_factor


if __name__ == '__main__':

    sonasca_player = SonascaPlayer(note_adj_factor=4, note_adj_frequency=10)

    play_thread = threading.Thread(target=sonasca_player.play, args=('resources/tubthumping.mid',))
    play_thread.start()
    for i in range(1, 11):
        print "i = %s" % i
        sonasca_player.set_mangle_factor(mangle_factor=i)
        print "Mangler enabled = %s, note adj frequency to 1 in %s" % (
            sonasca_player._mangle_enabled, sonasca_player._note_adj_frequency)
        time.sleep(2)
    time.sleep(15)
    for i in range(1, 11):
        print "i = %s" % i
        sonasca_player.set_mangle_factor(mangle_factor=(10 - i))
        print "Mangler enabled = %s, note adj frequency to 1 in %s" % (
            sonasca_player._mangle_enabled, sonasca_player._note_adj_frequency)
        time.sleep(2)
    play_thread.join()
