# Format of .music files

While I'm sure there are some code friendly music transcription formats already available, I decided to make this one to keep things simple for this project. The basic format is like this

    chord
    chord
    chord
    ...

Where a chord is formatted like

`note, note, note, note`.

Here's the format for notes.

# Notes

Let's say you wanted the first note of your song to be C4. That would simply be transcribed as `C4` as a note. If C4 is followed by other notes in the same octave, the octave number may be omitted. For example

    C2
    D2
    E2
    G2
    E3
    E3
    E5

could be condensed down to

    C2
    D
    E
    G
    E3
    E
    E5

If notes repeat like

    E5
    E
    E
    D
    F
    G
    G

you can condense that down using the 'multiple' operator like so

    3x E5
    D
    F
    2x G

In general, if you play (n) repeats of the same note you can condense it down as `(n)x note`

This supports sharps and flats, which are transcribed by either adding a sharp or lowercase f respectively at the end of the note. e.g. `C#5`, `Bf6`, etc..

If you want to add a half note, whole note, etc. Just add the relative duration at the start of the note. Since all notes default to quarter notes, `.5 C5` would be an eighth note, `2 C5` would be a half note, and `4 C5` would be a whole note.

These can all combine, so if you have 3 repeats of a C#5 whole note you can transcribe it as `3x 4 C#5`

# Chords

Chords are literally just notes separated by commas.

A major C chord would be `C5, E, G`, etc..

# Bonus Options
If you have a repeating section of music like

    C1
    C2
    C3
    C1
    C2
    C3
    C1
    C2
    C3

you can avoid repeating it all of those times and just write

    SR 2
    C1
    C2
    C3
    ER

`SR` stands for Start Repetition and can optionally take, as an argument, the
number of times you would like to additionally repeat. The default number of
repetitions is 1. To signify the end of the repeated portion of music, add an `ER` which stands for End Repetition.

## Note!

`SR 3` will not loop a section 3 times, it will loop it 4 times. Once for the original section of music and thrice for the repetition will make 4 total repetitions.

# tl;dr

Notes are in the format `(repeat)x (duration) (note)(octave)`

Chords are comma-separated notes

A song is line-separated chords

Repetitions are started by `SR [num reps]` and ended by `ER`

# tl;drt tl;dr

A song is a csv of notes with a .music on the end and bonus options for repeat sections.
