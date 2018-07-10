import math
import unittest

import librosa
from tuning_fork import TuningFork
from tuning_fork.tools.analysis import Analysis

wav1, sr1 = librosa.core.load("../examples/WavFiles/Bach.wav")
wav2, sr2 = librosa.core.load("../examples/WavFiles/C.wav")


class TuningForkTest(unittest.TestCase):
    def test_speed_up_to(self) -> None:
        spedUp = TuningFork.speedUpTo(wav1, sr1, 1.5)
        self.assertEqual(
            round(librosa.core.get_duration(spedUp, sr1), 1),
            1.5,
            "Duration"
        )

    def test_pitch_shift(self) -> None:
        pitched = TuningFork.pitchTo(wav2, sr2, 500, 120)
        note = Analysis.startingNote(pitched, sr2)
        error = math.fabs(note - 500)
        self.assertLessEqual(error, 20, "Pitch Shift")

    def test_sample_wavfile_into_music(self) -> None:
        musicFile = "../examples/MusicFiles/Scales.music"
        TuningFork.sampleWAVFileIntoMusic(
            "../examples/WavFiles/C.wav",
            musicFile,
            120
        )


if __name__ == "__main__":
    unittest.main()
