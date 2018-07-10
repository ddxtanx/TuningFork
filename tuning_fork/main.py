from typing import Tuple

import librosa
import numpy as np
import soundfile as sf
from tuning_fork.tools.analysis import Analysis
from tuning_fork.tools.parseMusic import ParseMusic


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


def shiftPitchBy(
            noteArray: np.ndarray,
            sr: int,
            shift: float
            ) -> np.ndarray:
    return librosa.effects.pitch_shift(noteArray, sr, shift)


def speedUpBy(
            noteArray: np.ndarray,
            sr: int,
            factor: float
            ) -> np.ndarray:
    spedUp = librosa.effects.time_stretch(noteArray, factor)
    return spedUp


class TuningFork():
    @staticmethod
    def speedUpTo(
                waveForm: np.ndarray,
                sr: int,
                shiftTo: float
                ) -> np.ndarray:
        """Speeds up waveform to a certain length in seconds.

        Parameters
        ----------
        waveForm : np.ndarray
            waveForm to be sped up.
        sr : int
            Sample rate of waveForm.
        shiftTo : float
            Number of seconds waveForm is shifted to.

        Returns
        -------
        np.ndarray
            waveForm shifted to shiftTo seconds.

        """
        dur = librosa.core.get_duration(waveForm, sr)
        ratio = dur/shiftTo
        spedUp = speedUpBy(waveForm, sr, ratio)
        return spedUp

    @staticmethod
    def pitchTo(
            waveForm: np.ndarray,
            sr: int,
            shiftTo: int,
            bpm: float
            ) -> np.ndarray:
        """Changes the dominant pitch of a waveForm to a specified frequency.

        Parameters
        ----------
        waveForm : np.ndarray
            Same as above.
        sr : int
            Sample rate of waveform.
        shiftTo : int
            Pitch frequency to be shifted to.
        bpm : float
            If you are shifting to fit to a song, this is the bpm of the song.

        Returns
        -------
        np.ndarray
            Description of returned object.

        """
        spb = getSPB(bpm)

        currentFrequency = Analysis.startingNote(waveForm, sr)
        freqRatio = shiftTo/float(currentFrequency)
        shift = np.log2(freqRatio)
        shiftedPitchWF = shiftPitchBy(waveForm, sr, 12*shift)
        return TuningFork.speedUpTo(shiftedPitchWF, sr, spb)

    @staticmethod
    def emptyBeatTrack(
            likeWaveForm: np.ndarray,
            sr: int,
            bpm: float
            ) -> np.ndarray:
        """Creates an (almost) empty track section.

        Used for making rests.
        Parameters
        ----------
        likeWaveForm : np.ndarray
            The waveForm the track should be modelled after.
        sr : int
            The sr of likeWaveForm.
        bpm : float
            Same as bpm from pitchTo.

        Returns
        -------
        np.ndarray
            A silent track similar to likeWaveForm.

        """
        spb = getSPB(bpm)
        emptyLike = np.full_like(likeWaveForm, .01)
        return TuningFork.speedUpTo(emptyLike, sr, spb)

    @staticmethod
    def sampleIntoSong(
            sampleTrack: np.ndarray,
            sr: int,
            frequencyList: list,
            bpm: float
            ) -> np.ndarray:
        """Takes a waveForm and autotunes it to a list of frequencies.

        Parameters
        ----------
        sampleTrack : np.ndarray
            The track to be sampled into the song.
        sr : int
            The sample rate of the sample track.
        frequencyList : list
            The list of frequencies to fit sampleTrack to.
        bpm : float
            Same as other bpm.

        Returns
        -------
        np.ndarray
            A waveform that is sampleTrack fitted to frequencyList.

        """
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
            spedUpPart = speedUpBy(avgArr, sr, 1.0/duration)
            song = np.concatenate((song, spedUpPart))
        return song

    @staticmethod
    def sampleWAVFileIntoMusic(
                        wavFileName: str,
                        musicFileName: str,
                        bpm: float
                        ) -> Tuple[np.ndarray, int]:
        """Wrapper of sampleIntoSong for convienience.

        Parameters
        ----------
        wavFileName : str
            The filename of the wav sample file.
        musicFileName : str
            The filename of the music template file.
        bpm : float
            same as above.

        Returns
        -------
        Tuple[np.ndarray, int]
            A tuple consisting of the fitted song and the sample rate of it.

        """
        waveForm, sr = sf.read(wavFileName)

        waveForm, _ = librosa.effects.trim(waveForm)
        waveForm = Analysis.condenseToSingleChannel(waveForm)
        freqList = ParseMusic.fileToFrequency(musicFileName)

        wP = TuningFork.sampleIntoSong(waveForm, sr, freqList, bpm=bpm)
        return (wP, sr)
