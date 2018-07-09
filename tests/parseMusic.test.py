import unittest

from tuning_fork import parseMusic


class ParseMusicTest(unittest.TestCase):
    def test_parse_note_string(self):
        noteString1 = "2x 3 C4"
        expNoteTuple1 = parseMusic.parseNoteString(noteString1)
        actNoteTuple1 = ("C", 4, 3, 2)
        self.assertTupleEqual(expNoteTuple1, actNoteTuple1, "Parse String 1")

        noteString2 = "G"
        expNoteTuple2 = parseMusic.parseNoteString(noteString2)
        actNoteTuple2 = ("G", 4, 1, 1)
        self.assertTupleEqual(expNoteTuple2, actNoteTuple2, "Parse String 2")

        noteString3 = "1x 1.4 A#7"
        expNoteTuple3 = parseMusic.parseNoteString(noteString3)
        actNoteTuple3 = ("A#", 7, 1.4, 1)
        self.assertTupleEqual(expNoteTuple3, actNoteTuple3, "Parse String 3")

    def test_parse_array_to_note_pair(self):
        stringArr1 = [
            "2x 3 C4",
            "G",
            "1x 1.4 A#7"
        ]
        expArr1 = parseMusic.parseArrayToNotePair(stringArr1)
        actArr1 = [
            [("C", 4, 3)],
            [("C", 4, 3)],
            [("G", 4, 1)],
            [("A#", 7, 1.4)]
        ]
        self.assertListEqual(expArr1, actArr1, "Parse List 1")

        stringArr2 = [
            "2 C#5, C4, Bf3",
            "_",
            "A1, A2, A3, A4, A5"
        ]
        expArr2 = parseMusic.parseArrayToNotePair(stringArr2)
        actArr2 = [
            [("C#", 5, 2), ("C", 4, 2), ("Bf", 3, 2)],
            [("_", 3, 1)],
            [("A", 1, 1), ("A", 2, 1), ("A", 3, 1), ("A", 4, 1), ("A", 5, 1)]
        ]
        self.assertListEqual(expArr2, actArr2, "Parse Arr 2")

    def test_note_tuple_to_frequency(self):
        noteTuple1 = ("C", 4, 1)
        expFreq1 = parseMusic.noteTupleToFrequency(noteTuple1)
        actFreq1 = (261.63, 1)
        self.assertAlmostEqual(expFreq1[0], actFreq1[0], places=2, msg="Freq 1")
        self.assertEqual(expFreq1[1], actFreq1[1], "Duration 1")

        noteTuple2 = ("D#", 7, 2)
        expFreq2 = parseMusic.noteTupleToFrequency(noteTuple2)
        actFreq2 = (2489.02, 2)
        self.assertAlmostEqual(expFreq2[0], actFreq2[0], places=2, msg="Freq 2")
        self.assertEqual(expFreq2[1], actFreq2[1], "Duration 2")

        noteTuple3 = ("_", 100, 4)
        expFreq3 = parseMusic.noteTupleToFrequency(noteTuple3)
        actFreq3 = (0, 4)
        self.assertTupleEqual(expFreq3, actFreq3, "Empty Note")

    def test_parse_file(self):
        filename = "../examples/TestSong.music"
        expParsed = parseMusic.fileToFrequency(filename)
        actParsed = [
            [(261.63, 1)],
            [(293.67, 1)],
            [(293.67, 1)],
            [(69.30, 2), (2489.02, 2), (55.00, 2)],
            [(0, 1)],
            [(0, 2)]
        ]
        self.assertListEqual(expParsed, actParsed, "Parse File")


if __name__ == "__main__":
    unittest.main()
