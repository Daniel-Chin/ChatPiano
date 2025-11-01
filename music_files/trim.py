# Drafted by GPT-5
from mido import MidiFile, MidiTrack

input_path  = 'guojiao_3track.mid'
bars_to_keep   = 8
output_path = f'guojiao_3track_{bars_to_keep}bars.mid'

midi = MidiFile(input_path)
ticks_per_beat = midi.ticks_per_beat
beats_per_bar  = 2
max_ticks      = bars_to_keep * beats_per_bar * ticks_per_beat

trimmed = MidiFile(ticks_per_beat=midi.ticks_per_beat)

for track in midi.tracks:
    new_track = MidiTrack()
    current_ticks = 0
    for msg in track:
        current_ticks += msg.time
        if current_ticks > max_ticks - 0.1:
            break
        new_track.append(msg)
    trimmed.tracks.append(new_track)

trimmed.save(output_path)
print('Saved:', output_path)

