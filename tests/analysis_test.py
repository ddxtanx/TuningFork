import math
import unittest

import librosa
import numpy as np
from tuning_fork.tools.analysis import Analysis

waveFormBach, _ = librosa.core.load("../examples/WavFiles/Bach.wav")
waveFormC, sr = librosa.core.load("../examples/WavFiles/C.wav")


class TestAnalysisMethods(unittest.TestCase):
    def test_single_channel(self):
        sc = Analysis.condenseToSingleChannel(waveFormBach)
        self.assertIsInstance(np.asscalar(sc[0]), float, "Single Channel")

    def test_starting_note_from_wav(self):
        experimentalFreq = Analysis.startingNote(waveFormC, sr)
        actualFreq = 261.1
        error = math.fabs(actualFreq - experimentalFreq)
        self.assertLessEqual(error, 15, "Starting Note Wav")

    def test_starting_note_from_file(self):
        experimentalFreq = Analysis.startingNoteFromFile(
            "../examples/WavFiles/C.wav"
        )
        actualFreq = 261.1
        error = math.fabs(actualFreq - experimentalFreq)
        self.assertLessEqual(error, 15, "Starting Note File")


if __name__ == "__main__":
    unittest.main()
