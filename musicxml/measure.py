from musicxml import instruments

note_types = {
    1.0: 'sixteenth',
    2.0: 'eighth',
    4.0: 'quarter',
    8.0: 'half',
    16.0: 'full'
}




class Measure:
    def __init__(self, tempo, number, meter):
        self.tempo = tempo
        self.number = number
        self.beats = meter[0]
        self.beat_type = meter[1]
        self.clef_sign = 'F'
        self.clef_line = 4
        self.notes = []

    def beats_to_notes(self, beats):
        if len(beats) != 2:
            raise Exception

        # snare
        for i in range(0, len(beats[0])):
            if len(self.notes) < i+1:
                self.notes.append([])

            if beats[0][i] == 1:
                self.notes[i].append(instruments.SnareDrum())

        # kick
        for i in range(0, len(beats[1])):
            if len(self.notes) < i+1:
                self.notes.append([])

            if beats[1][i] == 1:
                self.notes[i].append(instruments.KickDrum())

    def print_measure(self):
        for note in self.notes:
            print(note)