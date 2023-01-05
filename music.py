from music21 import midi


class Music:

    def __init__(self, midi_file: str, remove_drums: bool) -> None:
        self.__base_midi = self.__open_midi(midi_file, remove_drums)


    def get_base_midi(self):
        return self.__base_midi


    @staticmethod
    def __open_midi(midi_path: str, remove_drums: bool):
        # There is an one-line method to read MIDIs
        # but to remove the drums we need to manipulate some
        # low level MIDI events.
        mf = midi.MidiFile()
        mf.open(midi_path)
        mf.read()
        mf.close()
        if (remove_drums):
            for i in range(len(mf.tracks)):
                mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]          

        return midi.translate.midiFileToStream(mf)

    def list_instruments(self):
        partStream = self.__base_midi.parts.stream()
        print("List of instruments found on MIDI file:")
        for p in partStream:
            # aux = p
            print (p.partName)