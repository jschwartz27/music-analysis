from music21 import note, chord, pitch
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


class Visualize:

    def __init__(self, base_midi) -> None:
        self.base_midi = base_midi

    def visualize(self):
        self.__print_parts_countour(self.base_midi.measures(0, 6))
        self.base_midi.plot('histogram', 'pitchClass', 'count')
        self.base_midi.plot('scatter', 'offset', 'pitchClass')

    def __extract_notes(self, midi_part):
        parent_element = list()
        ret = list()
        for nt in midi_part.flat.notes:        
            if isinstance(nt, note.Note):
                ret.append(max(0.0, nt.pitch.ps))
                parent_element.append(nt)
            elif isinstance(nt, chord.Chord):
                for pitch in nt.pitches:
                    ret.append(max(0.0, pitch.ps))
                    parent_element.append(nt)
        
        return ret, parent_element

    def __print_parts_countour(self, midi):
        # plt.style.use('dark_background')
        fig = plt.figure(figsize=(12, 5))
        ax = fig.add_subplot(1, 1, 1)
        minPitch = pitch.Pitch('C10').ps
        maxPitch = 0
        xMax = 0

        # Drawing notes.
        for i in range(len(midi.parts)):
            top = midi.parts[i].flat.notes                  
            y, parent_element = self.__extract_notes(top)
            if (len(y) < 1): continue
                
            x = [n.offset for n in parent_element]
            ax.scatter(x, y, alpha=0.6, s=7)
            
            aux = min(y)
            if (aux < minPitch): minPitch = aux
                
            aux = max(y)
            if (aux > maxPitch): maxPitch = aux
                
            aux = max(x)
            if (aux > xMax): xMax = aux
        
        for i in range(1, 10):
            linePitch = pitch.Pitch('C{0}'.format(i)).ps
            if (linePitch > minPitch and linePitch < maxPitch):
                ax.add_line(mlines.Line2D([0, xMax], [linePitch, linePitch], color='red', alpha=0.3))            

        plt.ylabel("Note index (each octave has 12 notes)")
        plt.xlabel("Number of quarter notes (beats)")
        plt.title('Voices motion approximation, each color is a different instrument, red lines show each octave')
        plt.show()