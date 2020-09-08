import numpy as np
from statistics import variance, mean
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('dark_background')


'''
def sign(x):
    if x == 0:
        return 0
    else:
        return -1 if x < 0 else 1
'''

def _iVal(j):
    i = abs(j)
    if i == 0:
        interval = 0
    elif i in (1, 2):
        interval = 1
    elif i in (3, 4):
        interval = 2
    elif i == 5:
        interval = 3
    elif i in (6, 7):
        interval = 4
    elif i in (8, 9):
        interval = 5
    elif i in (10, 11):
        interval = 6
    else:
       interval = 7 + _iVal(i % 12)
    if j < 0:
        interval = 0 - interval
    return interval

'''
def diff(t):
    return [j-i for i, j in zip(t[:-1], t[1:])]
'''

def diff_rest(t):
    diffs = list()
    for i in range(len(t) - 1):
        if t[i] == 0 or t[i+1] == 0:
            continue
        else:
            diffs.append(t[i+1]-t[i])
    return list(map(lambda x: _iVal(x), diffs))


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def plot_per_voice(theD):
    fig, axes = plt.subplots(2, 2, sharex=True)
    fig.suptitle('Analysis')
    sns.lineplot(x="measure", y="modNotes", hue="voice", data=theD, ax=axes[0, 0])
    axes[0, 0].set_title("Distinct Pitch Classes per Measure")
    axes[0, 0].set(xlabel='Measure', ylabel='N Pitch Classes')
    sns.lineplot(x="measure", y="noteRange", hue="voice", data=theD, ax=axes[0, 1])
    axes[0, 1].set_title("Note Range per Measure")
    axes[0, 1].set(xlabel='Measure', ylabel='Note Range (chromatic)')
    sns.lineplot(x="measure", y="averageMagnitude", hue="voice", data=theD, ax=axes[1, 0])
    axes[1, 0].set_title("Mean Interval Magnitudes per Measure")
    axes[1, 0].set(xlabel='Measure', ylabel='Mean Interval Magnitudes')
    sns.lineplot(x="measure", y="averageAbsMagnitude", hue="voice", data=theD, ax=axes[1, 1])
    axes[1, 1].set_title("Mean Absolute Magnitudes per Measure")
    axes[1, 1].set(xlabel='Measure', ylabel='Mean Absolute Interval Magnitudes')

    plt.show()


def analyze(all_music):
    topics = ["voice", "measure", "modNotes", "noteRange", "averageMagnitude", "averageAbsMagnitude"]
    theRealD = {topic:[] for topic in topics}
    voice_names = ["violin_1", "violin_2", "viola", "cello"]
    for piece in all_music:
        for i, voice in enumerate(piece):
            vChunks16 = list(chunks(voice, 16))
            for measure, cell16 in enumerate(vChunks16):
                # rels = list(map(lambda x: _iVal(x), diff(cell16)))
                #'rels = diff_rest(cell16)
                # vDict[voice_names[i]].append(rels)
                # for rel in rels:
                #    theRealD["voice"].append(voice_names[i])
                #    theRealD["measure"].append(measure)
                #    theRealD["rels"].append(rel)
                theRealD["voice"].append(voice_names[i])
                theRealD["measure"].append(measure)
                noZeros = list(filter(lambda x: x != 0, cell16))
                theRealD["modNotes"].append(len(set(map(lambda x: x % 12, noZeros))))
                theRealD["noteRange"].append(max(noZeros) - min(noZeros))
                d = diff_rest(cell16)
                theRealD["averageMagnitude"].append(mean(d))
                theRealD["averageAbsMagnitude"].append(mean(list(map(lambda x: abs(x), d))))

    plot_per_voice(theRealD)
    quit()
    return vDict


def main():
    pass

if __name__ == '__main__':
    main()

'''
within a theme:
    ratio of notes in scale degree

per voice:
    velocity per measure

Inertia

hamming distance with relationship patterns?



https://www.python-course.eu/pandas_DataFrame.php
'''