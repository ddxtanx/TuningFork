import math
import unittest
from numbers import Number

import librosa
import numpy as np
import tuning_fork

analysis = tuning_fork.analysis

waveFormBach, _ = librosa.core.load("../examples/Bach.wav")
waveFormC, sr = librosa.core.load("../examples/C.wav")


class TestAnalysisMethods(unittest.TestCase):
    def test_single_channel(self):
        sc = analysis.condenseToSingleChannel(waveFormBach)
        self.assertIsInstance(np.asscalar(sc[0]), float, "Single Channel")

    def test_starting_note_from_wav(self):
        experimentalFreq = analysis.startingNote(waveFormC, sr)
        actualFreq = 261.1
        error = math.fabs(actualFreq - experimentalFreq)
        self.assertLessEqual(error, 15, "Starting Note")

    def test_starting_note_from_file(self):
        experimentalFreq = analysis.startingNoteFromFile("../examples/C.wav")
        actualFreq = 261.1
        error = math.fabs(actualFreq - experimentalFreq)
        self.assertLessEqual(error, 15, "Starting Note")

if __name__ == "__main__":
    unittest.main()
