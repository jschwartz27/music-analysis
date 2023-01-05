from music import Music
from visiualize import Visualize


def main():
    music = Music(midi_file="bwv1041b.mid", remove_drums=True)
    music.list_instruments()
    Visualize(music.get_base_midi()).visualize()


if __name__ == "__main__":
    main()
