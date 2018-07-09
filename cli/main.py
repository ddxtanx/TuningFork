#!/usr/bin/env python3.6

import argparse
import os

import librosa
from tuning_fork import TuningFork


def main() -> None:
    bpm = 100

    parser = argparse.ArgumentParser(
        description='Autotune a wavfile to a .music file'
    )
    parser.add_argument(
        "wavfile",
        type=str,
        help="The path to the wavfile you want to autotune."
    )
    parser.add_argument(
        "musicfile",
        type=str,
        help="The path to the music file you want the wavfile autotuned to."
    )
    parser.add_argument(
        "--bpm",
        dest="bpm",
        action="store",
        type=float,
        default=100,
        help="The bpm you want the song to play at."
    )
    parser.add_argument(
        "--out",
        dest="out",
        action="store",
        type=str,
        default="",
        help="The desired output file."
    )
    parser.add_argument(
        "--play",
        dest="play",
        action="store_true",
        help="Automatically play after wavfile is created."
    )
    args = parser.parse_args()
    filename1 = args.wavfile
    filename2 = args.musicfile
    dir1, name1 = os.path.split(filename1)
    dir2, name2 = os.path.split(filename2)
    name1 = name1.replace(".wav", "")
    name2 = name2.replace(".music", "")

    bpm = args.bpm

    outputFile = args.out
    if outputFile == "":
        outputFile = "{0}_ShiftedTo_{1}.wav".format(name1, name2)

    wP, sr = TuningFork.sampleWAVFileIntoMusic(filename1, filename2, bpm)
    librosa.output.write_wav(outputFile, wP, sr)
    if args.play:
        os.system("play {0}".format(outputFile))


if __name__ == "__main__":
    main()
