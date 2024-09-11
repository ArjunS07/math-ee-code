import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
from numpy.fft import fft, rfft
import csv
np.seterr(divide = 'ignore') 

import settings

def generate_spectrogram(sample_rate_hz: int, audio_data: np.ndarray, window_size: int = settings.WINDOW_SIZE, hop_size: int = settings.HOP_SIZE) -> np.ndarray:
    """"
    Generates a spectrogram from the given audio data

    sample_rate_hz: The sample rate of the audio data
    audio_data: The audio data as an array of samples
    window_size: The length of the frame on which the STFFT is performed
    hop_size: The number of samples between the start of adjacent frames 
    """
    # Calculate the number of frames and initialize the spectrogram matrix
    num_frames = 1 + (len(audio_data) - window_size) // hop_size

    # Each column corresponds to the magnitudes from one frame. Each row corresponds to the magnitudes at one frequency
    spectrogram = np.zeros((window_size // 2 + 1, num_frames), dtype=np.float32)

    for t in range(num_frames):
        start = t * hop_size
        end = start + window_size
        audio_frame = audio_data[start:end]
        frame = audio_frame * np.hanning(window_size)
        frame = np.abs(rfft(frame))
        spectrogram[:, t] = frame
    
    frequency_values = np.fft.rfftfreq(window_size, 1 / sample_rate_hz)
    return spectrogram, frequency_values

def plot_spectrogram(spectrogram, hop_size, sample_rate_hz):
    plt.imshow(
        np.log1p(spectrogram),
        cmap="viridis",
        aspect="auto",
        origin="lower",
        extent=[0, len(spectrogram[0]) * hop_size / sample_rate_hz, 0, sample_rate_hz / 2],
    )
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()

def generate_fingerprints_from_spectrogram(spectrogram: np.array, frequencies: np.array, sampling_rate_hz: int) -> np.array:

    # Transpose the spectrogram
    spectrogram = spectrogram.T
    num_frames, frame_width = spectrogram.shape
    fingerprints = []

    for frame_index in range(num_frames):
        magnitudes = spectrogram[frame_index]
        assert len(magnitudes) == len(frequencies)
        
        frame_fingerprints = []
        for lower, upper in settings.FREQUENCY_BUCKETS_FOR_FINGERPRINTS:
            bucket_freqs_mags = [(freq, mag) for (freq, mag) in zip(frequencies, magnitudes) if lower <= freq < upper]
            if len(bucket_freqs_mags) == 0: continue
            frame_fingerprints.append(sorted(bucket_freqs_mags, key=lambda x: x[1], reverse=True)[0][0])
        frame_fingerprint = "".join([str(int(f)) for f in frame_fingerprints])
        fingerprints.append(frame_fingerprint)
    return fingerprints


def generate_fingerprints_for_audio(audio_path: str):
    sample_rate_hz, audio_data = scipy.io.wavfile.read(audio_path)
    audio_data = np.mean(audio_data, axis=1) # convert stereo to mono
    spectrogram, frequencies = generate_spectrogram(sample_rate_hz, audio_data)
    fingerprints = generate_fingerprints_from_spectrogram(spectrogram, frequencies, sample_rate_hz)
    return fingerprints

if __name__ == "__main__":
    fingerprints_database = []
    with open(settings.TRACKS_DATABASE_PATH, "r") as database_file:
        database_reader = csv.reader(database_file)
        for row in database_reader:
            try:
                name, audio_path = row
                audio_path = f'music_recognition/{audio_path}'
                fingerprints = generate_fingerprints_for_audio(audio_path=audio_path)
                fingerprints = " ".join(fingerprints)
                fingerprints_database.append((name, fingerprints))
                print(f"Generated fingerprints for {name}")
            except Exception as e:
                print(f"Failed to generate fingerprints for {name}: {e}")
                continue
    
    with open(settings.FINGERPRINTS_DATABASE_PATH, "w") as database_file:
        database_writer = csv.writer(database_file)
        for title, fingerprints in fingerprints_database:
            try:
                database_writer.writerow([title, fingerprints])
                print(f"Wrote fingerprints for {title} to database")
            except Exception as e:
                print(f"Failed to write fingerprints for {title} to database: {e}")
                continue