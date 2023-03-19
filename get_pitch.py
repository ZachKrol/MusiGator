import pyaudio
import numpy as np
import scipy
import aubio
from scipy.signal import find_peaks
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def get_pitch(signal):
    pitch_detector = aubio.pitch("default", 2048, 2048 // 2, 44100)
    pitch_detector.set_unit("Hz")
    pitch_detector.set_silence(-40)
    pitch = pitch_detector(signal)[0]
    return pitch




def pitch_to_note(pitch):
    # Define the standard pitches for each note
    standard_pitches = 440 * 2**((np.arange(12 * 8) - 57) / 12)
    
    # Find the nearest standard pitch
    pitch_index = np.abs(standard_pitches - pitch).argmin()
    
    # Map the pitch to the nearest musical note
    note = notes[pitch_index % 12]
    octave = pitch_index // 12 - 1
    
    return note + str(octave)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, input=True, frames_per_buffer=2048)
target_note = 'C2'
note_held_time = 0.0
while True:
    data = stream.read(1024, exception_on_overflow=False)
    signal = np.frombuffer(data, dtype=np.float32)
    pitch = get_pitch(signal)
    note = pitch_to_note(pitch)
    if pitch > 0:
        if note == target_note:
            note_held_time += 1024/44100 # increment the note held time by the buffer length
            if note_held_time >= 2.0:
                break # exit the loop if the note has been held for more than two seconds
        elif note_held_time > 0:
            note_held_time -= 1024/44100 # decrement the note held time if the note changes
    print(note, note_held_time)
print("Note held!")