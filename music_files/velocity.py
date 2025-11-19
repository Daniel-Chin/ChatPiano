import os
import mido
from matplotlib.axes import Axes
from matplotlib import pyplot as plt

# matplotlib.use('TkAgg')
# matplotlib.use('Agg')

def histogram_velocity(midi_file_path: str, ax: Axes | None = None):
    # Load the MIDI file
    mid = mido.MidiFile(midi_file_path)
    ax = ax or plt.gca()
    
    # Extract velocity values from note_on messages
    velocities = []
    for track in mid.tracks:
        for msg in track:
            assert isinstance(msg, mido.Message | mido.MetaMessage), type(msg)
            if msg.type == 'note_on' and msg.velocity > 0:
                velocities.append(msg.velocity)
    
    # Plot histogram of velocities
    ax.hist(velocities, bins=range(0, 128), edgecolor='black', alpha=0.7)
    ax.set_title(os.path.basename(midi_file_path))
    ax.set_xlabel('Velocity')
    ax.set_ylabel('Frequency')
    ax.set_xlim(0, 127)
    ax.grid(axis='y', alpha=0.75)

def adjust_velocity(midi_file_path: str, output_file_path: str, factor: float):
    # Load the MIDI file
    mid = mido.MidiFile(midi_file_path)
    
    # Adjust velocity values
    for track in mid.tracks:
        for msg in track:
            assert isinstance(msg, mido.Message | mido.MetaMessage), type(msg)
            if msg.type == 'note_on' and msg.velocity > 0:
                new_velocity = int(msg.velocity * factor)
                msg.velocity = max(1, min(new_velocity, 127))  # Ensure velocity is between 1 and 127
    
    # Save the modified MIDI file
    mid.save(output_file_path)

def hist():
    mids = []
    for filename in os.listdir('.'):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            mids.append(filename)
    fig, axs = plt.subplots(len(mids), 1, sharex=True)
    for i, midi_file in enumerate(mids):
        histogram_velocity(midi_file, ax=axs[i])
        if i != len(mids) - 1:
            axs[i].set_xlabel('')
    plt.show()

if __name__ == "__main__":
    hist()
    # adjust_velocity('chatpiano_theme.mid', '_chatpiano_theme.mid', factor=0.6)
    # adjust_velocity('guojiao_3track.mid', '_guojiao_3track.mid', factor=0.6)
    # adjust_velocity('guojiao_3track_4bars.mid', '_guojiao_3track_4bars.mid', factor=0.6)
    # adjust_velocity('guojiao_3track_8bars.mid', '_guojiao_3track_8bars.mid', factor=0.6)
    # adjust_velocity('guojiao_mel_first2bars.mid', '_guojiao_mel_first2bars.mid', factor=1.0)
