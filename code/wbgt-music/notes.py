NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTEWITHOUTSHARP = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
OCTAVES = list(range(10))
NOTES_IN_OCTAVE = len(NOTES)



def noteToNumber(note: str, octave: int) -> int:
    assert note in NOTES, "Wrong note name."
    assert octave in OCTAVES, "Wrong octave number."
    return int( NOTES.index(note) + (NOTES_IN_OCTAVE * (octave+1)) )

def noteNumberToFreq(noteNumber):
    return 440 * (2**((noteNumber-69)/12))

def noteNumberToNote(noteNumber):
    octave = noteNumber // 12 - 1
    c = 12 * (octave + 1)
    return(NOTES[noteNumber - c] + str(octave))

def nextNoteName(firstNote):
    if firstNote.startswith("B"):
        nextNoteLetter = "C"
        nextNoteNumber = str(int(list(firstNote)[1]) + 1)
        nextNote = nextNoteLetter + nextNoteNumber
    else:
        nextNoteLetter = NOTEWITHOUTSHARP[NOTEWITHOUTSHARP.index(list(firstNote)[0]) + 1]
        nextNoteNumber = str(int(list(firstNote)[1]))
        nextNote = nextNoteLetter + nextNoteNumber
        
    return(nextNote)


if __name__ == "__main__":
    print( noteToNumber("A", 4) ) # 69
    print( noteToNumber("A", 0) ) # 21
    print(noteNumberToNote(60)) #C4
    print(noteNumberToNote(67)) #G4
    print(nextNoteName("F4")) #G4
    print(nextNoteName("B5")) #C6


 
