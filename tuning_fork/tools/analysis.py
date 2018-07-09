from typing import List, Tuple, Union

import librosa
import numpy as np
from scipy.io import wavfile

ndarray = np.ndarray
genlist = Union[ndarray, list]


# Helper functions:
def secondsToSamples(seconds: float, sr: int) -> int:
    return int(seconds*sr)


def maxIndex(l: genlist) -> int:
    maxI = 0
    maxVal = l[0]
    for i in range(1, len(l)):
        val = l[i]
        if val > maxVal:
            maxVal = val
            maxI = i
    return maxI


def chunkAverage(l: genlist, chunkSize: int) -> genlist:
    if chunkSize > len(l):
        raise ValueError("ChunkSize must be less than length of list.")
    avgList = []
    currentIndex = 0
    while (currentIndex + chunkSize) < len(l):
        avgList.append(np.mean(l[currentIndex:currentIndex + chunkSize]))
        currentIndex += chunkSize
    avgList.append(np.mean(l[currentIndex:]))
    return avgList


def loadFromFile(fileName: str) -> Tuple[np.ndarray, int]:
    sr, _ = wavfile.read(fileName, "rb")
    wf, _ = librosa.core.load(fileName)
    return (wf, sr)


def getNSecondsFromWaveForm(
        waveForm: np.ndarray,
        sr: int,
        seconds: float
        ) -> np.ndarray:
    return waveForm[:secondsToSamples(seconds, sr)]


# Main functions:
class Analysis():
    @staticmethod
    def condenseToSingleChannel(waveForm: np.ndarray) -> np.ndarray:
        waveFormList = waveForm.tolist()
        if (isinstance(waveFormList[0], list)):
            waveFormSingleChannel = np.array(
                map(lambda l: l[0], waveForm)
            )
        else:
            waveFormSingleChannel = waveForm
        return waveFormSingleChannel

    @staticmethod
    def rfftAudible(waveForm: genlist) -> List:
        fft = np.fft.rfft(waveForm)
        mfft = []
        for n in range(0, len(fft)):
            if n < 150 or n > 3000:
                mfft.append(0)
            else:
                mfft.append(np.sqrt(fft[n].real**2 + fft[n].imag**2))
        return mfft

    @staticmethod
    def startingNote(waveForm: ndarray, sr: int) -> int:
        sc = Analysis.condenseToSingleChannel(waveForm)
        beatSample = getNSecondsFromWaveForm(sc, sr, 1.5)
        trimmed, _ = librosa.effects.trim(beatSample)
        adRFFT = Analysis.rfftAudible(trimmed)
        return maxIndex(adRFFT)

    @staticmethod
    def startingNoteFromFile(fileName: str) -> int:
        waveForm, sr = loadFromFile(fileName)
        return Analysis.startingNote(waveForm, sr)
