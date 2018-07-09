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
        """Condenses multi-channel waveforms down to one channel.

        This is done by taking the first channel value, no other black magic.
        Parameters
        ----------
        waveForm : np.ndarray
            A waveform that might be multi channel.

        Returns
        -------
        np.ndarray
            The waveform condensed to a single channel.

        """
        waveFormList = waveForm.tolist()
        if (isinstance(waveFormList[0], list)):
            waveFormSingleChannel = np.array(
                map(lambda l: l[0], waveForm)
            )
        else:
            waveFormSingleChannel = waveForm
        return waveFormSingleChannel

    @staticmethod
    def rfftAudible(waveForm: np.ndarray) -> np.ndarray:
        """Take a (real-valued) Fast Fourier transform of a waveform.

        Parameters
        ----------
        waveForm : np.ndarray
            Single Channel waveform.

        Returns
        -------
        np.ndarray
            waveForm transformed into the (audible) frequency domain.
        """
        fft = np.fft.rfft(waveForm)
        mfft = list(
            filter(
                lambda x: (x >= 200) and (x <= 2000)
            ),
            fft
        )
        return np.array(mfft)

    @staticmethod
    def startingNote(waveForm: ndarray, sr: int) -> int:
        """Get's the starting note of a waveform.

        Parameters
        ----------
        waveForm : ndarray
            Any ol' waveform.
        sr : int
            Sample rate of the waveform.

        Returns
        -------
        int
            The most dominant frequency of waveForm in the first 1.5 seconds.

        """
        sc = Analysis.condenseToSingleChannel(waveForm)
        beatSample = getNSecondsFromWaveForm(sc, sr, 1.5)
        trimmed, _ = librosa.effects.trim(beatSample)
        adRFFT = Analysis.rfftAudible(trimmed)
        return maxIndex(adRFFT)

    @staticmethod
    def startingNoteFromFile(fileName: str) -> int:
        """Convienient wrapper for startingNote to load file automatically.

        For more info see startingNote
        Parameters
        ----------
        fileName : str
            fileName of wavFile.

        Returns
        -------
        int
            Dominant frequency present in fileName.

        """
        waveForm, sr = loadFromFile(fileName)
        return Analysis.startingNote(waveForm, sr)
