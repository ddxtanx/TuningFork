import os
import sys
from typing import Tuple

import librosa
import numpy as np
from scipy.io import wavfile
from tools import analysis, parseMusic


def getSPB(bpm: float) -> float:
    bps = bpm/60
    return 1.0/bps


def addList(l1: list, l2: list) -> list:
    if len(l1) != len(l2):
        raise ValueError("Lists must be of Equal Length")
    comb = zip(l1, l2)
    return list(map(lambda t: t[0] + t[1], comb))


def mdArrayAverage(md: list) -> list:
    sumArr = md[0]
    for i in range(1, len(md)):
        sumArr = addList(sumArr, md[i])
    return list(map(lambda v: float(v)/len(md), sumArr))


class TuningFork():
    @staticmethod
    def shiftPitchBy(
                noteArray: np.ndarray,
                sr: int,
                shift: float
                ) -> np.ndarray:
        return librosa.effects.pitch_shift(noteArray, sr, shift)

    @staticmethod
    def speedUpBy(
                noteArray: np.ndarray,
                sr: int,
                factor: float
                ) -> np.ndarray:
        spedUp = librosa.effects.time_stretch(noteArray, factor)
        return spedUp

    @staticmethod
    def speedUpTo(
                noteArray: np.ndarray,
                sr: int,
                shiftTo: float
                ) -> np.ndarray:
        dur = librosa.core.get_duration(noteArray, sr)
        ratio = dur/shiftTo
        spedUp = TuningFork.speedUpBy(noteArray, sr, ratio)
        return spedUp

    @staticmethod
    def pitchTo(
            noteArray: np.ndarray,
            sr: int,
            shiftTo: int,
            bpm: float
            ) -> np.ndarray:
        spb = getSPB(bpm)

        currentFrequency = analysis.startingNote(noteArray, sr)
        freqRatio = shiftTo/float(currentFrequency)
        shift = np.log2(freqRatio)
        shiftedPitchWF = TuningFork.shiftPitchBy(noteArray, sr, 12*shift)
        return TuningFork.speedUpTo(shiftedPitchWF, sr, spb)

    @staticmethod
    def emptyBeatTrack(
            likeList: np.ndarray,
            sr: int,
            bpm: float
            ) -> np.ndarray:
        spb = getSPB(bpm)
        emptyLike = np.full_like(likeList, .01)
        return TuningFork.speedUpTo(emptyLike, sr, spb)

    @staticmethod
    def sampleIntoSong(
            sampleTrack: np.ndarray,
            sr: int,
            frequencyList: list,
            bpm: float
            ) -> np.ndarray:
        song = np.array([])
        for freqList in frequencyList:
            nextParts = []
            for freq, duration in freqList:
                if freq != 0:
                    pitched = TuningFork.pitchTo(sampleTrack, sr, freq, bpm)
                    nextParts.append(pitched)
                else:
                    empty = TuningFork.emptyBeatTrack(sampleTrack, sr, bpm)
                    nextParts.append(empty)
            avgArr = np.array(mdArrayAverage(nextParts))
            spedUpPart = TuningFork.speedUpBy(avgArr, sr, 1.0/duration)
            song = np.concatenate((song, spedUpPart))
        return song

    @staticmethod
    def sampleWAVFileIntoMusic(
                        wavFileName: str,
                        musicFileName: str,
                        bpm: float
                        ) -> Tuple[np.ndarray, int]:
        sr, _ = wavfile.read(wavFileName)
        waveForm, _ = librosa.core.load(wavFileName, sr)

        waveForm, _ = librosa.effects.trim(waveForm)
        freqList = parseMusic.fileToFrequency(musicFileName)

        wP = TuningFork.sampleIntoSong(waveForm, sr, freqList, bpm=bpm)
        return (wP, sr)
