#!/usr/bin/env python3.6

import os
import sys

import librosa
from tuning_fork import TuningFork


def main() -> None:
    bpm = 100

    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    dir1, name1 = os.path.split(filename1)
    dir2, name2 = os.path.split(filename2)
    name1 = name1.replace(".wav", "")
    name2 = name2.replace(".music", "")

    if len(sys.argv) > 3:
        bpm = int(sys.argv[3])

    wP, sr = TuningFork.sampleWAVFileIntoMusic(filename1, filename2, bpm)
    librosa.output.write_wav("{0}_ShiftedTo_{1}.wav".format(name1, name2), wP, sr)
    os.system("play {0}_ShiftedTo_{1}.wav".format(name1, name2))

if __name__ == "__main__":
    main()
