import math
from typing import List, Tuple

# Global Types
noteTupleDuration = Tuple[str, int, float, int]
noteTuple = Tuple[str, int, float]
frequencyTuple = Tuple[float, float]
# Note tuple has (Note Letter, Octave, Duration(, repetition times))

# Global Variables
currentOctave = 4
shiftDict = {
    "A": 0,
    "A#": 1,
    "Bf": 1,
    "B": 2,
    "C": 3,
    "C#": 4,
    "Df": 4,
    "D": 5,
    "D#": 6,
    "Ef": 6,
    "E": 7,
    "F": 8,
    "F#": 9,
    "Gf": 9,
    "G": 10,
    "G#": 11,
    "Af": 11
}

baseFreq = 440  # A4 is 440
expBase = math.pow(2, 1.0/12)


# Helper functions:
def isFloat(s: str) -> bool:
    return s.replace(".", "").isdigit()


def appendMultipleTimes(l: list, a: any, i: int) -> list:
    c = 0
    nl = l
    while c < i:
        nl.append(a)
        c += 1
    return nl


def lastCharInString(s: str) -> chr:
    return s[len(s)-1]


def getArrayFromFile(fileName: str) -> list:
    with open(fileName, "r") as file:
        return list(map(lambda s: s.replace("\n", ""), file.readlines()))


# Main functions:
class ParseMusic():
    @staticmethod
    def parseNoteString(note: str) -> noteTupleDuration:
        """Takes a string like "2x 3 E5" and parses it into a note tuple.

        Parameters
        ----------
        note: str
            String representation of note.
                e.g. 2x 3 E5 for 2 repetitions of an E in the 5th octave with
                duration 3

        Returns
        -------
        noteTuple
            NoteTuple with information from noteString
                "2x 3 E5" -> (E, 5, 3, 2)

        """

        # TODO: avoid globals
        global currentOctave
        parts = note.split(" ")
        nums = 1
        duration = 1.0
        currIndex = 0
        if(
            len(parts[currIndex]) > 1 and
            isFloat(parts[currIndex][:-1]) and
            parts[currIndex][-1:] == 'x'
        ):
            nums = int(parts[currIndex][:-1])
            currIndex += 1
        if isFloat(parts[currIndex]) and lastCharInString(parts[currIndex]) != 'x':
            duration = float(parts[currIndex])
            currIndex += 1
        noteString = parts[currIndex]
        if isFloat(noteString[len(noteString) - 1]):
            currentOctave = int(noteString[len(noteString) - 1])
            noteString = noteString[:-1]
        return (noteString, currentOctave, duration, nums)

    @staticmethod
    def parseArrayToNotePair(noteArray: List[str]) -> List[List[noteTuple]]:
        """Takes a list of note strings and returns a list of note tuples.

        Parameters
        ----------
        noteArray : List[str]
            List of note strings.
                e.g.
                    [
                        "2x 3 E5",
                        "2 D",
                        "3x C",
                        ...
                    ]

        Returns
        -------
        List[noteTuple]
            Parsed list.
                e.g.
                    [
                        (E, 5, 3, 2),
                        (D, 5, 2, 1),
                        (C, 5, 1, 3),
                        ...
                    ]

        """
        parsedArray = []  # type: List[List[noteTuple]]

        for note in noteArray:
            arr = []
            if "," not in note:
                ns, o, d, n = ParseMusic.parseNoteString(note)
                appendMultipleTimes(parsedArray, [(ns, o, d)], n)
                continue
            else:
                splitArr = note.split(",")
                genDuration = ParseMusic.parseNoteString(splitArr[0])[2]
                for partialNote in splitArr:
                    partialNote = partialNote.strip()
                    ns, o, _, n = ParseMusic.parseNoteString(partialNote)
                    arr.append((ns, o, genDuration))
            parsedArray.append(arr)

        return parsedArray

    @staticmethod
    def noteTupleToFrequency(noteT: noteTuple) -> frequencyTuple:
        """Takes a note tuple and returns a frequency tuple for the note.

        Parameters
        ----------
        notePair : noteTuple
            NoteTuple for note.

        Returns
        -------
        frequencyTuple
            Frequency tuple for note.

        """
        note, octave, duration = noteT
        if note == "_":
            return (0, duration)
        semitoneDiff = (octave-4 - 1)*12 + shiftDict[note]
        # -1 to account for the fact that octaves start at 0.
        roundedFreq = round(baseFreq * math.pow(expBase, semitoneDiff), 2)
        return (roundedFreq, duration)

    @staticmethod
    def fileToFrequency(fileName: str) -> List[List[frequencyTuple]]:
        """Short summary.

        Parameters
        ----------
        fileName : str
            Filename of music file.

        Returns
        -------
        List[List[frequencyTuple]]
            Music file parsed into frequencies.

        """
        arr = getArrayFromFile(fileName)
        np = ParseMusic.parseArrayToNotePair(arr)
        song = []
        for chord in np:
            freqChord = list(map(ParseMusic.noteTupleToFrequency, chord))
            song.append(freqChord)
        return song
