# Installation/Requirements

All requirements are in requirements.txt. They are numpy for array manipulations, librosa for audio processing, and scipy for it's wavefile export.

Installation, currently, is all via github. To download the cli tool run

    pip3.6 install tuning-fork-cli

or, if you just want the Python Library Code, run

    pip3.6 install tuning-fork

This project does require python3.6 since I use mypy annotations to help me out.

# CLI Usage

You need two things to run this program effectively: a sampled wavefile and a .music file.

To sample the wavefile into the .music run

    tuning-fork (wavfile) (musicfile) ((bpm))

The bpm is optional, and specifying it will set the samplefile's length to be consistent with the bpm. BPM is automatically 100

# Python Usage

To import the entire package just include

    import tuning_fork ((as tf))

in your imports and all code will be loaded!

`tuning_fork` itself contains methods for pitch shifting, so, to shift a wav to a .music, you can run

    tf.sampleWAVFileIntoMusic("wavfilename", "musicfilename", (bpm))

and that will return a librosa style ndarray that represents the WAV encoding of the autotuned song.

Along with normal functions, `tuning_fork` also exposes analysis and parseMusic.

* analysis
  * Deals with the analysis of a wavfile.
  * Most useful exports are `startingNote` and `startingNoteFromFile`
    * These methods take in some reference to a wavfile (depending on the function) and returns the approximate starting note frequency of the song.

* parseMusic
  * Deals with parsing .music files
  * Fairly useful all around, take a look around the source or the `help(parseMusic)` to find what will fit you!
