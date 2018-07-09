# Installation/Requirements

All requirements are in requirements.txt. They are numpy for array manipulations, librosa for audio processing, and scipy for it's wavefile export.

Installation, currently, is all via github. To download the code simply run

    git clone https://github.com/ddxtanx/TuningFork.git

  in your favourite directory. To install all requirements, just run

      pip3.6 install -r requirements.txt

  This project does require python3.6 since I use mypy annotations to help me out.

  # Usage

  You need two things to run this program effectively: a sampled wavefile and a .music file.

  To sample the wavefile into the .music run

      python3.6 shift.py (wavfile) (musicfile) ((bpm))

  The bpm is optional, and specifying it will set the samplefile's length to be consistent with the bpm.
